import nonebot
from nonebot.matcher import Matcher
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11 import GROUP_ADMIN, GROUP_OWNER
from nonebot import get_driver, on_command, on_message, logger

config = nonebot.get_driver().config
blacklist = get_driver().config.bot_blocklist


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


block = on_message(priority=0, block=False)


@block.handle()
async def _(event: Event, matcher: Matcher):
    if blacklist and event.get_user_id() in blacklist:
        logger.info("已忽略该指令")
        # await block.send("Error")
        matcher.stop_propagation()
