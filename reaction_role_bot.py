""" A discord bot that can be used to change user role by reaction """

import discord
import os

intents = discord.Intents(messages=True,
                          guilds=True,
                          reactions=True,
                          members=True)
client = discord.Client(intents=intents)


def get_member_and_role_from_payload(payload):
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
    role = discord.utils.get(guild.roles, name=payload.emoji.name)
    member = discord.utils.find(lambda m: m.id == payload.user_id,
                                guild.members)
    return member, role


@client.event
async def on_raw_reaction_add(payload):
    member, role = get_member_and_role_from_payload(payload)
    await member.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):
    member, role = get_member_and_role_from_payload(payload)
    await member.remove_roles(role)


client.run(os.getenv('TOKEN'))
