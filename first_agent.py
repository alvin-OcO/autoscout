from browser_use import Agent, ChatOpenAI
from deepseek_llm import ChatDeepSeekFixed
from dotenv import load_dotenv
import asyncio
import os
from custom_actions import tools  # ← 导入已经注册了 save_to_json 的 tools


load_dotenv()

async def main():
    llm = ChatDeepSeekFixed(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        add_schema_to_system_prompt=True,    # ← 新增
        dont_force_structured_output=True,   # ← 新增
    )
    
    agent = Agent(
        task="搜索 qoder，找到第一条结果的标题后，将结果保存到 JSON 文件中",
        llm=llm,
        tools=tools,        # ← 传进去
        use_judge=False,
    )

    result = await agent.run()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())