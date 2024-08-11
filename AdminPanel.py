import discord
import requests
import json
from discord import File
from discord.ext import commands
import random
import vk_api
import io
import datetime
from SQLMetod import SQL
import asyncio
from config import *
from bs4 import BeautifulSoup
from utilites import DungeonParty, ban_check, AdminCheck

connection = SQL("localhost", "Bot", "Bot_Python")

vk = vk_api.VkApi(token=vk_token)


User_functional = """
Ты пока нихуя не можешь иди нахуй
"""
Admin_functional = """
1️⃣ - Список всех текстовых каналов
2️⃣ - Список всех голосовых каналов
3️⃣ - Чёта будет
"""

Admin_reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "⛔"]
User_reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "⛔"]

message_panel = []


async def get_message(bot, reaction):
    guild = bot.get_guild(reaction.guild_id)
    channel = guild.get_channel(reaction.channel_id)
    message = await channel.fetch_message(reaction.message_id)
    return message


class AdminPanel(commands.Cog):
    """COMMAND FOR ALL"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="apanel")
    async def _Apanel(self, ctx):
        Guild = self.bot.get_guild(ctx.guild.id)
        panel_info = f"Guild: {Guild}\n" \
                     f"User: {ctx.author}\n" \
                     f"Bot Permission: {'Admin' if ctx.author.id in connection.get_admin_list() else 'User'}\n"
        embed = discord.Embed(color=0xff9900,
                              description=f"{Admin_functional if ctx.author.id in connection.get_admin_list() else User_functional}",
                              title=panel_info)
        message = await ctx.send(embed=embed)
        if ctx.author.id in connection.get_admin_list():
            for i in Admin_reactions:
                await message.add_reaction(i)
        else:
            for i in User_reactions:
                await message.add_reaction(i)
        message_panel.append({message.id: ctx.author.id})

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        message_cheak = {reaction.message_id: reaction.user_id}
        Permission = 'Admin' if reaction.user_id in connection.get_admin_list() else 'User'
        panel_info = f"Guild: {self.bot.get_guild(reaction.guild_id)}\n" \
                     f"User: {await self.bot.fetch_user(reaction.user_id)}\n" \
                     f"Bot Permission: {'Admin' if reaction.user_id in connection.get_admin_list() else 'User'}\n"
        if message_cheak in message_panel and reaction.user_id != 905047827619663903:
            if Permission == 'Admin':
                if reaction.emoji.name == "1️⃣":
                    channels_text_info = f""
                    guild_channels = (self.bot.get_guild(reaction.guild_id)).text_channels
                    for i in guild_channels:
                        # Что то сделать
                        # Что то сделать
                        channels_text_info = f"{channels_text_info}\n{i.name:-^30}({i.id})" if i.type == discord.ChannelType.text else f"{channels_text_info}"
                        # Что то сделать
                        # Что то сделать
                    embed = discord.Embed(color=0xff9900, description=channels_text_info, title=panel_info)
                    message = await get_message(self.bot, reaction)
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    await message.add_reaction("⬅️")

                if reaction.emoji.name == "2️⃣":
                    channels_text_info = f""
                    guild_channels = (self.bot.get_guild(reaction.guild_id)).voice_channels
                    for i in guild_channels:
                        # Что то сделать
                        # Что то сделать
                        channels_text_info = f"{channels_text_info}\n{i.name:-^30}({i.id})\n" \
                                             f"{[j.name for j in i.members]!r}\n" if i.type == discord.ChannelType.voice else f"{channels_text_info}"
                        # Что то сделать
                        # Что то сделать
                    embed = discord.Embed(color=0xff9900, description=channels_text_info, title=panel_info)
                    message = await get_message(self.bot, reaction)
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    await message.add_reaction("⬅️")

                if reaction.emoji.name == "3️⃣":
                    pass


            if Permission == 'User':
                if reaction.emoji.name == "1️⃣":
                    pass


            if reaction.emoji.name == "⬅️":
                message = await get_message(self.bot, reaction)
                await message.clear_reactions()
                embed = discord.Embed(color=0xff9900,
                              description=f"{Admin_functional if reaction.user_id in connection.get_admin_list() else User_functional}",
                              title=panel_info)
                await message.edit(embed=embed)
                if reaction.user_id in connection.get_admin_list():
                    for i in Admin_reactions:
                        await message.add_reaction(i)
                else:
                    for i in User_reactions:
                        await message.add_reaction(i)

            if reaction.emoji.name == "⛔":
                message = await get_message(self.bot, reaction)
                await message.delete()


def setup(bot):
    bot.add_cog(AdminPanel(bot))
