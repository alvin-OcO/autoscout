"""
自定义 action：save_to_json
需求：
    参数：data（字符串，搜索结果内容）、filename（字符串，默认 "result.json"）
    功能：把 data 保存为 JSON 文件（key 为 "result"）
    返回：ActionResult 告知保存成功
"""

# 导包
import json
from browser_use import Tools, ActionResult  
from pydantic import BaseModel, Field

# 创建 Tools 实例
tools = Tools()        

# 先定义 Pydantic 参数模型
class SaveToJsonParams(BaseModel):
    data: str = Field(description="要保存的搜索结果内容")
    filename: str = Field(default="result.json", description="保存的文件名")

# 用 @tools.registry.action() 注册
@tools.registry.action(
    '将搜索结果保存到JSON文件',
    param_model = SaveToJsonParams,
)
async def save_to_json(params: SaveToJsonParams):
   # 执行保存操作
    data_to_save = {"result": params.data}
    with open(params.filename, 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
    return ActionResult(extracted_content=f'已保存到 {params.filename}')  




