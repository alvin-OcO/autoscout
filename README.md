# 🔍 AutoScout

> 基于 browser-use + DeepSeek 的 AI 竞品分析工具，一行命令自动搜索、提取、生成结构化分析报告。

## ✨ 亮点

- **国产模型适配**：通过子类继承 + regex 清洗，解决 DeepSeek 不支持 OpenAI 结构化输出的兼容问题
- **轻重分离架构**：浏览器 Agent 负责搜索采集，纯 LLM 调用负责分析，避免过度工程
- **一行命令即用**：`argparse` 参数化 + Markdown 报告自动持久化

## 🏗️ 架构

```
用户输入关键词
    │
    ▼
┌─────────────┐     ┌─────────────┐
│ Searcher    │ ──→ │ Analyzer    │ ──→ 报告.md
│(browser-use)│     │ (纯LLM调用)  │
└─────────────┘     └─────────────┘
```

## 🚀 快速开始

```bash
# 安装依赖
uv sync

# 配置 API Key
echo "DEEPSEEK_API_KEY=你的key" > .env

# 运行
uv run autoscout.py "React vs Vue 前端框架对比"
uv run autoscout.py "Python vs Go" --top 5
```

## 📂 项目结构

```
├── autoscout.py       # 主程序：CLI + 流水线编排
├── deepseek_llm.py    # DeepSeek 适配层
├── orchestrator.py    # 多 Agent 编排原型
├── first_agent.py     # 单 Agent 基础示例
├── custom_actions.py  # 自定义 Action 示例
└── reports/           # 生成的分析报告
```
