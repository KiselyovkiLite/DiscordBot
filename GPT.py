import asyncio
import time

import openai
import os
import json
import encodings
from discord import File
from discord.ext import commands
from utilites import *
import discord
import io
import requests
import g4f
import config



openai.organization = config.organization
openai.api_key = config.gtp_api_key

"""
text = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "user", "content": "Почему игра громкая?"},
    ]
)
print(text)
text_v2 = (text['choices'][0]['message']['content'])
"""


class GPT_Bot(commands.Cog):
    """Всеми извесный GPT бот"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gpt")
    @commands.check(ban_gpt)
    async def _gpt_chat(self, ctx: discord.ext.commands.Context, *, text):
        
        await asyncio.sleep(3)
        await ctx.reply(f'Какая то ошибка, сорян не могу ответить')
        """
        gpt_use = self.bot.get_channel(1083401371119779910)
        await gpt_use.send(f"{ctx.author}({ctx.author.id}) Запросил {text}")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": f"{text}"},
                ]
            )
            await ctx.reply(f"{response['choices'][0]['message']['content']}")
        except:
        """


    @commands.command(name="gpt_image")
    @commands.check(ban_gpt)
    async def _gpt_image(self, ctx: discord.ext.commands.Context, *, text):
        
        await asyncio.sleep(3)
        await ctx.reply(f'Какая то ошибка, сорян не могу нарисовать')
        """
        gpt_use = self.bot.get_channel(1083401371119779910)
        await gpt_use.send(f"{ctx.author}({ctx.author.id}) Запросил нарисовать {text}")
        try:
            response = openai.Image.create(
                prompt=f"{text}",
                n=1,
                size="1024x1024"
            )
            image_url = response['data'][0]['url']
            photo = requests.get(image_url)
            fileq = io.BytesIO(photo.content)
            await ctx.reply("Вот твоя картинка", file=File(fileq, filename='znak.png'))
        except:
        """

    @commands.command(name="ban_gpt")
    @commands.check(ban_gpt)
    @commands.check(OwnerCheck)
    async def _ban_gpt(self, ctx: discord.ext.commands.Context, ban: discord.Member):
        connection.ban_gpt(ban.id)
        await ctx.reply("Забанил пидараса")

    @commands.command(name="unban_gpt")
    @commands.check(ban_gpt)
    @commands.check(OwnerCheck)
    async def _unban_gpt(self, ctx: discord.ext.commands.Context, ban: discord.Member):
        connection.unban_gpt(ban.id)
        await ctx.reply("Разбанил пидараса")


def setup(bot):
    bot.add_cog(GPT_Bot(bot))
