import botpy
import os
import view

from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, Message
from plugins.commands import *

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
_log = logging.get_logger()

COMMAND = f"""
{Commands.help}
{Commands.CF_recent_ac} <cf用户名称> <查询提交个数>
{Commands.AT_random_problem_by_index} <选择场次: (abc, arc)> <序号: (A,B,C,D,E,F,G)> <at用户名称> <是否可以抽已经ac的题: (0,1)>
"""

CANNOT_FIND_RESPONSE = f"""找不到对应指令哦。
以下为可用指令：
{COMMAND}
"""

HELP_RESPONSE = f"""我还没有对接 GPT 哦，请输入以 '/' 开头的指令。
以下为可用指令：
{COMMAND}
"""


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    @staticmethod
    async def _api_config(content_list: list[str]):
        response: str = ''
        # 配置命令映射
        if content_list[0].startswith('/'):
            if content_list[0] == Commands.CF_recent_ac:
                response += (await view.user_cf_ac_problems(content_list)).unwrap()
            elif content_list[0] == Commands.AT_random_problem_by_index:
                response += (await view.at_random_problem_by_index(content_list)).unwrap()
            elif content_list[0] == Commands.help:
                response += f"以下为可用指令：\n{COMMAND}\n"
            else:
                response += CANNOT_FIND_RESPONSE
        else:
            response += HELP_RESPONSE
        return response

    @staticmethod
    async def on_at_message_create(message: Message):
        # 获取命令
        content_list: list[str] = message.content.lstrip(" ").split()
        content_list = content_list[1:]  # 第一个是一个莫名其妙的对象

        response: str = await MyClient._api_config(content_list)

        # 机器人回复
        await message.reply(content=response)
        _log.info(f"成功返回了 {message.author.username} 的消息")

    async def on_group_at_message_create(self, message: GroupMessage):
        # 获取命令
        content_list: list[str] = message.content.lstrip(" ").split()

        response: str = '\n'
        response += await MyClient._api_config(content_list)

        # 机器人回复
        await self.api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            content=response)
        _log.info(f"成功返回了 {message.content} 消息")


if __name__ == "__main__":
    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True, public_messages=True)
    client = MyClient(intents=intents, is_sandbox=True)
    client.run(appid=test_config["appid"], secret=test_config["secret"])
