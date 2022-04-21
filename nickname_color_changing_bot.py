""" A discord bot that can be used to change nickname color """

from functools import reduce
import discord
import os
import re

intents = discord.Intents(messages=True,
                          guilds=True,
                          reactions=True,
                          members=True)
client = discord.Client(intents=intents)

COMMAND_PATTERN = '!color '


def convert_rgb_to_discord_color(rgb_str: str) -> discord.Color:
    r, g, b = map(int, rgb_str.replace('rgb(', '').replace(')', '').split(','))
    return discord.Color.from_rgb(r, g, b)


SUPPORTED_COLOR_PATTERN = [{
    'regexp':
    r'^#[0-9A-Fa-f]{6}$',
    'example':
    '#AABBCC',
    'convert_fn':
    lambda x: discord.Color(int(x[1:], 16))
}, {
    'regexp': r'^rgb\(\d{1,3},\d{1,3},\d{1,3}\)$',
    'example': 'rgb(25,25,25)',
    'convert_fn': convert_rgb_to_discord_color
}]
SUPPORTED_COLOR_PATTERN_EXAMPLE = reduce(
    lambda x, y: x + '\t' + y,
    [pattern['example'] for pattern in SUPPORTED_COLOR_PATTERN])


def is_valid_commend(message: discord.Message) -> bool:
    content = message.content
    return content.startswith(COMMAND_PATTERN) and len(content.split(' ')) == 2


def parse_message(message: discord.Message) -> discord.Color or None:
    color_str = message.content.split(' ')[1]
    for pattern in SUPPORTED_COLOR_PATTERN:
        if re.match(pattern['regexp'], color_str):
            return pattern['convert_fn'](color_str)
    return None


@client.event
async def on_message(message: discord.Message):
    author: discord.Member = message.author
    if not author or not author.id or author == client.user\
        or not is_valid_commend(
            message):
        return

    color = parse_message(message)
    if color is None:
        await message.channel.send('色碼不符合格式\n目前支援的格式為\n' +
                                   SUPPORTED_COLOR_PATTERN_EXAMPLE)
        return

    role_name = f'{author.id}'
    existed_role = next((x for x in author.roles if x.name == role_name), None)
    if existed_role:
        await existed_role.edit(colour=color)
    else:
        created_role = await message.author.guild.create_role(name=role_name,
                                                              color=color)
        await message.author.add_roles(created_role)
    await message.add_reaction('👌')


client.run(os.getenv('NICKNAME_COLOR_CHANGING_BOT_TOKEN'))
