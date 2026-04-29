from .base_agent import BaseAgent


class LogParserAgent(BaseAgent):
    """Agent 1: 解析异常日志，提取结构化信息"""
    
    def run(self, context: dict) -> dict:
        raw_log = context.get("raw_log", "")
        self.log("正在解析异常日志...")
        
        system_prompt = (
            "你是一名专业的日志分析专家。请从给定的异常堆栈中提取以下信息："
            "1. 错误类型；2. 涉事实体（类名/函数名）；3. 关键上下文片段。"
            "以 JSON 格式输出。"
        )
        result = self.api.chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": raw_log}
        ], temperature=self.config.get("temperature", 0.1))
        
        context["parsed_log"] = result
        self.log("日志解析完成")
        return context
