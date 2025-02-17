from fastapi import FastAPI, APIRouter, Request, UploadFile, File
from fastapi.encoders import jsonable_encoder
from typing_extensions import List, Optional, Union, Literal, Any, TypedDict
from src.helpers.langfuse import langfuse_manager
router=APIRouter()

@router.post("/PMS/api/v2.1/admin/sources/version", tags=["Prompt Versioning"])
def prompt_versioning(prompt_name: str,
                        prompt: str,
                        labels: Optional [str] = "latest",
                        tags: Optional[str] = ""):
    return langfuse_manager.prompt_versioning(name= prompt_name,                                          
                                            prompt=prompt, 
                                            labels=labels,
                                            tags=tags)

@router.post("/PMS/api/v2.1/promote",tags=["Update prompt label"])
def promote_prompt(prompt_name: str,
                    version: int,
                    new_labels: Optional[str] = "latest"):
    return langfuse_manager.promote_prompt(name=prompt_name,
                                            version=version,
                                            new_labels=new_labels)

