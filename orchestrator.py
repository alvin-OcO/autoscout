# 1. 导入：Agent, ChatDeepSeekFixed, 消息类, asyncio, os, dotenv
from browser_use import Agent
from browser_use.llm.messages import SystemMessage, UserMessage
from dotenv import load_dotenv
from deepseek_llm import ChatDeepSeekFixed
import asyncio, os

# 2. load_dotenv()
load_dotenv()

# 3. async def main():
async def main():
    #      a. 创建 llm 实例
    llm = ChatDeepSeekFixed(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        add_schema_to_system_prompt=True,    # ← 新增
        dont_force_structured_output=True,   # ← 新增
    )
    #      b. 创建 Searcher Agent（task=搜索任务, llm=llm, use_judge=False）
    searcher = Agent(task="搜索'browser-use vs playwright 自动化对比'，提取前 3 条结果的标题和摘要", llm=llm, use_judge=False)
    history = await searcher.run()
    search_data = history.final_result()

    #      e. 构造 messages 列表（system + user）
    messages = [
        SystemMessage(content="你是竞品分析师，基于搜索数据输出结构化对比报告"),
        UserMessage(content=f"以下是搜索结果：\n{search_data}\n\n请输出结构化对比报告"),
    ]
    #      f. response = await llm.ainvoke(messages)
    response = await llm.ainvoke(messages)
    #      g. report = response.completion
    report = response.completion
    #      h. print(report)
    print(f"报告：\n{report}")

if __name__ == "__main__":
    asyncio.run(main())

