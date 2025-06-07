# tools/web_fetch.py

import markdownify
import readabilipy.simple_json
from typing import Annotated, Tuple
from mcp.shared.exceptions import McpError
from mcp.types import TextContent, ErrorData, INVALID_PARAMS, INTERNAL_ERROR
from pydantic import BaseModel, Field, AnyUrl

# 默认用户代理字符串
DEFAULT_USER_AGENT = "ModelContextProtocol/1.0 (User-Specified; +https://github.com/modelcontextprotocol/servers)"


def extract_content_from_html(html: str) -> str:
    """从HTML内容中提取并转换为Markdown格式

    Args:
        html: 要处理的原始HTML内容

    Returns:
        内容的简化markdown版本
    """
    ret = readabilipy.simple_json.simple_json_from_html_string(
        html, use_readability=True
    )
    if not ret["content"]:
        return "<error>页面无法从HTML简化</error>"
    content = markdownify.markdownify(
        ret["content"],
        heading_style=markdownify.ATX,
    )
    return content



async def fetch_url(
    url: str, user_agent: str, force_raw: bool = False, proxy_url: str | None = None
) -> Tuple[str, str]:
    """
    获取URL并返回为LLM准备的内容形式，以及带有状态信息的前缀字符串。
    """
    from httpx import AsyncClient, HTTPError

    # 创建客户端，如果有代理则设置代理
    client_kwargs = {}
    if proxy_url:
        client_kwargs["proxies"] = proxy_url
    
    async with AsyncClient(**client_kwargs) as client:
        try:
            response = await client.get(
                url,
                follow_redirects=True,
                headers={"User-Agent": user_agent},
                timeout=30,
            )
        except HTTPError as e:
            raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"获取{url}失败: {e!r}"))
        if response.status_code >= 400:
            raise McpError(ErrorData(
                code=INTERNAL_ERROR,
                message=f"获取{url}失败 - 状态码{response.status_code}",
            ))

        page_raw = response.text

    content_type = response.headers.get("content-type", "")
    is_page_html = (
        "<html" in page_raw[:100] or "text/html" in content_type or not content_type
    )

    if is_page_html and not force_raw:
        return extract_content_from_html(page_raw), ""

    return (
        page_raw,
        f"内容类型{content_type}无法简化为markdown，但这里是原始内容:\n",
    )


class Fetch(BaseModel):
    """获取URL的参数"""

    url: Annotated[AnyUrl, Field(description="要获取的URL")]
    max_length: Annotated[
        int,
        Field(
            default=5000,
            description="返回的最大字符数",
            gt=0,
            lt=1000000,
        ),
    ]
    start_index: Annotated[
        int,
        Field(
            default=0,
            description="从此字符索引开始返回输出，如果之前的获取被截断且需要更多上下文时很有用",
            ge=0,
        ),
    ]
    raw: Annotated[
        bool,
        Field(
            default=False,
            description="获取请求页面的实际HTML内容，不进行简化",
        ),
    ]


async def _fetch_web_content(arguments: dict) -> list[TextContent]:
    """网页内容获取工具的MCP接口"""
    
    try:
        args = Fetch(**arguments)
    except ValueError as e:
        return [TextContent(type="text", text=f"❌ 参数错误: {str(e)}")]

    url = str(args.url)
    if not url:
        return [TextContent(type="text", text="❌ 错误：URL不能为空")]

    try:
        # 使用默认用户代理，忽略robots.txt限制
        user_agent = DEFAULT_USER_AGENT
        
        content, prefix = await fetch_url(
            url, user_agent, force_raw=args.raw, proxy_url=None
        )
        
        original_length = len(content)
        if args.start_index >= original_length:
            content = "<error>没有更多可用内容</error>"
        else:
            truncated_content = content[args.start_index : args.start_index + args.max_length]
            if not truncated_content:
                content = "<error>没有更多可用内容</error>"
            else:
                content = truncated_content
                actual_content_length = len(truncated_content)
                remaining_content = original_length - (args.start_index + actual_content_length)
                
                # 只有在仍有剩余内容时才添加继续获取的提示
                if actual_content_length == args.max_length and remaining_content > 0:
                    next_start = args.start_index + actual_content_length
                    content += f"\n\n<error>内容被截断。使用start_index为{next_start}调用fetch工具以获取更多内容</error>"
        
        return [TextContent(type="text", text=f"✅ {prefix}{url}的内容:\n{content}")]
        
    except McpError as e:
        return [TextContent(type="text", text=f"❌ 获取失败: {e.data.message}")]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 获取失败: {str(e)}")]