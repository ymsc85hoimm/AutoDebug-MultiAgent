from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseAgent(ABC):
    """Agent 基类，定义标准接口"""
    
    def __init__(self, name: str, api_client, config: Dict[str, Any]):
        self.name = name
        self.api = api_client
        self.config = config
    
    @abstractmethod
    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行 Agent 核心逻辑，返回更新后的上下文"""
        pass
    
    def log(self, msg: str):
        print(f"[{self.name}] {msg}")
