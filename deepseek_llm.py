"""
deepseek_llm.py
修复 DeepSeek 输出 markdown 代码块包裹的兼容性问题。
"""
import re
from browser_use import ChatOpenAI
from browser_use.llm.views import ChatInvokeCompletion

def _strip_markdown_json(text: str) -> str:
    """去掉 ```json ... ``` 包裹，返回裸 JSON 字符串。"""
    return re.sub(r'```(?:json)?\s*(.*?)\s*```', r'\1', text, flags=re.DOTALL)

class ChatDeepSeekFixed(ChatOpenAI):
    """修复 DeepSeek markdown 包裹问题的 ChatOpenAI 子类。"""

    async def ainvoke(self, messages, output_format=None, **kwargs):
        response = await super().ainvoke(messages, output_format=None, **kwargs)
        if output_format is None:
            # 不需要结构化输出 → 直接交给父类
            return response 
        raw_text = response.completion  # ← 从 completion 字段取字符串
        cleaned_text = _strip_markdown_json(raw_text)
        parsed_output = output_format.model_validate_json(cleaned_text)
        return ChatInvokeCompletion(
            completion=parsed_output,
            usage=response.usage,       # ← 传递 token 用量
            stop_reason=response.stop_reason,
            )