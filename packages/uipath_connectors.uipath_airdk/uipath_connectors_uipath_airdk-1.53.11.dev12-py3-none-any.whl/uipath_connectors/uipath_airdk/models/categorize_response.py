from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class CategorizeResponse(BaseModel):
    """
    Attributes:
        content (str): The content to categorize. This must be provided as a string. Example: I am unable to access my
                email account. Whenever I try to log in, I receive an error message saying 'Invalid username or password.
        category (Optional[str]): The inferred category of the content
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    content: str = Field(alias="content")
    category: Optional[str] = Field(alias="category", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["CategorizeResponse"], src_dict: Dict[str, Any]):
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
