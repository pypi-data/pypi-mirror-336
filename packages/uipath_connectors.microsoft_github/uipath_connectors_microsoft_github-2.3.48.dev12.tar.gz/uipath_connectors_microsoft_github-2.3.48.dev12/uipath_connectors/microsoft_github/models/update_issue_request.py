from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.update_issue_request_assignee import UpdateIssueRequestAssignee
from ..models.update_issue_request_labels_array_item_ref import (
    UpdateIssueRequestLabelsArrayItemRef,
)
from ..models.update_issue_request_milestone import UpdateIssueRequestMilestone
from ..models.update_issue_request_state import UpdateIssueRequestState


class UpdateIssueRequest(BaseModel):
    """
    Attributes:
        assignee (Optional[UpdateIssueRequestAssignee]):
        assignees (Optional[list[str]]):
        body (Optional[str]): The contents of the issue Example: It looks like the new widget form is broken on Safari.
                When I try and create the widget, Safari crashes. This is reproducible on 10.8, but not 10.9. Maybe a browser
                bug?.
        labels (Optional[list['UpdateIssueRequestLabelsArrayItemRef']]):
        milestone (Optional[UpdateIssueRequestMilestone]):
        state (Optional[UpdateIssueRequestState]): The open or closed state of the issue. Can be one of: open, closed
                Example: open.
        title (Optional[str]): The title of the issue Example: Widget creation fails in Safari on OS X 10.8.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    assignee: Optional["UpdateIssueRequestAssignee"] = Field(
        alias="assignee", default=None
    )
    assignees: Optional[list[str]] = Field(alias="assignees", default=None)
    body: Optional[str] = Field(alias="body", default=None)
    labels: Optional[list["UpdateIssueRequestLabelsArrayItemRef"]] = Field(
        alias="labels", default=None
    )
    milestone: Optional["UpdateIssueRequestMilestone"] = Field(
        alias="milestone", default=None
    )
    state: Optional["UpdateIssueRequestState"] = Field(alias="state", default=None)
    title: Optional[str] = Field(alias="title", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["UpdateIssueRequest"], src_dict: Dict[str, Any]):
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
