"""
autoscout.py - AI 竞品分析工具（CLI 模式）
用法：uv run autoscout.py "关键词" --top 5
"""
from browser_use import Agent
from browser_use.llm.messages import SystemMessage, UserMessage
from dotenv import load_dotenv
from deepseek_llm import ChatDeepSeekFixed
import asyncio, os, argparse, re
from pathlib import Path
from datetime import datetime

load_dotenv()

parser = argparse.ArgumentParser(description="AI 竞品分析工具")
parser.add_argument("keyword", help="搜索关键词")
parser.add_argument("--top", type=int, default=3, help="提取前N条结果（默认3）")
args = parser.parse_args()


async def main():
    llm = ChatDeepSeekFixed(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        add_schema_to_system_prompt=True,
        dont_force_structured_output=True,
    )

    searcher = Agent(
        task=f"搜索'{args.keyword}'，提取前 {args.top} 条结果的标题和摘要",
        llm=llm,
        use_judge=False,
    )

    try:
        history = await searcher.run()
        search_data = history.final_result()
    except Exception as e:
        print(f"❌ Agent 运行出错：{e}")
        return

    if search_data is None:
        print("❌ 搜索失败，未获取到结果")
        return

    messages = [
        SystemMessage(content="你是竞品分析师，基于搜索数据输出结构化对比报告"),
        UserMessage(content=f"以下是搜索结果：\n{search_data}\n\n请输出结构化对比报告"),
    ]
    response = await llm.ainvoke(messages)
    report = response.completion
    print(f"报告：\n{report}")

    # 保存报告
    safe_name = re.sub(r'[^\w\u4e00-\u9fff-]', '-', args.keyword)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{safe_name}-{date_str}.md"
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    file_path = reports_dir / filename
    file_path.write_text(report, encoding="utf-8")
    print(f"✅ 报告已保存到：{file_path}")


if __name__ == "__main__":
    asyncio.run(main())
