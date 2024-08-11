import discord
import requests
import json
from discord import File
from discord.ext import commands
import random
import vk_api
import io
from yt import YTDLSource
import datetime
from SQLMetod import SQL
import asyncio
from config import *
from bs4 import BeautifulSoup
from utilites import DungeonParty, ban_check, ChurkaChel
from gtts import gTTS

connection = SQL("localhost", "Bot", "Bot_Python")

vk = vk_api.VkApi(token=vk_token)


class DiscordBot(commands.Cog):
    """COMMAND FOR ALL"""

    def __init__(self, bot):
        self.bot = bot
        self.bot.add_application_command(self._is_admin)

    @commands.command(name="isadmin")
    @commands.check(ban_check)
    async def _is_admin(self, ctx):
        connection.UpdataBD()
        if ctx.message.author.id in connection.get_admin_list():
            await ctx.send(f'Ты Администратор')
        else:
            await ctx.send(f'Ты не Администратор')

    @commands.command(name="delete", aliases=['del'])
    @commands.check(ban_check)
    @commands.bot_has_permissions(manage_messages=True)
    async def _delete(self, ctx, *number: int):
        if number == "":
            number = 0
        channel = ctx.channel
        try:
            async for msg in channel.history(limit=int(number[0]) + 1):
                await msg.delete()
            await channel.send("Удаление завершено", delete_after=2.0)
        except:
            await channel.send("Подождите пока Бот выполит свою работу и повторите")

    """
    @commands.command(name="hug", aliases=['h'])
    @commands.check(ban_check)
    async def _hug(self, ctx, *who: str):
        who = who[0]
        response = requests.get('https://some-random-api.ml/animu/hug')
        json_data = json.loads(response.text)
        embed = discord.Embed(color=0xff9900, title=f'Hug')
        embed.set_image(url=json_data['link'])
        await ctx.channel.send(embed=embed, content=who)
    """

    @commands.command(name="sound", aliases=['snd'])
    @commands.check(ban_check)
    async def _sound(self, ctx, *, sound):

        connection.UpdataBD()

        # guild = ctx.guild
        # user = await guild.fetch_member(ctx.author.id)
        # if ctx.voice_client is not None:
        #    return await ctx.voice_client.move_to(user.voice.channel)
        # if ctx.voice_client.is_connected() == False:
        #    await user.voice.channel.connect()

        text = gTTS(text=sound, lang="ru", slow=False)
        text.save('Gtts.mp3')
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source='Gtts.mp3',
                                                                     executable=r'C:\Users\Kiselyov\Desktop\GitHub\Python Project\DiscordBot\ffmpeg\bin\ffmpeg.exe'))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command(name="choose", aliases=['ch'])
    @commands.check(ban_check)
    async def _choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        await ctx.send(random.choice(choices))

    """
    @commands.command(name="goroskop", aliases=['gor'])
    @commands.check(ban_check)
    async def _goroskop(self, ctx, znak: str):
        '''Check Your goroskop'''
        list_znak = {"овен": 10, "телец": 11, "близнецы": 12, "рак": 13, "лев": 14, "дева": 15, "весы": 20,
                     "скорпион": 21, "стрелец": 22, "козерог": 23, "водолей": 24, "рыбы": 25}
        search = f'''Гороскоп на {datetime.datetime.now().day}.Часть {str(list_znak[znak.lower()])[0]}.'''
        try:
            goroscop = vk.method('wall.search',
                                 {'owner_id': -182875281, 'count': 1, 'query': search, 'owners_only': 1})
            if goroscop['count'] == 0:
                text = "По вашему запросу ничего не найдено"
                photo = ""
            goroscop = goroscop["items"]
            for i in goroscop:
                text = str(i['text']).replace(f'Часть {str(list_znak[znak.lower()])[0]}.', '').strip()
                url = i['attachments'][int(str(list_znak[znak.lower()])[1])]['photo']['sizes'][-1]['url']
                photo = requests.get(url)
                fileq = io.BytesIO(photo.content)

            await ctx.send(f"{text} {znak}", file=File(fileq, filename='znak.png'))
        except:
            await ctx.send('Данная функция не работает(Напишите Администратору <@494896118975561728>)')
    """

    @commands.command(name="goroskop_v2", aliases=['gor_v2'])
    @commands.check(ban_check)
    async def goroskop_v2(self, ctx, znak: str):
        list_znak = {"овен": "aries", "телец": "taurus", "близнецы": "gemini", "рак": "cancer", "лев": "leo",
                     "дева": "virgo", "весы": "libra", "скорпион": "scorpio", "стрелец": "sagittarius",
                     "козерог": "capricorn", "водолей": "aquarius", "рыбы": "pisces"}
        # Общий
        request = requests.get(f"https://goroskop365.ru/{list_znak[znak.lower()]}/").text
        soup = BeautifulSoup(request, "lxml")
        date_goroskop = soup.find('div', class_="date").text
        text_all = soup.find('div', class_="content_wrapper horoborder").find("p").text
        # Любовь
        request = requests.get(f"https://goroskop365.ru/lyubov/{list_znak[znak.lower()]}/").text
        soup = BeautifulSoup(request, "lxml")
        text_love = soup.find('div', class_="content_wrapper horoborder").find("p").text
        # Работа
        request = requests.get(f"https://goroskop365.ru/biznes/{list_znak[znak.lower()]}/").text
        soup = BeautifulSoup(request, "lxml")
        text_work = soup.find('div', class_="content_wrapper horoborder").find("p").text
        # Фулл текст
        text = f"**Общий гороскоп** {date_goroskop}\n{text_all}\n**Любовный гороскоп**\n{text_love}\n**Гороскоп работы**\n{text_work}"
        await ctx.send(text)

    @commands.command(name="sovmestimost", aliases=['sovmest'])
    @commands.check(ban_check)
    async def _sovmestimost(self, ctx, znak: str):
        """Check Your sovmestimost with other ZZ"""
        list_znak = {"овен": 10, "телец": 11, "близнецы": 12, "рак": 13, "лев": 14, "дева": 15, "весы": 20,
                     "скорпион": 21, "стрелец": 22, "козерог": 23, "водолей": 24, "рыбы": 25}
        search = f'Совместимость на {datetime.datetime.now().day}.Часть {str(list_znak[znak.lower()])[0]}.'
        try:
            goroscop = vk.method('wall.search',
                                 {'owner_id': -182875281, 'count': 1, 'query': search, 'owners_only': 1})
            if goroscop['count'] == 0:
                text = "По вашему запросу ничего не найдено"
                photo = ""
            goroscop = goroscop["items"]
            for i in goroscop:
                text = str(i['text']).replace(f'Часть {str(list_znak[znak.lower()])[0]}.', '').strip()
                url = i['attachments'][int(str(list_znak[znak.lower()])[1])]['photo']['sizes'][-1]['url']
                photo = requests.get(url)
                fileq = io.BytesIO(photo.content)

            await ctx.send(f"{text} {znak}", file=File(fileq, filename='znak.png'))
        except:
            await ctx.send('Данная функция не работает(Напишите Администратору <@494896118975561728>)')

    @commands.command(name="avatar", aliases=['ava'])
    @commands.check(ban_check)
    async def _avatar(self, ctx, people: discord.Member):
        guild = ctx.guild
        user = await guild.fetch_member(people.id)
        url = str(user.avatar_url_as(static_format='png'))
        print(url)
        fileq = io.BytesIO(requests.get(url).content)
        await ctx.send(file=File(fileq, filename='tweet.png'))

    @commands.command(name="join", aliases=['j'])
    @commands.check(ban_check)
    async def _join(self, ctx):
        """Joins a voice channel"""
        guild = ctx.guild
        user = await guild.fetch_member(ctx.author.id)
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(user.voice.channel)

        await user.voice.channel.connect()

    @commands.command(name="play", aliases=['pl', 'p'])
    @commands.check(ban_check)
    async def _play(self, ctx, *, url):

        user = await ctx.guild.fetch_member(ctx.author.id)
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(user.voice.channel)

        await user.voice.channel.connect()

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command(name="stop", aliases=['st', 's'])
    @commands.check(ban_check)
    async def _stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @commands.command(name="waify", aliases=['w'])
    @commands.check(ban_check)
    async def _waify(self, ctx):
        try:
            req = requests.get(f'https://www.thiswaifudoesnotexist.net/example-{random.randint(0, 100000)}.jpg').content
            await ctx.send(file=File(io.BytesIO(req), filename='waify.png'))
        except:
            await ctx.send('Данная функция не работает(Напишите Администратору <@494896118975561728>)')

    @commands.command(name="setgame", aliases=['stG', "gameset"])
    @commands.check(ban_check)
    async def _setgame(self, ctx, *, game: str):

        connection.UpdataBD()

        if ctx.author.id in connection.get_admin_list():
            connection.set_game_text(game, ctx.author.id)
            await self.bot.change_presence(activity=discord.Game(game), status=discord.Status.online)
            await ctx.send(f'Игра сменена на "{game}"')
        else:
            await ctx.send('Недостаточно прав')

    @commands.command(name="listadmin", aliases=['listA', 'adminlist'])
    @commands.check(ban_check)
    async def _listadmin(self, ctx):

        connection.UpdataBD()

        admin_list = connection.get_admin_list()

        message = 'Администраторы:\n'

        for i in admin_list:
            message = f'{message}<@{i}>\n'
        await ctx.send(message)

    @commands.command(name="del_r", aliases=['d_r'])
    @commands.bot_has_permissions(manage_messages=True)
    @commands.check(ban_check)
    async def _del_r(self, ctx):

        await (await (self.bot.get_channel(ctx.message.reference.channel_id)).fetch_message(
            ctx.message.reference.message_id)).delete()
        await ctx.send('Удалил', delete_after=2)
        await ctx.message.delete()

    @commands.command(name='start_drochka', aliases=['st_dr'])
    @commands.check(DungeonParty)
    @commands.check(ban_check)
    async def _start_drochka(self, ctx):
        await ctx.message.delete()

        ping = "<@879687797022269470> <@481171951469985826> <@395243569721638913> <@403533426193465346> " \
               "<@398878761493463040> <@351781819710177290> <@494896118975561728> " \
               "<@608931269010653206> <@415578980436017152>"
        fileq = io.BytesIO(requests.get(
            'https://sun9-45.userapi.com/s/v1/ig2/J5n0fsENaGJ-DD4w1iEwnZw9mSNCb2jgPOHIEBhcb5stxEWQ7s4G2PfsHeOi0Hj'
            'XucdP1GJJ7E3yk8Ftq2gGPisg.jpg?size=1034x1080&quality=95&type=album').content)
        await ctx.send(ping, file=File(fileq, filename='drochka.png'))
        await asyncio.sleep(600)
        await ctx.send(f"Груповая МАСТУРБАЦИЯ НАЧАЛАСЬ\n{ping}")

    @commands.command(name='ranime')
    @commands.check(ban_check)
    async def _rAnime(self, ctx):
        data = {"base": "genres", "single": "true"}
        headers = {"authorization": "e95975fe462564212f9e3a269790564599f31bf4d85e7c1e8075cb46c14321f0"}
        chek = requests.post("https://www.randomanime.org/api/list/custom", data=data, headers=headers)
        json_chek = chek.json()
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
        await ctx.send(embed=embed)

    @commands.command(name='8ball', aliases=["8b"])
    @commands.check(ban_check)
    async def _8ball(self, ctx):
        answer = ['бесспорно', 'это было предрешено', 'никаких сомнений', 'определенно да',
                  'можешь быть уверен(а) в этом', 'мне кажется - да',
                  'вероятнее всего', 'хорошие перспективы', 'знаки говорят - да', 'да', 'пока не ясно',
                  'попробуй снова', 'лучше не рассказывать', 'сейчас нельзя предсказать',
                  'сконцентрируйся и спроси опять', 'даже не думай', 'мой ответ - нет', 'по моим данным - нет',
                  'перспективы плохие', 'весьма сомнительно']
        await ctx.reply(content=random.choice(answer), mention_author=False)

    @commands.command(name='churka_mode')
    @commands.check(ban_check)
    @commands.check(DungeonParty)
    @commands.check(ChurkaChel)
    async def _churka_mode(self, ctx: discord.ext.commands.Context):
        mode = connection.churka_mode_get()
        if mode == 1:
            connection.churka_mode_set(0)
            await ctx.send("Выключил")
        else:
            connection.churka_mode_set(1)
            await ctx.send("Включил")


    @commands.command(name='dota2')
    @commands.check(ban_check)
    @commands.check(DungeonParty)
    async def _dota2(self, ctx: discord.ext.commands.Context, *extra_player: discord.Member):
        list_player = ctx.author.voice.channel.members
        bot_remove = [159985870458322944, 905047827619663903, 234395307759108106]
        for i in bot_remove:
            bot = await ctx.guild.fetch_member(i)
            if bot in list_player:
                list_player.remove(bot)
        if len(list_player) == 10:
            first_team = set(random.sample(list_player, 5))
            second_team = set(list_player)
            second_team.difference_update(first_team)
            text = await self._full_team(first_team, second_team)
        elif len(list_player) < 10 and len(list_player)+len(extra_player) == 10:
            all_list = [*list_player, *extra_player]
            first_team = set(random.sample(all_list, 5))
            second_team = set(all_list)
            second_team.difference_update(first_team)
            text = await self._full_team(first_team, second_team)
        elif len(list_player) > 10 and len(list_player)-len(extra_player) == 10:
            if len(extra_player) >= 1:
                for i in extra_player:
                    list_player.remove(i)
            first_team = set(random.sample(list_player, 5))
            second_team = set(list_player)
            second_team.difference_update(first_team)
            text = await self._full_team(first_team, second_team)
        else:
            if len(list_player) < 10 and len(extra_player)+len(list_player) != 10:
                text = 'Не хватает людей'
            elif len(list_player) > 10 and len(extra_player)-len(list_player) != 10:
                text = "Много людей(после команды добавь id людей, которые не играют)"
            else:
                text = "Админ конч и не умеет кодить"

        await ctx.send(f"{text}")

    async def _full_team(self, first_team, second_team):
        text = 'Команда 1:\n'
        for i in first_team:
            if i.nick is not None:
                text = f'{text}{i.nick}\n'
            else:
                text = f'{text}{i.name}\n'
        text = f'{text}\n\nКоманда 2:\n'
        for i in second_team:
            if i.nick is not None:
                text = f'{text}{i.nick}\n'
            else:
                text = f'{text}{i.name}\n'
        return text


    @commands.command(name='roll')
    @commands.check(ban_check)
    async def _roll(self, ctx: discord.ext.commands.Context, roll_min: int = 0, roll_max: int = 100):
        await ctx.send(f"Число: {random.randint(roll_min, roll_max)}")


def setup(bot):
    bot.add_cog(DiscordBot(bot))
