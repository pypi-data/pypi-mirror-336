import re

from openai import OpenAI

from ..base import VannaBase

class DeepSeekChat(VannaBase):
    def __init__(self, config=None):
        super().__init__(config)
        if config is None:
            raise ValueError(
                "For DeepSeek, config must be provided with an api_key and model"
            )
        if "api_key" not in config:
            raise ValueError("config must contain a DeepSeek api_key")

        if "model" not in config:
            raise ValueError("config must contain a DeepSeek model")
    
        self.api_key = config["api_key"]
        self.model = config["model"]
        self.temperature = config.get("temperature", 0.7)
        self.top_p = config.get("top_p", 0.95)
        self.max_retries = config.get("max_retries", 3)
        self.max_tokens = config.get("max_tokens", 4096)
        self.conversation_history = []
        
        # 根据环境配置不同的base_url
        base_url = config.get("base_url", "https://api.deepseek.com/v1")
        self.client = OpenAI(api_key=self.api_key, base_url=base_url)
        
    def system_message(self, message: str) -> any:
        return {"role": "system", "content": message}

    def user_message(self, message: str) -> any:
        return {"role": "user", "content": message}

    def assistant_message(self, message: str) -> any:
        return {"role": "assistant", "content": message}

    def generate_sql(self, question: str, **kwargs) -> str:
        # 构建系统提示词
        system_prompt = self.system_message(
            "你是一个专业的SQL专家，擅长将自然语言问题转换为准确的SQL查询语句。请仅返回SQL查询语句，不需要任何解释。生成的SQL语句应该遵循标准SQL语法，确保可以直接执行。在Ollama环境中运行时，请确保生成的SQL语句简洁明确。"
        )
        
        # 构建用户提示词
        user_prompt = self.user_message(
            f"请将以下问题转换为SQL查询语句，只需要返回SQL语句本身，不要包含任何其他说明。如果可能，请尽量使用标准SQL语法：\n{question}"
        )
        
        # 提交提示词获取响应
        response = self.submit_prompt([system_prompt, user_prompt], **kwargs)
        
        # 提取并优化SQL查询
        sql = self.extract_sql_query(response)
        sql = sql.replace("\_", "_")
        sql = sql.replace("\\", "")
        
        # 添加日志记录
        print(f"生成的SQL查询: {sql}")
        
        return sql
        
    def extract_sql_query(self, text: str) -> str:
        """从文本中提取SQL查询语句

        参数:
            text (str): 包含SQL查询的文本

        返回:
            str: 提取的SQL查询语句
        """
        # 尝试匹配SQL代码块
        sql_matches = re.findall(r'```sql\n(.+?)\n```', text, re.DOTALL)
        if sql_matches:
            return sql_matches[0].strip()

        # 尝试匹配普通代码块
        code_matches = re.findall(r'```\n(.+?)\n```', text, re.DOTALL)
        if code_matches:
            return code_matches[0].strip()

        # 尝试匹配SELECT语句
        select_matches = re.findall(r'\bSELECT\b.+?;', text, re.DOTALL)
        if select_matches:
            return select_matches[0].strip()

        # 如果都没有匹配到，返回原始文本
        return text.strip()

    def submit_prompt(self, prompt, **kwargs) -> str:
        if not isinstance(prompt, list):
            prompt = [prompt]
        
        # 添加对话历史
        messages = self.conversation_history + prompt
        
        # 检查token限制
        while len(str(messages)) > self.max_tokens and len(self.conversation_history) > 0:
            self.conversation_history.pop(0)
            messages = self.conversation_history + prompt
        
        for attempt in range(self.max_retries):
            try:
                # 根据base_url判断是否使用Ollama API
                base_url_str = str(self.client.base_url)
                if 'localhost:11434' in base_url_str:
                    # 使用Ollama API格式
                    import httpx
                    # 构建完整的提示词
                    full_prompt = "\n".join([msg['content'] for msg in messages])
                    response = httpx.post(
                        'http://localhost:11434/api/generate',
                        json={
                            'model': self.model,
                            'prompt': full_prompt,
                            'temperature': self.temperature,
                            'top_p': self.top_p,
                            'stream': False
                        },
                        timeout=30.0
                    )
                    response_json = response.json()
                    response_content = response_json.get('response', '')
                    if not response_content:
                        raise Exception('Ollama API返回的响应内容为空')
                    print(f'Ollama API响应内容: {response_content}')
                else:
                    # 使用标准OpenAI API格式
                    chat_response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        temperature=self.temperature,
                        top_p=self.top_p
                    )
                    response_content = chat_response.choices[0].message.content
                
                # 更新对话历史
                self.conversation_history.extend(prompt)
                self.conversation_history.append(self.assistant_message(response_content))
                
                return response_content
                
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                continue
