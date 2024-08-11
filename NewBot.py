import discord
import requests
from discord.ext import commands
import random
import vk_api
import io
import datetime
from async_eval import eval
from utilites import AdminCheck, OwnerCheck, LogBot, ban_check
from config import *
from discord import File
from SQLMetod import SQL
from bs4 import BeautifulSoup
import os

vk = vk_api.VkApi(token=vk_token)
initial_extensions = ['DiscordBot', "AdminCommand", "EventQuest", "AdminPanel", "NSFWBOT", "Secret", "GPT"]
connection = SQL("26.8.182.214", "Bot", "Bot_Python")
bot = commands.Bot(command_prefix="&", pm_help=True, case_insensitive=True, intents=discord.Intents.all())
show_attachment = True
spam_durak = False


@bot.event
async def on_ready():
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)
    await bot.change_presence(activity=discord.Game(connection.get_game_text()), status=discord.Status.online)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_message_delete(ctx):
    if ctx.author.id != 228537642583588864 and ctx.channel.id != 983302845522653234:
        file = None
        if ctx.attachments:
            file = requests.get(ctx.attachments[0].url).content
        fmt = f'{ctx.author} has deleted the message: {ctx.content}'
        channel = bot.get_channel(983302845522653234)
        await channel.send(fmt,
                           file=File(io.BytesIO(file), filename='deleted.png') if ctx.attachments != [] else None)
        print(ctx)


@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    connection.UpdataBD()

    fmt = ""
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

    # if member.id in connection.get_ping_list() and join == 1:
    #        await ping.send(
    #        f'{member} Зашёл в {after.channel} <@494896118975561728> <@494896118975561728>')
    if attachment_bool is False:
        await channel.send(fmt)


@bot.event
async def on_member_remove(member):
    ping = bot.get_channel(983329039387344908)
    await ping.send(f"{member} Ливнул с {member.guild}")


@bot.slash_command(name="do", description="Выполняет команду в интерпретаторе Python")
@commands.check(AdminCheck)
async def _do(ctx, *, params):
    if "shutdown" in params.lower() or "exit" in params.lower():
        await ctx.send_response("Идёшь нахуй")
    else:
        channel = bot.get_channel(983304305392107530)
        await channel.send(f'{ctx.author} || {params}')
        await ctx.send_response(str(eval(params))[0:1999])


@bot.command(name='show_attachment')
@commands.check(AdminCheck)
@commands.check(LogBot)
async def _show_attachment(ctx):
    global show_attachment

    if show_attachment is False:
        show_attachment = True
        await ctx.send("Доп функции включены")
    elif show_attachment is True:
        show_attachment = False
        await ctx.send("Доп функции выключены")


@bot.slash_command(name="naxui", description="Проверка на лоха")
@commands.check(AdminCheck)
async def _naxui(ctx,
                 kto_ti: discord.Option(str, "Кто же ты такой", choices=['Лох'], required=False)):
    await ctx.send_response(f"Ты {'Гений' if kto_ti is None else kto_ti}")


@bot.slash_command(name="goroskop", description="гороскоп на сегодня")
@commands.check(ban_check)
@commands.cooldown(1, 86400, commands.BucketType.user)
async def _goroskop(ctx,
                    znak: discord.Option(str, "Твой знак зодиака", choices=["Овен", "Телец", "Близнецы", "Рак",
                                                                            "Лев", "Дева", "Весы", "Скорпион",
                                                                            "Стрелец", "Козерог", "Водолей", "Рыбы"])):
    list_znak = {"овен": 10, "телец": 11, "близнецы": 12, "рак": 13, "лев": 14, "дева": 15, "весы": 20,
                 "скорпион": 21, "стрелец": 22, "козерог": 23, "водолей": 24, "рыбы": 25}

    search = f'''Гороскоп на {datetime.datetime.now().day}.Часть {str(list_znak[znak.lower()])[0]}.'''
    text = ''
    if ctx.author.id in connection.get_admin_list() and _goroskop.is_on_cooldown(ctx):
        _goroskop.reset_cooldown(ctx)
        text = 'Кд было сброшено, не благодари\n'
    try:
        goroscop = vk.method('wall.search',
                             {'owner_id': -182875281, 'count': 1, 'query': search, 'owners_only': 1})
        if goroscop['count'] == 0:
            text = "По вашему запросу ничего не найдено"
            photo = ""
        goroscop = goroscop["items"]
        for i in goroscop:
            text = f"{text}{str(i['text']).replace(f'Часть {str(list_znak[znak.lower()])[0]}.', '').strip()}"
            url = i['attachments'][int(str(list_znak[znak.lower()])[1])]['photo']['sizes'][-1]['url']
            photo = requests.get(url)
            fileq = io.BytesIO(photo.content)

        await ctx.send_response(f"{text} {znak}", file=File(fileq, filename='znak.png'))
    except Exception as e:
        await ctx.send_response(f'Данная функция не работает(Напишите Администратору <@494896118975561728>){e}')


@bot.slash_command(name='ranime', description="Случайное аниме")
@commands.check(ban_check)
@commands.cooldown(1, 10, commands.BucketType.user)
async def _rAnime(ctx):
    data = {"base": "genres", "single": "true"}
    headers = {"authorization": "35UYgP7tEkLVPZ4bAHGRGxn9EuWdRhVd3PmvY745zyeZf2GyF8QAgzwTi6k6ipEV"}
    chek = requests.post("https://www.randomanime.org/api/list/custom", data=data, headers=headers)
    json_chek = chek.json()
    print(json_chek)
    anime_name = json_chek["results"]["anime"]
    anime_ulr = "https://www.randomanime.org/anime/" + anime_name
    anime_info = requests.get(anime_ulr).text
    soup = BeautifulSoup(anime_info, "html.parser")
    episods = soup.find_all("p", class_="entry__info-bucket-content")[2].text
    duration = soup.find_all("p", class_="entry__info-bucket-content")[3].text
    name = str(soup.find("span", class_="h-fluid-top-header").text)
    pic = f'https://www.randomanime.org/{soup.find("img", class_="entry-header__image").get("src")}'
    itog = f'Название: {name}\n' \
           f'Кол-во серий: {episods}\n' \
           f'Ср. Прод. Серии: {duration} мин\n' \
           f'Cсылка: {anime_ulr}'
    embed = discord.Embed(color=0xff9900, title=itog)
    embed.set_image(url=pic)
    await ctx.send_response(embed=embed)


@bot.slash_command(name='genshin_porn', description="NSFW картинка с геншином", )
@discord.is_nsfw()
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.check(ban_check)
async def _genshin_porn(ctx):
    await ctx.send_response("Рандом Хентыч Гашиш", file=File("genshin.png", filename='genshin.png'))
    while True:
        memory = await _genshin_porn_load_new_photo()
        if memory <= 8288608:
            break


async def _genshin_porn_load_new_photo():
    headers = {'Referer': 'http://thatpervert.com/'}
    hentai_list = requests.get(r"http://thatpervert.com/tag/Genshin+Impact+porn", headers=headers)
    soup = BeautifulSoup(hentai_list.text, "lxml")
    page_last = int(soup.find('div', class_='pagination_expanded').find('span', class_='current').text)
    random_page = random.randint(0, page_last)
    hentai_page = requests.get(rf"http://thatpervert.com/tag/Genshin+Impact+porn/{random_page}", headers=headers)
    image = BeautifulSoup(hentai_page.text, "lxml")
    list_image = image.find_all('a', class_='prettyPhotoLink')
    request_image = requests.get(random.choice(list_image).get('href'), headers=headers).content
    with open('genshin.png', "wb") as file:
        file.write(request_image)
    return os.stat('genshin.png').st_size


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Блять, подожди {round(error.retry_after, 2)} секунд пжшка",
                       delete_after=error.retry_after if int(error.retry_after) <= 30 else 10)

    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send(f"&help Для кого придумали, долбаёб, нет такой команды", delete_after=10.0)
        
    else:
        print(error)
        print(type(error))
        await ctx.send(f"Да идите вы нахуй, до вас всё нормально работало, а сейчас вот эта хуйня выскакивает: {error}")


@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Блять подожди, кд", description=f"Попробуй через {error.retry_after:.2f}s.")
        await ctx.send_response(embed=em, delete_after=error.retry_after if int(error.retry_after) <= 30 else 10)

    elif isinstance(error, discord.errors.CheckFailure):
        await ctx.send_response(f"А кто тебе разрешал эту команду использовать, ты фейс контроль не прошёл ИДИ НАХУЙ",
                                delete_after=5.0)
    else:
        print(error)
        print(type(error))
        await ctx.send_response(f"Да идите вы нахуй, до вас всё нормально"
                                f" работало, а сейчас вот эта хуйня выскакивает: {error}")


if __name__ == "__main__":
    bot.run(bot_discord_token, reconnect=True)
