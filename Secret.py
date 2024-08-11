import discord
import requests
import json
from discord import File
from discord.ext import commands
import random
import io
import datetime
from SQLMetod import SQL
import asyncio
from utilites import DungeonParty, ban_check, AdminCheck
import os


connection = SQL("localhost", "Bot", "Bot_Python")


class Secret(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="terapiya")
    @commands.check(AdminCheck)
    async def _sound(self, ctx: discord.ext.commands.Context, *, number):
        guild = ctx.guild
        user = await guild.fetch_member(ctx.author.id)
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(user.voice.channel)

        await user.voice.channel.connect()
        if int(number) in range(1, 11):
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source=f'D:\Видео Славянская Клиника\Диск {connection.terapiya_get()}.mp3',
                                                                         executable=r'C:\Users\Kiselyov\Desktop\GitHub\Python Project\DiscordBot\ffmpeg\bin\ffmpeg.exe'))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            connection.terapiya_add()
        else:
            await ctx.send("Нужно число от 1 до 10")

    @commands.command(name="clear_terapiya")
    @commands.check(AdminCheck)
    async def _sound(self, ctx: discord.ext.commands.Context):
        connection.terapiya_clear()
        await ctx.send("Список очищен")


def setup(bot):
    bot.add_cog(Secret(bot))
