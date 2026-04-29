from .base_agent import BaseAgent


class RootCauseAgent(BaseAgent):
    """Agent 2: 长链推理定位根因"""
    
    def run(self, context: dict) -> dict:
        parsed = context.get("parsed_log", "")
        codebase = context.get("codebase_snippet", "")
        self.log("启动长链推理根因定位...")
        
        system_prompt = (
            "你是一名资深软件架构师，擅长通过长链推理定位复杂 Bug 的根因。"
            "请遵循以下推理链："
            "Step 1 - 假设：根据错误日志提出 3 个可能的根因假设；"
            "Step 2 - 验证：结合代码片段逐一验证每个假设；"
            "Step 3 - 结论：给出最可能的根因文件、行号与具体原因。"
        )
        user_prompt = f"【错误日志】\n{parsed}\n\n【相关代码】\n{codebase}"
        
        # 使用长链推理接口，消耗大量 Token
        result = self.api.long_chain_reasoning(
            system_prompt, user_prompt, steps=3
        )
        
        context["root_cause"] = result
        self.log("根因定位完成")
        return context
