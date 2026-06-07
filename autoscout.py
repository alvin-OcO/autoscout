# 1. 导入：Agent, ChatDeepSeekFixed, 消息类, asyncio, os, dotenv
from browser_use import Agent
from browser_use.llm.messages import SystemMessage, UserMessage
from dotenv import load_dotenv
from deepseek_llm import ChatDeepSeekFixed
import asyncio, os, argparse, re
from pathlib import Path
from datetime import datetime

# 2. load_dotenv()
load_dotenv()
# main() 之前加参数解析逻辑
parser = argparse.ArgumentParser(description="竞品分析工具")

# 位置参数 = 必须按的按钮
parser.add_argument("keyword", help="搜索关键词")

# 可选参数 = 有默认值的旋钮，不动也行
parser.add_argument("--top", type=int, default=3, help="提取前N条结果")

args = parser.parse_args()
# 现在 args.keyword = 用户传的关键词
# 现在 args.top = 用户传的数量（或默认3）


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
    
    searcher = Agent(task=f"搜索'{args.keyword}'，提取前 {args.top} 条结果的标题和摘要", llm=llm, use_judge=False)
    try:
        history = await searcher.run()
        search_data = history.final_result()
    except Exception as e:
        print(f"❌ Agent 运行出错：{e}")
        return
    
    if search_data is None:
        print("❌ 搜索失败，未获取到结果")
        return  # ← 直接退出 main()，不继续分析

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
    # 构建文件名
    safe_name = re.sub(r'[^\w\u4e00-\u9fff-]', '-', args.keyword)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{safe_name}-{date_str}.md"

    #保存
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    file_path = reports_dir / filename
    file_path.write_text(report, encoding="utf-8")
    print(f"报告已保存到：{file_path}")



if __name__ == "__main__":
    asyncio.run(main())

