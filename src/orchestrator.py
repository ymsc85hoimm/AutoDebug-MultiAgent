from typing import Dict, Any
from .agents import LogParserAgent, RootCauseAgent, FixGenAgent, VerifierAgent
from .utils.api_client import CloudAPIClient


class DebugOrchestrator:
    """
    中央调度器：管理多 Agent 协作流水线
    支持失败回流（Retry Loop）与上下文共享
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        self.api = CloudAPIClient(config_path)
        # 加载配置
        import yaml
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        
        self.agents = {
            "parser": LogParserAgent("LogParser", self.api, cfg["agents"]["log_parser"]),
            "root_cause": RootCauseAgent("RootCause", self.api, cfg["agents"]["root_cause"]),
            "fix_gen": FixGenAgent("FixGen", self.api, cfg["agents"]["fix_gen"]),
            "verifier": VerifierAgent("Verifier", self.api, cfg["agents"]["verifier"]),
        }
        self.max_retries = 2
    
    def run(self, raw_log: str, codebase: str) -> Dict[str, Any]:
        context = {
            "raw_log": raw_log,
            "codebase_snippet": codebase,
            "status": "pending"
        }
        
        # Stage 1: 日志解析
        context = self.agents["parser"].run(context)
        
        # Stage 2: 根因定位（长链推理）
        context = self.agents["root_cause"].run(context)
        
        for attempt in range(self.max_retries + 1):
            # Stage 3: 补丁生成
            context = self.agents["fix_gen"].run(context)
            
            # Stage 4: 验证
            context = self.agents["verifier"].run(context)
            
            if context["status"] == "success":
                print("\n[Orchestrator] 调试流水线完成，补丁已验证通过")
                break
            else:
                print(f"\n[Orchestrator] 第 {attempt+1} 次验证失败，回流至根因分析...")
                # 将验证错误信息加入上下文，重新生成
                context["parsed_log"] += f"\n[验证反馈] {context['verify_result']}"
                context = self.agents["root_cause"].run(context)
        else:
            print("\n[Orchestrator] 达到最大重试次数，调试失败")
        
        return context
