from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class AddDocumentToEnvelopeRequest(BaseModel):
    """
    Attributes:
        document_id (Optional[int]): The unique ID of the document within the envelope that needs to be replaced or
                added. You can specify the documentId yourself. Typically the first document has the ID 1, the second document
                2, and so on, but you can use any number from 1 through 2147483647. Default: 50. Example: 1.0.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    document_id: Optional[int] = Field(alias="documentId", default=50)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["AddDocumentToEnvelopeRequest"], src_dict: Dict[str, Any]):
        return cls.model_validate(src_dict)

    @property
    def additional_keys(self) -> list[str]:
        base_fields = self.model_fields.keys()
        return [k for k in self.__dict__ if k not in base_fields]

    def __getitem__(self, key: str) -> Any:
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def __delitem__(self, key: str) -> None:
        if key in self.__dict__:
            del self.__dict__[key]
        else:
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return key in self.__dict__
