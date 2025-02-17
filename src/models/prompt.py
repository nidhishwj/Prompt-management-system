from pydantic import BaseModel, Field, HttpUrl, RootModel
from typing_extensions import List, Optional, Union, Literal, Any, TypedDict, Dict

class PromptParameters (RootModel):
    root: Dict[str, Any] 

class ParameterList(RootModel):
    root: Dict[str, PromptParameters] = Field(
        example={
            "prompt_name1": {
                "key1": "value1",
                "key2": "value2"
            },
            "prompt_name2": {
                "key1": "valuel",
                "key2": "value2"
            }
        }
    )

class ChatMessageDict(TypedDict):
    role: str
    content: str

class NewPromptRequest(BaseModel):
    name: str
    prompt: Union[str, List[ChatMessageDict]]
    labels: List[str] = []
    tags: Optional[List[str]] = None
    type: Optional [Literal["chat", "text"]] = "text"
    config: Optional [Any] = None

class PromptRetrivalRequest(BaseModel):
    name: str
    version: Optional[int] = None
    label: Optional[str] = None
    type: Literal["chat", "text"] = "text"
    cache_ttl_seconds: Optional [int] = None
    fallback: Union[Optional [List[ChatMessageDict]], Optional[str]] = None
    max_retries: Optional [int] = None
    fetch_timeout_seconds: Optional[int] = None

class Prompt(BaseModel):
    promptName: str
    version: int
    Stage: str
    Prompt: Union [str, List[str]]

class Data (BaseModel):
    prompt: List[Prompt]
    promptSummary:str

class SuccessResponseModel (BaseModel):
    statusCode: int
    status: str
    response: str
    error: Optional [str]
    data: Optional [Union [Data, dict]]

class FailureResponseModel (BaseModel):
    statusCode:int
    status: str
    response: Optional[str]
    error: str
    data: dict

class ResponseModel (BaseModel):
    statusCode: int
    status: str
    response: Optional[str]
    error: Optional [str]
    data: Optional[Union [Data, dict]]