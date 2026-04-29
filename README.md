# AutoDebug-MultiAgent

基于云端大模型 API 的多 Agent 协作自动化调试系统。

## 核心架构

- **Orchestrator**: 中央调度器，维护全局状态与 Agent 间消息总线
- **LogParser Agent**: 异常日志结构化解析
- **RootCause Agent**: 长链推理根因定位（Chain-of-Thought）
- **FixGen Agent**: 修复补丁生成
- **Verify Agent**: 补丁验证与测试回归

## 快速开始

```bash
pip install -r requirements.txt
# 配置 config.yaml 中的 api_key 与 base_url
python demo.py
