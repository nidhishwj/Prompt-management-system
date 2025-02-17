from typing import List, Optional, Union, Literal, Any, TypedDict
from src.config.response import FailureResponse
from typing import Optional, Literal, Dict
from src.models.prompt import ParameterList, Data, Prompt, SuccessResponseModel, FailureResponseModel
from src.exceptions.prompt_exception import MissingKeyException


class PromptHelper:
    def get_prompts_recursively(self,
                                name: str,
                                langfuse: object,
                                label: Optional[str] ="latest",
                                prompt_listing: Optional[bool] = False,
                                prompts_list: List[str]=None, 
                                parameter_list: Optional[Dict[str, Dict[str, Any]]] =None):
        if prompts_list is None:
            prompts_list=[]

        prompt =langfuse.get_prompt(name=name, label=label)
        prompt_params = parameter_list.get(name, {}) if parameter_list else {}
        self.placeholder_validation(prompt, **prompt_params)
        print(prompt.variables)
        compiled_prompt = prompt.compile(**prompt_params)

        tags= [tags.split()[1] for tags in prompt.tags if "parents" in tags.lower()]

        # labels=[lbl for lbl in prompt.labels if lbl.lower() not in ["production", "latest"]]

        prompts_list.append(compiled_prompt)

        if tags==[]:
            if prompt_listing:
                print("listing happened")
                return prompts_list[::-1]
            else:
                return self.concat_prompts(prompts_list)
        else:
            return self.get_prompts_recursively(name=tags[0],
                                                langfuse=langfuse,
                                                label=label,
                                                parameter_list=parameter_list,
                                                prompt_listing=prompt_listing,
                                                prompts_list=prompts_list)

    def concat_prompts(self, prompts_list: List[str] = None):
        concatenated_string='\n'.join(prompts_list[::-1])
        return concatenated_string

    def placeholder_validation(self, prompt, **prompt_params):
        required_keys=prompt.variables
        kwargs_keys=prompt_params.keys()
        missing_keys = ", ".join([key for key in required_keys if key not in kwargs_keys])
        if missing_keys != "":
            raise MissingKeyException(FailureResponse.missingKey.format(prompt_name=prompt.name, missing_keys= missing_keys))
        return True

    def convert_to_list(self, value: Optional [str]) ->List[str]:
        if value:
            return [item.strip() for item in value.split(",")]
        return ["latest"]

def create_response(statusCode: int,
                    response: str,
                    prompt_name: str,
                    prompt: Union[str, List[str]],
                    label: str,
                    version: Optional[int] = None,
                    include_data: Optional[bool]= False) -> dict:
    if statusCode == 200:
        data = {}
        if include_data:
            data=Data(
                prompt=[Prompt(
                    promptName=prompt_name,
                    version=version,
                    Stage=label,
                    Prompt=prompt
                )],
                promptSummary=""
            )
        return SuccessResponseModel(
            statusCode=statusCode,
            status="OK",
            response=response,
            error=None,
            data=data
        ).model_dump()
    else:
        return FailureResponseModel(
            statusCode=statusCode,
            status="Failed",
            response=None,
            error=response,
            data={}
        ).model_dump()