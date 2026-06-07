"""
app.py - AI 竞品分析工具（Web UI 模式）
用法：uv run app.py → 浏览器打开 http://127.0.0.1:7860
"""
import gradio as gr
import asyncio, os, re
from pathlib import Path
from datetime import datetime
from browser_use import Agent
from browser_use.llm.messages import SystemMessage, UserMessage
from deepseek_llm import ChatDeepSeekFixed
from dotenv import load_dotenv

load_dotenv()


async def analyze(keyword: str, top_n: int) -> str:
    """搜索 + 分析 → 返回报告文本，同时保存为 Markdown 文件"""
    llm = ChatDeepSeekFixed(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        add_schema_to_system_prompt=True,
        dont_force_structured_output=True,
    )

    searcher = Agent(
        task=f"搜索'{keyword}'，提取前{top_n}条结果的标题和摘要",
        llm=llm,
        use_judge=False,
    )
    history = await searcher.run()
    search_data = history.final_result()

    if search_data is None:
        return "❌ 搜索失败，未获取到结果"

    messages = [
        SystemMessage(content="你是竞品分析师，基于搜索数据输出结构化对比报告"),
        UserMessage(content=f"以下是搜索结果：\n{search_data}\n\n请输出结构化对比报告"),
    ]
    response = await llm.ainvoke(messages)
    report = response.completion

    # 保存报告
    safe_name = re.sub(r'[^\w\u4e00-\u9fff-]', '-', keyword)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{safe_name}_{date_str}.md"
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    (reports_dir / filename).write_text(report, encoding="utf-8")

    return report


def run_analyze(keyword, top_n):
    """同步桥接：Gradio 回调 → async analyze"""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(analyze(keyword, int(top_n)))
    finally:
        loop.close()


gr.Interface(
    fn=run_analyze,
    inputs=[
        gr.Textbox(label="搜索关键词", placeholder="如：React vs Vue"),
        gr.Number(label="提取结果数", value=3),
    ],
    outputs=gr.Markdown(label="分析报告"),
    title="🔍 AutoScout - AI 竞品分析",
    description="输入关键词，自动搜索并生成结构化竞品分析报告",
).launch()
