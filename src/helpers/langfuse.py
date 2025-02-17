from src.config.config_manager import ConfigManager
from src.config.response import SuccessResponse, FailureResponse
from src.models.prompt import NewPromptRequest, PromptRetrivalRequest, ChatMessageDict
from typing_extensions import List, Optional, Annotated
from fastapi.responses import JSONResponse
import os
import pandas as pd
import io
from langfuse import Langfuse
from dotenv import load_dotenv
from typing import List, Optional, Union, Literal, Any, TypedDict, Dict
from src.helpers.prompt_helper import PromptHelper, create_response
from src.exceptions.prompt_exception import PromptAlreadyExistsException, PromptNotFoundException
from fastapi import HTTPException

load_dotenv()

langfuse = Langfuse(
    secret_key="sk-1f-080356eb-21cb-492c-8c61-282108618477",
    public_key="pk-1f-46181f65-7d5a-4f87-8186-ae89e0ff1c41",
    host="https://us.cloud.langfuse.com"
)

prompt_helper= PromptHelper()

class langfuse_manager:
    
    def __init__(self, config_manager: ConfigManager):
        self.env_config = config_manager()
        self._secret_key: str = self.env_config.get(key = "secret_key")
        self._public_key: str = self.env_config.get(key = "public_key")
        self._host_url: str = self.env_config.get(key = "host_url")

    def create_new_prompt(name:str,
                          prompt:str,
                          labels: Optional [str] = "latest",
                          tags: Optional[str] = "",
                          type: Optional[str]= "text",
                          config: Optional [Any] = None):
        try:
            langfuse.get_prompt(names=name, label="latest")
            raise PromptAlreadyExistsException(f"Prompt with name (name) already exists.")
        except PromptAlreadyExistsException as e:
            return create_response(statusCode=409,
                                   response=FailureResponse.create,
                                   prompt_name="",
                                   prompt="",
                                   label="")
        except Exception as e:
            langfuse.create_prompt(name-name,
                                   type-type,
                                   prompt=prompt,
                                   tags=prompt_helper.convert_to_list(tags),
                                   labels=prompt_helper.convert_to_list(labels), 
                                   config=config)
            return create_response(statusCode=200,
                                   response=SuccessResponse.create,
                                   prompt_name=name,
                                   prompt=prompt,
                                   label=labels,
                                   version=1)

    def retrieve_prompt(name:str,
                        label: Optional [str] = None,
                        version: Optional [int] = None,
                        flag: Optional [bool] = False,
                        prompt_listing: Optional [bool] = False,
                        parameter_list: Optional [Dict[str, Dict[str, Any]]] = None):

        if flag:
            prompts_list= prompt_helper.get_prompts_recursively(name=name,
                                                                langfuse=langfuse,
                                                                label=label,
                                                                prompt_listing=prompt_listing,
                                                                parameter_list=parameter_list)
            
            # return prompts_list
        else:
            prompt_params=parameter_list.get(name, ())if parameter_list else {}
            if version is None and label is None:
                return create_response(statusCode=422,
                                        response=FailureResponse.versionLabelAbsent,
                                        prompt_name=name,
                                        prompt="",
                                        label="")
            elif version is not None and label is not None:
                return create_response(statusCode=422,
                                        response=FailureResponse.versionLabelPresent,
                                        prompt_name=name,
                                        prompt="",
                                        label="")
            elif version == None:
                prompt=langfuse.get_prompt(name=name, label=label)
            else:
                prompt=langfuse.get_prompt(name=name, version=version)
                #print(dir(prompt))
                prompt_helper.placeholder_validation (prompt, **prompt_params)
                prompts_list = prompt.compile(**prompt_params)
                version=prompt.version
            return create_response(statusCode=200,
                                    response=SuccessResponse.retrieve,
                                    prompt_name=name,
                                    prompt=prompts_list,
                                    label=label if label is not None else "latest",
                                    version=version if version is not None else 8,
                                    include_data=True)

    def prompt_versioning(name:str,
                            prompt:str,
                            labels:Optional[str] = "latest",
                            tags: Optional[str] ="",
                            type: Optional [str]= "text",
                            config: Optional [Any]= None):
        try:
            langfuse.get_prompt(name= name, label = "latest")
            obj=langfuse.create_prompt(name=name,
                                        type=type,
                                        prompt=prompt,
                                        tags=prompt_helper.convert_to_list(tags),
                                        labels=prompt_helper.convert_to_list(labels),
                                        config=config)
            return create_response(statusCode=208,
                                    response=SuccessResponse.version,
                                    prompt_name=name,
                                    prompt=prompt,
                                    label=labels,
                                    version=obj.version)
        except PromptNotFoundException:
            return {"message": "prompt not available"}
        except Exception as e:
            if "NotFoundError" in str(e):
                return create_response(statusCode=484,
                                        response=FailureResponse.version,
                                        prompt_name=name,
                                        prompt=prompt,
                                        label=labels)
            else:
                raise HTTPException(status_code=500, detail=f"Unexpected error {str(e)}")

    def promote_prompt(name: str, version: int, new_labels: Optional[str]= "latest"):
        langfuse.update_prompt(name=name,
                               version=version, 
                               new_labels=prompt_helper.convert_to_list(new_labels), )