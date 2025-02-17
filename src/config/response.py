class SuccessResponse:
    create= "Prompt Created Successfully"
    version= "Prompt Updated Successfully"
    retrieve= "Prompt Retrieved Successfully"

class FailureResponse:
    create= "Prompt Name Already Exist"
    version= "Prompt name doesn't exist for versioning"
    versionLabelAbsant= "Invalid Input: Either 'version' or 'label' must be provided" 
    versionLabelPresant= "Invalid Input: Provide either 'verston' or 'label', but not both"
    missingKey= "Prompt '{prompt_name}' is missing the following keys: {missing_keys}. Please ensure all required keys are provided."