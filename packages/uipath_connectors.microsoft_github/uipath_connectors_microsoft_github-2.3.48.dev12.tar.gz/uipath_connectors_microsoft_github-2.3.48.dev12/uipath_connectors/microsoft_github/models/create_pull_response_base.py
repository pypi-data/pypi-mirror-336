from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.create_pull_response_base_repo import CreatePullResponseBaseRepo
from ..models.create_pull_response_base_user import CreatePullResponseBaseUser


class CreatePullResponseBase(BaseModel):
    """
    Attributes:
        ref (str): The name of the branch you want the changes pulled into. This should be an existing branch on the
                current repository. You cannot submit a pull request to one repository that requests a merge to a base of
                another repository.
        label (Optional[str]):
        repo (Optional[CreatePullResponseBaseRepo]):
        sha (Optional[str]):
        user (Optional[CreatePullResponseBaseUser]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    ref: str = Field(alias="ref")
    label: Optional[str] = Field(alias="label", default=None)
    repo: Optional["CreatePullResponseBaseRepo"] = Field(alias="repo", default=None)
    sha: Optional[str] = Field(alias="sha", default=None)
    user: Optional["CreatePullResponseBaseUser"] = Field(alias="user", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["CreatePullResponseBase"], src_dict: Dict[str, Any]):
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
