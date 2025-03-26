from nonebot_plugin_alconna import on_alconna
from nonebot import get_plugin_config
from nonebot_plugin_alconna.builtins.extensions.reply import ReplyRecordExtension
from nonebot.internal.adapter import Event
from nonebot_plugin_alconna.uniseg import Reply, UniMessage, Text, MsgId, Image
from .api import AsyncChatClient
from .config import Config
from pathlib import Path
from PIL import Image as PILImage
from io import BytesIO
from .browser import get_browser
import httpx
import base64
from loguru import logger
import random
import re
import ssl

system_prompt_raw = (
    Path(__file__).parent.joinpath("prompt.txt").read_text(encoding="utf-8")
)
config = get_plugin_config(Config)

zssm = on_alconna("zssm", extensions=[ReplyRecordExtension()])


async def url_to_base64(url: str) -> str:
    ssl_context = ssl.create_default_context()
    ssl_context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_3
    ssl_context.set_ciphers("HIGH:!aNULL:!MD5")
    async with httpx.AsyncClient(verify=ssl_context) as client:
        response = await client.get(url)
        image = PILImage.open(BytesIO(response.content))
        # 把图片控制在5mb以内
        if len(response.content) > 5 * 1024 * 1024:
            image.thumbnail((4096, 4096))
        if image.mode != "RGB":
            image = image.convert("RGB")
        buffered = BytesIO()
        image.save(buffered, format="JPEG", quality=80)
        b64_content = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/jpeg;base64,{b64_content}"


@zssm.handle()
async def handle(msg_id: MsgId, ext: ReplyRecordExtension, event: Event):
    msg = event.get_message()
    if reply := ext.get_reply(msg_id):
        reply_msg_raw = reply.msg
    else:
        return await UniMessage(Text("未找到上一条消息")).send(reply_to=Reply(msg_id))

    if not reply.msg:
        return await UniMessage(Text("上一条消息内容为空")).send(reply_to=Reply(msg_id))

    if not config.zssm_ai_text_token or not config.zssm_ai_vl_token:
        return await UniMessage(Text("未配置 Api Key，暂时无法使用")).send(
            reply_to=Reply(msg_id)
        )

    if isinstance(reply_msg_raw, str):
        reply_msg_raw = msg.__class__(reply_msg_raw)

    reply_msg = UniMessage.generate_sync(message=reply_msg_raw)
    image_list = reply_msg.get(Image)
    reply_msg_display = ""
    for item in reply_msg:
        if isinstance(item, Image):
            reply_msg_display += f"[图片 {item.id}]"
        else:
            reply_msg_display += str(item)

    random_number = str(random.randint(10000000, 99999999))
    system_prompt = system_prompt_raw + random_number
    user_prompt = f"<random number: {random_number}> \n<type: text>\n{reply_msg_display}\n</type: text>\n"

    for image in image_list:
        image: Image
        image_url = image.url
        if not image_url:
            continue
        async with AsyncChatClient(
            config.zssm_ai_vl_endpoint, config.zssm_ai_vl_token
        ) as client:
            logger.info(f"image_url: {image_url}")
            response = await client.create(
                config.zssm_ai_vl_model,
                [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {"url": await url_to_base64(image_url)},
                            },
                            {"type": "text", "text": "请描述这张图片"},
                        ],
                    },
                ],
            )
            image_prompt = response.json()["choices"][0]["message"]["content"]
            user_prompt += (
                f"<type: image, id: {image.id}>\n{image_prompt}\n</type: image>\n"
            )

    reg_match = re.compile(
        r"\b(?:https?|ftp):\/\/[^\s\/?#]+[^\s]*|\b(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})*(?:\/[^\s]*)?\b"
    )
    msg_url_list = reg_match.findall(str(reply_msg))
    if msg_url_list:
        browser = await get_browser(
            proxy={"server": config.zssm_browser_proxy}
            if config.zssm_browser_proxy
            else None
        )
        msg_url = msg_url_list[0]
        logger.info(f"msg_url: {msg_url}")
        await UniMessage(Text("正在尝试打开消息中的第一条链接")).send(
            reply_to=Reply(msg_id)
        )
        page = await browser.new_page()
        try:
            await page.goto(msg_url, timeout=60000)
        except Exception:
            return await UniMessage(Text("打开链接失败")).send(reply_to=Reply(msg_id))
        # 获取页面的内容
        page_content = await page.query_selector("html")
        if page_content:
            page_content = await page_content.inner_text()
            user_prompt += (
                f"<type: web_page, url: {msg_url}>\n{page_content}\n</type: web_page>\n"
            )
        await page.close()
        if not page_content:
            return await UniMessage(Text("无法获取页面内容")).send(
                reply_to=Reply(msg_id)
            )

    user_prompt += f"</random number: {random_number}>\n"
    logger.info(f"user_prompt: \n{user_prompt}")
    async with AsyncChatClient(
        config.zssm_ai_text_endpoint, config.zssm_ai_text_token
    ) as client:
        response = await client.create(
            config.zssm_ai_text_model,
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        logger.info(response.json())

    await UniMessage(Text(response.json()["choices"][0]["message"]["content"])).send(
        reply_to=Reply(msg_id)
    )
