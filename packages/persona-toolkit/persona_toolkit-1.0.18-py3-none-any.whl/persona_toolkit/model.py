import asyncio
import logging
from typing import Type, Callable, Optional

from pydantic import BaseModel
from pydantic.alias_generators import to_camel

logger = logging.getLogger(__name__)


def map_model_props(schema: dict):
    """Define a standard format for model properties to be used in API documentation."""
    properties = schema.get("properties", {})
    required = schema.get("required", [])
    title = schema.get("title", "")
    _type = schema.get("type", "object")
    fields = {}
    for field_name, field_info in properties.items():
        param = {
            "type": field_info.get("type", "string"),
            "description": field_info.get("description", ""),
        }
        if "items" in field_info:
            param["items"] = field_info["items"]
        fields[field_name] = param

    return {
        "title": title,
        "type": _type,
        "properties": fields,
        "required": required,
    }


class Tool:
    def __init__(
            self,
            name: str,
            input_model: Type[BaseModel],
            output_model: Type[BaseModel],
            handler: Callable[..., BaseModel],
            is_async: bool = False,
    ):
        self.name = name
        self.input_model = input_model
        self.output_model = output_model
        self.handler = handler
        self.is_async = is_async

    def schema(self):
        return {
            "name": self.name,
            "description": self.handler.__doc__ or f"Function for {self.name}",
            "parameters": map_model_props(self.input_model.model_json_schema()),
            "output": map_model_props(self.output_model.model_json_schema()),

        }

    async def run(self, request: "InvocationRequest") -> "InvocationResponse":
        parsed = self.input_model.model_validate(request.input)
        try:
            if self.is_async:
                result = await self.handler(parsed, session_id=request.session_id, project_id=request.project_id,
                                            user_id=request.user_id)
            else:
                def call_handler():
                    return self.handler(parsed, session_id=request.session_id, project_id=request.project_id,
                                        user_id=request.user_id)

                result = await asyncio.get_event_loop().run_in_executor(None, call_handler)
            output = result.model_dump()
            logger.info(f"Tool {self.name} invoked. Input: {parsed}, Output {output}")
            return InvocationResponse(success=True, output=output)
        except Exception as e:
            logger.info(f"Tool {self.name}, input {parsed}, failed with error: {e}")
            return InvocationResponse(success=False, error_message=str(e), output={})


class InvocationRequest(BaseModel):
    project_id: str
    session_id: str
    user_id: str
    tool: str
    input: dict

    class Config:
        populate_by_name = True
        alias_generator = to_camel


class InvocationResponse(BaseModel):
    success: bool
    error_message: Optional[str] = None
    output: dict

    class Config:
        populate_by_name = True
        alias_generator = to_camel
