from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic
from neurosdk.core.messages.action import Action, ResultActionData
from dataclasses_json import DataClassJsonMixin
from marshmallow_jsonschema import JSONSchema
import json

class NeuroAction(ABC):
    dataType: type[DataClassJsonMixin] | None = None

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

    def get_schema(self) -> dict[str, Any]:
        if self.__class__.dataType is None:
            return {}
        return JSONSchema().dump(self.__class__.dataType.schema())

    def can_be_used(self) -> bool:
        return True

    def validate_action(self, data: str) -> bool:
        if self.__class__.dataType is None:
            return True
        return len(self.__class__.dataType.schema().validate(json.loads(data))) == 0

    def dict_to_data(self, data: str) -> DataClassJsonMixin | None:
        if self.__class__.dataType:
            return self.__class__.dataType.from_json(data)
        return None

    @abstractmethod
    def execute_action(self, id: str, data: type[DataClassJsonMixin] | None) -> ResultActionData:
        pass

    def to_json(self) -> Action:
        return Action(
            name=self.get_name(),
            description=self.get_description(),
            schema_=self.get_schema(),
        )
