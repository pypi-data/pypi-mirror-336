from .chromadb.chromadb_vector import ChromaDB_VectorStore
from .openai.openai_chat import OpenAI_Chat


class LocalContext_OpenAI(ChromaDB_VectorStore, OpenAI_Chat):
    """
    LocalContext_OpenAI 类
    
    这个类继承自 ChromaDB_VectorStore 和 OpenAI_Chat，用于在本地环境中结合 ChromaDB 向量存储和 OpenAI 聊天功能。
    它提供了一个本地化的上下文处理解决方案，可以同时利用 ChromaDB 的向量存储能力和 OpenAI 的对话能力。
    
    属性:
        无特有属性，继承自父类的所有属性
    """
    
    def __init__(self, config=None):
        """
        初始化 LocalContext_OpenAI 实例
        
        参数:
            config (dict, 可选): 配置字典，包含初始化所需的配置参数
                                如果为 None，则使用默认配置
        
        示例:
            >>> local_context = LocalContext_OpenAI(config={"api_key": "your-api-key"})
        """
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)
