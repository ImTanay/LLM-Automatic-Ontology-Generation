import openai
import time

class GPTWrapper:
    """
    A wrapper class for interacting with the GPT models.
    Args:
        api_key (str): The API key for accessing the OpenAI GPT models.
        model (str, optional): The GPT model to use. Defaults to "gpt-3.5-turbo-instruct".
    Attributes:
        api_key (str): The API key for accessing the OpenAI GPT models.
        model (str): The GPT model to use.
    Methods:
        prepare_prompt(prompt: str) -> dict:
            Prepares the prompt for invoking the GPT model.
        invoke_model(prompt: str, model: str = "gpt3", verbose: bool = False, test: bool = False) -> str:
            Invokes the GPT model with the given prompt.
    """
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo-instruct"):
        """
        Initializes the GPTWrapper object.
        Args:
            api_key (str): The API key for accessing the OpenAI GPT models.
            model (str, optional): The GPT model to use. Defaults to "gpt-3.5-turbo-instruct".
        """
    def prepare_prompt(self, prompt: str) -> dict:
        """
        Prepares the prompt for invoking the GPT model.
        Args:
            prompt (str): The prompt to be used for generating the response.
        Returns:
            dict: A dictionary containing the prepared prompt with additional parameters.
        """
    def invoke_model(self, prompt: str, model: str = "gpt3", verbose: bool = False, test: bool = False) -> str:
        """
        Invokes the GPT model with the given prompt.
        Args:
            prompt (str): The prompt to be used for generating the response.
            model (str, optional): The GPT model to use. Defaults to "gpt3".
            verbose (bool, optional): Whether to print additional information. Defaults to False.
            test (bool, optional): Whether to simulate a test scenario. Defaults to False.
        Returns:
            str: The generated response from the GPT model.
        """

    def __init__(self, api_key:str, model:str="gpt-3.5-turbo-instruct"):
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key

    def prepare_prompt(self, prompt:str)->dict:
        return {"prompt": prompt, "max_tokens": 2048, "temperature": 0.1}

    def invoke_model(self, prompt:str, model:str="gpt3", verbose:bool=False, test:bool=False):
        output_response = ""
        
        try:
            if verbose: 
                print("Model code: ", self.model)
                print("PROMPT: ", prompt)
            
            params = self.prepare_prompt(prompt)
            
            if model == "gpt3":
                if not test:
                    # Invoke GPT-3 model
                    response = openai.completions.create(
                        model = self.model,
                        prompt=params['prompt'],
                        max_tokens=params['max_tokens'],
                        temperature=params['temperature']
                    )
                    
                    output_response = response.choices[0].text.strip()
                    
                else: 
                    output_response = "GPT API is not working"
            
            elif model == "gpt4":
                if not test:
                    # Invoke GPT-4 model
                    response = openai.chat.completions.create(
                        model=self.model,
                        messages=[
                            {
                                "role": "assistant",
                                "content": params['prompt'],
                            },
                        ],
                        max_tokens=params['max_tokens']
                    )
                    
                    output_response = response.choices[0].message.content.strip()
                 
                else: 
                    output_response = "lorem ipsum"
    
        except Exception as error:
            print(error)
            if verbose: 
                print(error)
                print("Experiment Stuck. Retry in 30 seconds")
            time.sleep(30)
            self.invoke_model(prompt, model, verbose, test)
            raise error

        if verbose:
            print(output_response)

        return output_response
