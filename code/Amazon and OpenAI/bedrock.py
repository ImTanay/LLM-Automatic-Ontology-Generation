import logging
import boto3
import botocore
import json
import time
# from notify import Notify

class BedrockWrapper:
  """Encapsulates Amazon Bedrock foundation model actions."""

  def __init__(self, model:str="mixtral", region_name:str="us-west-2"):
    """
    Initializes the BedrockWrapper class.

    :param model: the model to use (default is "mixtral")
    :param region_name: the region name (default is "us-west-2")
    """
    self.model = model
    self.bedrock_client = boto3.client(service_name="bedrock-runtime", region_name=region_name)
    # self.n = Notify("BedrockWrapper")

  def prepare_prompt(self, prompt:str)->dict:
    """
    Prepares the prompt for the model.

    :param prompt: the input prompt
    :return: the configuration dictionary
    """
    if self.model == "llama":
      configuration = {
       "modelId": "meta.llama2-70b-chat-v1",
       "body": json.dumps({"prompt":prompt,"max_gen_len":2048,"temperature":0.1,"top_p":1})
      }
    elif self.model == "mixtral":
      configuration = {
       "modelId": "mistral.mixtral-8x7b-instruct-v0:1",
       "body": json.dumps({"prompt":prompt, "max_tokens":2048, "temperature":0.1, "top_p":1, "top_k":100})
      }
    elif self.model == "mistral":
      configuration = {
       "modelId": "mistral.mistral-7b-instruct-v0:2",
       "body":json.dumps({"prompt":prompt, "max_tokens":2048, "temperature":0.1, "top_p":1, "top_k":100})
      }
    elif self.model == "cohere":
      configuration = {
      "modelId": "cohere.command-text-v14",
      "body": json.dumps({"prompt":prompt, "max_tokens":2048, "temperature":0.1, "p":1, "k":100})
      }
    elif self.model == "cohere-light":
      configuration = {
      "modelId": "cohere.command-light-text-v14",
      "body": json.dumps({"prompt":prompt, "max_tokens":2048, "temperature":0.1, "p":1, "k":100})
      }
    elif self.model == "claude-haiku":
      configuration = {
        "modelId": "anthropic.claude-3-haiku-20240307-v1:0",
        "body": json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2048,
        # "temperature":0.1, 
        # "p":1, 
        # "k":100,
        "messages": [
          {
          "role": "user",
          "content": [
            {
            "type": "text",
            "text": prompt
            }
          ]
          }
        ]
        })
      }
    elif self.model == "claude-sonnet":
      configuration = {
        "modelId": "anthropic.claude-3-sonnet-20240229-v1:0",
        "body": json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2048,
        # "temperature":0.1, 
        # "p":1, 
        # "k":100,
        "messages": [
          {
          "role": "user",
          "content": [
            {
            "type": "text",
            "text": prompt
            }
          ]
          }
        ]
        })
      }
      
    else:
      raise Exception("Error with the MODEL parameter. Valid values are llama, mistral or mixtral") 

    return configuration

  def invoke_model(self, prompt:str, verbose:bool=False, test:bool=False):
    """
    Invokes the model and returns the content.

    :param prompt: the input prompt
    :param verbose: whether to print verbose output (default is False)
    :param test: whether to run in test mode (default is False)
    :return: the output response
    """
    output_response = ""
    
    try:
      if verbose: print("Model code: ",self.model)
      if verbose: print("PROMPT: ",prompt)
      params = self.prepare_prompt(prompt)

      if not test:
        response = self.bedrock_client.invoke_model(
          body=params["body"], modelId=params["modelId"], accept="application/json", contentType="application/json"
        )
        response_body = json.loads(response.get("body").read())

        if verbose: print("actual model: ",params["modelId"])
        
        # mapping output response to the response content 
        if params["modelId"].startswith("meta"):        output_response = response_body.get("generation")
        elif params["modelId"].startswith("mistral"):   output_response = response_body.get("outputs")[0].get("text")
        elif params["modelId"].startswith("cohere"):    output_response = response_body.get("generations")[0].get("text")
        elif params["modelId"].startswith("anthropic"): output_response = response_body.get("content")[0].get("text")
        else:                                           output_response = response_body
      else: 
        output_response = "lorem ipsum"

    
    except botocore.exceptions.ClientError as error:
      if error.response['Error']['Code'] == 'AccessDeniedException':
           print(f"\x1b[41m{error.response['Error']['Message']}\
            \nTo troubleshoot this issue please refer to the following resources.\
             \nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\
             \nhttps://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")
    
      else:
        if verbose: print(error)
        self.n.send_slack("I have got stuck in here. I am going to wait 30 seconds. And call myself again.")
        time.sleep(30)
        self.invoke_model(prompt)
        raise error

    except error:
      print(error.response['Error']['Message'])
      if verbose: print(error)
      self.n.send_slack("I have got stuck in here. I am going to wait 30 seconds. And call myself again.")
      time.sleep(30)
      self.invoke_model(prompt)
      raise error

    if verbose:
      print(output_response)

    return output_response

