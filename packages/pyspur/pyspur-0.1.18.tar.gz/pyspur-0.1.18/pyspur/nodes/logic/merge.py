import logging
from typing import Optional

from pydantic import BaseModel, create_model

from ..base import BaseNode, BaseNodeConfig, BaseNodeInput, BaseNodeOutput

logger = logging.getLogger(__name__)


class MergeNodeConfig(BaseNodeConfig):
    has_fixed_output: bool = False


class MergeNodeInput(BaseNodeInput):
    pass


class MergeNodeOutput(BaseNodeOutput):
    class Config:
        arbitrary_types_allowed = True

    pass


class MergeNode(BaseNode):
    """Takes all its inputs and merge them into one output."""

    name = "merge_node"
    display_name = "Merge"
    input_model = MergeNodeInput
    config_model = MergeNodeConfig

    async def run(self, input: BaseModel) -> BaseModel:
        data = input.model_dump()

        self.output_model = create_model(
            f"{self.name}",
            **{k: (Optional[type(v)], ...) for k, v in data.items()},
            __base__=MergeNodeOutput,
            __module__=self.__module__,
            __doc__=f"Output model for {self.name} node",
            __cls_kwargs__=None,
            __config__=None,
            __validators__=None,
        )
        return self.output_model(**data)
