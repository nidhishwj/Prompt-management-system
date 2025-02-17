from fastapi import FastAPI, APIRouter, Request, UploadFile, File
from fastapi.encoders import jsonable_encoder
from src.config.config_manager import ConfigManager
from pydantic import BaseModel
import pathlib
import requests
import json
from typing import Optional, Literal, Dict, Any, List
from src.helpers.langfuse import langfuse_manager
from src.helpers.prompt_helper import create_response
from src.models.prompt import ParameterList, ResponseModel
from fastapi import APIRouter, HTTPException
from src.exceptions.prompt_exception import PromptAlreadyExistsException, MissingKeyException

router = APIRouter()

@router.post("/PMS/api/v2.1/create", tags=["Create new prompt"], response_model=ResponseModel)
def create_new_prompt(prompt_name: str, prompt: str, labels: Optional[str] = "latest", tags: Optional[str] = ""):
    try:
        return langfuse_manager.create_new_prompt(name= prompt_name, prompt= prompt, labels=labels, tags=tags)
    except PromptAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@router.post("/PMS/api/v2.1/retrieve", tags=["Retrieve Prompt"])
def retrieve_prompt(prompt_name: str,
                    version: Optional[int] = None, 
                    label: Optional [str]= None,
                    MultilevelPrompt: Optional [bool] = False,
                    return_as_list: Optional [bool] = False,
                    parameter_list: Optional [ParameterList] = None):
    try:
        prompts =langfuse_manager.retrieve_prompt(name=prompt_name,
                                                  version=version, 
                                                  label=label, 
                                                  flag=MultilevelPrompt, 
                                                  prompt_listing=return_as_list,
                                                  parameter_list=parameter_list.model_dump() if parameter_list else None)
        
        
        return prompts
    except MissingKeyException as e:
        
        return create_response (statusCode=400,
                                response=e.message, 
                                prompt_name="",
                                prompt="", 
                                label="")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected arror: (str(e))")