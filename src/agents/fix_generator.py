from .base_agent import BaseAgent


class FixGenAgent(BaseAgent):
    """Agent 3: 基于根因生成修复补丁"""
    
    def run(self, context: dict) -> dict:
        root_cause = context.get("root_cause", "")
        self.log("正在生成修复补丁...")
        
        system_prompt = (
            "你是一名高级开发工程师。请根据根因分析结果，生成一个符合 PEP8 规范的 Python 修复补丁。"
            "输出格式：```diff ... ```"
        )
        result = self.api.chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": root_cause}
        ], temperature=self.config.get("temperature", 0.3))
        
        context["patch"] = result
        self.log("补丁生成完成")
        return context
