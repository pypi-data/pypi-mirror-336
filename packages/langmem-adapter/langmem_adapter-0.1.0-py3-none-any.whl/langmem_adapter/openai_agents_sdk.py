"""
This module provides a LangMemToolAdapter class that adapts LangMem tools to be used with the OpenAI Agents SDK.

The LangMemToolAdapter class is a generic class that adapts LangMem tools to be used with the OpenAI Agents SDK.
It supports both static (pre‑injected store) and dynamic store injection.
"""

import asyncio
import inspect
import json
import uuid
import string

from typing import Any, Callable, Dict, Optional, cast, Union, TypeVar, Generic
from pydantic import BaseModel, Field, create_model
from agents import FunctionTool, RunContextWrapper

TContext = TypeVar("TContext", bound=BaseModel)

def extract_template_keys(template: str) -> set:
    """Extract placeholder keys from a template string."""
    formatter = string.Formatter()
    return {field_name for _, field_name, _, _ in formatter.parse(template) if field_name}


class LangMemOpenAIAgentToolAdapter(Generic[TContext]):
    """
    Adapter for langmem tools that supports both static (pre‑injected store)
    and dynamic store injection. In dynamic mode, a store_provider callable is provided
    that yields a fresh store instance (via an async context manager) on each invocation.

    In static mode, no store_provider is passed and the tool instance is used directly.
    """
    def __init__(self,
                langmem_tool: Any,
                store_provider: Optional[Callable[[], Any]] = None,
                 namespace_template: Optional[tuple[str, ...]] = None
                ):
        """
        Args:
            langmem_tool:
                - In static mode, an already‑constructed tool instance.
                - In dynamic mode, a factory callable that accepts a store and returns a tool.
            store_provider:
                An optional callable that returns an async context manager yielding a store.
                If provided, dynamic mode is enabled.
            namespace_template:
                An optional template string (e.g. "memories/{user_name}") used to dynamically
                construct the namespace from context (ctx.content). If the required keys are missing,
                an error is returned.
        """
        self.store_provider = store_provider
        self.namespace_template = namespace_template

        if self.store_provider is None:
            # Static mode: use the provided tool directly.
            self.langmem_tool = langmem_tool
            self.name = getattr(langmem_tool, "name", langmem_tool.__class__.__name__)
            self.description = getattr(langmem_tool, "description", "") or ""
            self._callable = getattr(langmem_tool, "func", getattr(langmem_tool, "run", None))
            if not callable(self._callable):
                raise AttributeError(f"{self.name} has no callable 'func' or 'run' method.")
        else:
            # Dynamic mode: call the factory with a dummy store (None) to get a dummy instance.
            self.langmem_tool = langmem_tool
            dummy_tool = langmem_tool(None)
            self.name = getattr(dummy_tool, "name", dummy_tool.__class__.__name__)
            self.description = getattr(dummy_tool, "description", "") or ""
            self._callable = getattr(dummy_tool, "func", getattr(dummy_tool, "run", None))
            if not callable(self._callable):
                raise AttributeError("Dynamic tool instance (dummy) is missing callable 'func' or 'run'.")

        # Generate JSON schema from the callable's signature.
        sig = inspect.signature(cast(Callable[..., Any], self._callable))
        fields = {}
        self._uuid_fields = set()
        self._json_fields = set()
        self._optional_fields = set()

        for k, v in sig.parameters.items():
            if k == "self" or v.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue
            param_type = v.annotation

            if getattr(param_type, '__origin__', None) is Union:
                args = param_type.__args__
                if type(None) in args:
                    self._optional_fields.add(k)
                    args = [a for a in args if a is not type(None)]
                    param_type = args[0]

            if param_type is uuid.UUID:
                param_type = str
                self._uuid_fields.add(k)
            elif param_type in (dict, Dict[str, Any]):
                param_type = str
                self._json_fields.add(k)

            fields[k] = (param_type, Field(default="") if k in self._optional_fields else ...)

        self.args_schema = create_model(f"{self.name}Args", **fields)
        self.params_json_schema = self.args_schema.model_json_schema()

        self.tool = FunctionTool(
            name=self.name,
            description=self.description,
            params_json_schema=self.params_json_schema,
            on_invoke_tool=self._on_invoke_tool,
        )

    async def _on_invoke_tool(self, ctx: RunContextWrapper[TContext], args: str) -> str:
        # Parse arguments using our generated schema.
        parsed_args = self.args_schema.model_validate_json(args).model_dump(exclude_unset=True)

        # For optional fields, convert empty strings to None.
        for field in self._optional_fields:
            if parsed_args.get(field) == "":
                parsed_args[field] = None

        # Convert UUID fields from string to uuid.UUID.
        for field in self._uuid_fields:
            val = parsed_args.get(field)
            if val:
                try:
                    parsed_args[field] = uuid.UUID(val)
                except ValueError:
                    return f"Error: Invalid UUID format provided for '{field}'. Please provide a valid UUID."

        # Convert JSON fields from string to actual dict.
        for field in self._json_fields:
            if parsed_args.get(field):
                try:
                    parsed_args[field] = json.loads(parsed_args[field])
                except json.JSONDecodeError:
                    return f"Error: Invalid JSON format provided for '{field}'. Please provide valid JSON."

        # If we're in dynamic mode, obtain a fresh store and create a tool instance.
        if self.store_provider is not None:
            async with self.store_provider() as store:
                # Create a new tool instance with the store injected.
                if self.namespace_template:
                    context_dict = ctx.context.model_dump()  # TContext is bound to BaseModel
                    formatted_namespace = []
                    for template in self.namespace_template:
                        required_keys = extract_template_keys(template)
                        missing_keys = [key for key in required_keys if key not in context_dict]
                        if missing_keys:
                            return f"Error: Missing required context values for namespace element '{template}': {missing_keys}"
                        formatted_namespace.append(template.format(**context_dict))
                    formatted_namespace = tuple(formatted_namespace)
                else:
                    formatted_namespace = None

                # Create a new tool instance with the store injected and the formatted namespace.
                tool_instance = self.langmem_tool(store, namespace=formatted_namespace)
                callable_ = getattr(tool_instance, "func", getattr(tool_instance, "run", None))

                if not callable(callable_):
                    return "Error: Dynamic tool instance is missing a callable method."
                try:
                    result = (
                        await callable_(**parsed_args)
                        if inspect.iscoroutinefunction(callable_)
                        else await asyncio.to_thread(callable_, **parsed_args)
                    )
                    return result
                except ValueError as e:
                    return f"Error: {str(e)}"
                except Exception as e:
                    return f"Unhandled error: {str(e)}"
        else:
            # Static mode: simply call the pre‑constructed tool.
            try:
                result = (
                    await self._callable(**parsed_args)
                    if inspect.iscoroutinefunction(self._callable)
                    else await asyncio.to_thread(self._callable, **parsed_args)
                )
                return result
            except ValueError as e:
                return f"Error: {str(e)}"
            except Exception as e:
                return f"Unhandled error: {str(e)}"

    def as_tool(self) -> FunctionTool:
        return self.tool
