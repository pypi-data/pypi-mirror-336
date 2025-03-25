from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class AddDocumentToEnvelopeResponseEnvelopeDocumentsArrayItemRef(BaseModel):
    """
    Attributes:
        authoritative_copy (Optional[str]):  Example: false.
        contains_pdf_form_fields (Optional[str]):  Example: false.
        document_id (Optional[str]):  Example: 2.
        document_id_guid (Optional[str]):  Example: 0d0502b2-07ed-4ee4-89b5-e8c4dcaf1b63.
        name (Optional[str]):  Example: testdocument.txt.
        order (Optional[str]):  Example: 2.
        template_required (Optional[str]):  Example: false.
        type_ (Optional[str]):  Example: content.
        uri (Optional[str]):  Example: /envelopes/01bdd3c9-6174-43f1-aaa9-5210f5c098eb/documents/2.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    authoritative_copy: Optional[str] = Field(alias="authoritativeCopy", default=None)
    contains_pdf_form_fields: Optional[str] = Field(
        alias="containsPdfFormFields", default=None
    )
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_guid: Optional[str] = Field(alias="documentIdGuid", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    order: Optional[str] = Field(alias="order", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    type_: Optional[str] = Field(alias="type", default=None)
    uri: Optional[str] = Field(alias="uri", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["AddDocumentToEnvelopeResponseEnvelopeDocumentsArrayItemRef"],
        src_dict: Dict[str, Any],
    ):
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
