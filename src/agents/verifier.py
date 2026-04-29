from .base_agent import BaseAgent


class VerifierAgent(BaseAgent):
    """Agent 4: 验证修复结果（模拟）"""
    
    def run(self, context: dict) -> dict:
        patch = context.get("patch", "")
        self.log("正在验证补丁...")
        
        # 实际场景中这里会执行单元测试
        # 此处通过 API 进行静态验证
        system_prompt = (
            "你是一名测试工程师。请审查以下代码补丁，判断："
            "1. 是否引入了新的语法错误；2. 是否可能破坏原有逻辑。"
            "如果存在问题，请指出并返回 'FAIL'；否则返回 'PASS'。"
        )
        result = self.api.chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": patch}
        ], temperature=self.config.get("temperature", 0.0))
        
        context["verify_result"] = result
        is_pass = "PASS" in result.upper()
        context["status"] = "success" if is_pass else "retry"
        self.log(f"验证结果: {'通过' if is_pass else '失败，准备回流'}")
        return context
