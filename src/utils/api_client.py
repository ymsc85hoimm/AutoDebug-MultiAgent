import requests
import yaml
from typing import List, Dict, Any


class CloudAPIClient:
    """统一封装云端 API 调用，支持长上下文与多轮对话"""
    
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)["api"]
        self.base_url = cfg["base_url"]
        self.api_key = cfg["api_key"]
        self.model = cfg["model"]
        self.max_tokens = cfg["max_tokens"]
    
    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
        """调用云端 ChatCompletion API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": self.max_tokens
        }
        try:
            resp = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=120
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[API Error] {str(e)}"
    
    def long_chain_reasoning(self, system_prompt: str, user_prompt: str, steps: int = 3) -> str:
        """长链推理：多步思考，逐步深化"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        reasoning_log = []
        for i in range(steps):
            content = self.chat(messages, temperature=0.2)
            reasoning_log.append(f"Step {i+1}: {content}")
            # 将上一步结果作为下一步的上下文
            messages.append({"role": "assistant", "content": content})
            messages.append({
                "role": "user",
                "content": f"基于以上分析，继续深入推理下一步（Step {i+2}）："
            })
        return "\n".join(reasoning_log)
