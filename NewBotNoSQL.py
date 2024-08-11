import discord
import requests
from discord.ext import commands
import random
import vk_api
import io
import os
import datetime
import asyncio
from async_eval import eval
from utilitesNoSQL import AdminCheckNoSQL, OwnerCheck, LogBot
from config import *
from Send_telega import Leave_send
import dis


vk = vk_api.VkApi(token=vk_token)
initial_extensions = []
bot = commands.Bot(command_prefix="&", pm_help=True, case_insensitive=True, intents=discord.Intents.all())
show_attachment = True
spam_durak = False
ping_list = [410183717106089994, 537775183566733314]
AdminCheckList = [410183717106089994, 537775183566733314, 494896118975561728]


@bot.event
async def on_ready():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
        except Exception as e:
            print(e)
    await bot.change_presence(status=discord.Status.offline)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_message_delete(ctx):
    fmt = f'{ctx.author} has deleted the message: {ctx.content}'
    channel = bot.get_channel(983302845522653234)
    await channel.send(fmt)
    print(ctx)


@bot.event
async def on_voice_state_update(member, before, after):

    ping = bot.get_channel(983329039387344908)
    channel = bot.get_channel(983302513929371720)
    channel_attachment = bot.get_channel(984774654352834560)

    if before.channel is None:
        fmt = f'{member} Зашёл в {after.channel}'
        join = 1
        attachment_bool = False

    elif after.channel is None:
        fmt = f'{member} Вышел из {before.channel}'
        join = 0
        attachment_bool = False

    elif (before.channel is not None) and (after.channel is not None) and (before.channel != after.channel):
        fmt = f'{member} Перешёл из {before.channel} в {after.channel}'
        join = 0
        attachment_bool = False

    elif before.channel == after.channel and show_attachment is True:
        join = 0
        attachments = 'Хз что сделал'
        attachment_bool = True

        if before.mute != after.mute:
            if before.mute is True:
                attachments = 'Размутил микро(Сервер)'
            else:
                attachments = 'Замутил микро(Сервер)'
        if before.deaf != after.deaf:
            if before.deaf is True:
                attachments = 'Размутил наушники(Сервер)'
            else:
                attachments = 'Замутил наушники(Сервер)'
        if before.self_mute != after.self_mute:
            if before.self_mute is True:
                attachments = 'Размутил микро'
            else:
                attachments = 'Замутил микро'
        if before.self_deaf != after.self_deaf:
            if before.self_deaf is True:
                attachments = 'Размутил наушники'
            else:
                attachments = 'Замутил наушники'
        if before.self_stream != after.self_stream:
            if before.self_stream is True:
                attachments = 'Выключил стрим'
            else:
                attachments = 'Включил стрим'
        if before.self_video != after.self_video:
            if before.self_video is True:
                attachments = 'Выключил вебку'
            else:
                attachments = 'Включил вебку'
        await channel_attachment.send(f'{member} Выполнил действие: {attachments}')
    else:
        join = 0
        fmt = "Дичь какая та"
        attachment_bool = False

    if member.id in ping_list and join == 1:
        await ping.send(
            f'{member} Зашёл в {after.channel} <@494896118975561728> <@494896118975561728>')
    if attachment_bool is False:
        await channel.send(fmt)


@bot.event
async def on_member_remove(member):
    block_stop = True
    global spam_durak
    ping = bot.get_channel(983329039387344908)

    if (member.guild.id == 983302513325387816) and (member.id == 410183717106089994) and block_stop is False:
        spam_durak = True
        while spam_durak is True:
            await ping.send(f"<@494896118975561728> НАСТЯ ЛИВНУЛА С СЕРВЕРА ДОЛБАЁБ <@494896118975561728>")
            await asyncio.sleep(1)
    else:
        await ping.send(f"{member} Ливнул с {member.guild}")


@bot.command(name="do", aliases=['d'])
@commands.check(AdminCheckNoSQL)
@commands.check(LogBot)
async def _do(ctx, *, params):

    if "shutdown" in params.lower():
        await ctx.send("Идёшь нахуй")
    else:
        channel = bot.get_channel(983304305392107530)
        await channel.send(f'{ctx.author} || {params}')
        await ctx.send(str(eval(params))[0:1999])


@bot.command(name='show_attachment')
@commands.check(AdminCheckNoSQL)
@commands.check(LogBot)
async def _show_attachment(ctx):

    global show_attachment

    if show_attachment is False:
        show_attachment = True
        await ctx.send("Доп функции включены")
    elif show_attachment is True:
        show_attachment = False
        await ctx.send("Доп функции выключены")


@bot.command(name='stop_spam')
@commands.check(OwnerCheck)
@commands.check(LogBot)
async def _show_attachment(ctx):
    global spam_durak
    spam_durak = False
    await ctx.send("Ладно успокоюсь")


if __name__ == "__main__":
    bot.remove_command("help")
    bot.run(bot_discord_token, reconnect=True)
