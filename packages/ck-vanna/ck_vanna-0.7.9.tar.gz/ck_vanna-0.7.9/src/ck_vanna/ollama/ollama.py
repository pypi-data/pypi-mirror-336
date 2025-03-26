import json
import re

from httpx import Timeout

from ..base import VannaBase
from ..exceptions import DependencyError


class Ollama(VannaBase):
  def __init__(self, config=None):

    try:
      ollama = __import__("ollama")
    except ImportError:
      raise DependencyError(
        "You need to install required dependencies to execute this method, run command:"
        " \npip install ollama"
      )

    if not config:
      raise ValueError("config must contain at least Ollama model")
    if 'model' not in config.keys():
      raise ValueError("config must contain at least Ollama model")
    self.host = config.get("ollama_host", "http://localhost:11434")
    self.model = config["model"]
    if ":" not in self.model:
      self.model += ":latest"

    self.ollama_timeout = config.get("ollama_timeout", 240.0)

    self.ollama_client = ollama.Client(self.host, timeout=Timeout(self.ollama_timeout))
    self.keep_alive = config.get('keep_alive', None)
    self.ollama_options = config.get('options', {})
    self.num_ctx = self.ollama_options.get('num_ctx', 2048)
    self.__pull_model_if_ne(self.ollama_client, self.model)

  @staticmethod
  def __pull_model_if_ne(ollama_client, model):
    model_response = ollama_client.list()
    model_lists = [model_element['model'] for model_element in
                   model_response.get('models', [])]
    if model not in model_lists:
      ollama_client.pull(model)

  def system_message(self, message: str) -> any:
    return {"role": "system", "content": message}

  def user_message(self, message: str) -> any:
    return {"role": "user", "content": message}

  def assistant_message(self, message: str) -> any:
    return {"role": "assistant", "content": message}

  def extract_sql(self, llm_response):
    """
    Extracts the first SQL statement after the word 'select', ignoring case,
    matches until the first semicolon, three backticks, or the end of the string,
    and removes three backticks if they exist in the extracted string.

    Args:
    - llm_response (str): The string to search within for an SQL statement.

    Returns:
    - str: The first SQL statement found, with three backticks removed, or an empty string if no match is found.
    """
    # Remove ollama-generated extra characters
    llm_response = llm_response.replace("\_", "_")
    llm_response = llm_response.replace("\\", "")
    
    # Regular expression to find ```sql' and capture until '```'
    sql = re.search(r"```(?:sql)?\s*\n?([\s\S]*?)(?=\n?```|;|\[|$)", llm_response, re.IGNORECASE)
    # Regular expression to find 'select, with (ignoring case) and capture until ';', [ or end of string
    select_with = re.search(r'(?:select|with\s+\w+\s+as\s*\()([\s\S]*?)(?=;|\[|$)',
                                llm_response,
                                re.IGNORECASE)
    
    self.log(f"Processing LLM Response:\n{llm_response}")
    
    if sql:
        extracted_sql = sql.group(1).strip()
        self.log(f"Extracted SQL from code block:\n{extracted_sql}")
        return extracted_sql
    elif select_with:
        extracted_sql = select_with.group(0).strip()
        self.log(f"Extracted SQL from direct query:\n{extracted_sql}")
        return extracted_sql
    else:
        self.log("No SQL query found in the response")
        return llm_response

  def submit_prompt(self, prompt, **kwargs) -> str:
    self.log(
      f"Ollama parameters:\n"
      f"model={self.model},\n"
      f"options={self.ollama_options},\n"
      f"keep_alive={self.keep_alive}")
    self.log(f"Prompt Content:\n{json.dumps(prompt, ensure_ascii=False)}")
    response_dict = self.ollama_client.chat(model=self.model,
                                            messages=prompt,
                                            stream=False,
                                            options=self.ollama_options,
                                            keep_alive=self.keep_alive)

    self.log(f"Ollama Response:\n{str(response_dict)}")

    return response_dict['message']['content']
