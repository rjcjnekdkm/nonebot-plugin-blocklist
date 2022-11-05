import json
import nonebot
from nonebot.matcher import Matcher
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11 import GROUP_ADMIN, GROUP_OWNER
from nonebot import get_driver, on_command, on_message, logger

config = nonebot.get_driver().config
try:
    blocklist = get_driver().config.bot_blocklist
    logger.info(f"已加载{len(blocklist)}个阻断用户")
except:
    blocklist = []
    logger.info("未读取到阻断名单，请检查env文件")


user_permission = on_command("测试权限")


@user_permission.handle()
async def _(bot: Bot, event: Event):
    msg = event.get_message()
    if str(msg) == "测试权限":
        if await GROUP_OWNER(bot, event):
            await user_permission.send("群主测试成功")
        elif await GROUP_ADMIN(bot, event):
            await user_permission.send("管理测试成功")
        else:
            await user_permission.send("群员测试成功")


block_msg = on_message(priority=0, block=False)


@block_msg.handle()
async def _(event: Event, matcher: Matcher):
    at = At(event.json())
    if at != []:
        for x in blocklist:
            if int(x) in at:
                logger.info("已忽略该条指令")
                matcher.stop_propagation()
    elif event.get_user_id() in blocklist:
        logger.info("已拦截该人指令")
        matcher.stop_propagation()


def At(data: str):
    """
    检测at了谁，返回[qq, qq, qq,...]
    包含全体成员直接返回['all']
    如果没有at任何人，返回[]
    :param data: event.json
    :return: list
    此部分来自@yzyyz1387的nonebot_plugin_admin，感谢
    """
    try:
        qq_list = []
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "at":
                if 'all' not in str(msg):
                    qq_list.append(int(msg["data"]["qq"]))
                else:
                    return ['all']
        return qq_list
    except KeyError:
        return []
