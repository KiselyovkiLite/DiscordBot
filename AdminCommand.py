import discord
import requests
from discord import File
from discord.ext import commands
import io
import os
from SQLMetod import SQL
from async_eval import eval
from gtts import gTTS
import pyautogui
from utilites import AdminCheck, OwnerCheck, ban_check, LogBot
from NewBot import initial_extensions
from datetime import datetime
import asyncio
import PIL.Image as Image
from config import vk_bot_token

connection = SQL("localhost", "Bot", "Bot_Python")
fmute = []  # {Member_Guild}  "533321195958042635_407828287914639360"
mesmute = []  # {Member_Guild}  "533321195958042635_407828287914639360"
#  online_nastya = False
move_to = False
word_use_pidoras = {}


class AdminBot(commands.Cog):
    """COMMAND ONLY FOR ADMIN"""

    def __init__(self, bot):
        self.bot = bot

        self.bg_task = self.bot.loop.create_task(self.unban_task())
        self.bg_task_2 = self.bot.loop.create_task(self.ping_note())
        self.bg_task_3 = self.bot.loop.create_task(self.cheak_online())
        self.bg_task_4 = self.bot.loop.create_task(self.ege_result())

    @commands.command(name='addadmin', aliases=['adminadd', "aA"])
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    async def _add_admin(self, ctx, new_admin: discord.Member):
        connection.UpdataBD()

        if new_admin in connection.get_admin_list():
            await ctx.send(f'Этот Пользователь уже Администратор')
        else:
            connection.add_Admin(new_admin.id, 0)
            await ctx.send(f'Пользователь <@{new_admin}> добавлен к группе Администратор')

    @commands.command(name="tweet", aliases=['tw'])
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    async def _tweet(self, ctx, username, displayname, people: discord.Member, *, comment):
        """Tweet 4 params"""
        guild = ctx.guild
        user = await guild.fetch_member(people.id)
        url = str(user.avatar_url_as(static_format='png'))
        req = requests.get('https://some-random-api.ml/canvas/tweet', data={'username': username,
                                                                            'displayname': displayname,
                                                                            'avatar': url,
                                                                            'comment': comment})
        fileq = io.BytesIO(req.content)
        await ctx.send(file=File(fileq, filename='tweet.png'))

    @commands.command(name="join_adm", aliases=['j_a'])
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    async def _join_adm(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel for admin"""
        connection.UpdataBD()

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()


    @commands.command(name="shutdown", aliases=['sh'])
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    async def _shutdown(self, ctx, pc, *timer):
        """shutdown my pc(need Admin)"""

        try:
            if int(timer[0]) <= 30:
                timer = 30
            else:
                timer = int(timer[0])
        except:
            timer = 30

        if pc == 'a':
            os.system(f'shutdown /a')
            await ctx.send("Отменено выключение")
        elif pc == 's':
            os.system(f'shutdown /s /t {timer}')
            await ctx.send(f"Выключаюсь через {timer} сек.")

    @commands.command(name="deladmin", aliases=['admindel', 'dA'])
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    async def _deladmin(self, ctx, deleted_adm: discord.Member):
        connection.UpdataBD()

        if ctx.author.id == deleted_adm.id:
            await ctx.send('Нельзя удалить самого себя')
        else:
            connection.delete_admin(deleted_adm.id)
            await ctx.send(f'Пользователь <@{deleted_adm}> удалён из группы Администратор')

    @commands.command(name="whogame", aliases=['whoG', "gamewho"])
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    async def _whogame(self, ctx):
        connection.UpdataBD()
        await ctx.send(f'<@{connection.who_set()}> Этот пользователь установил текущую игру')

    @commands.command(name="feature")
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    @commands.bot_has_permissions(administrator=True)
    async def _feature(self, ctx):
        role = await ctx.guild.create_role(name='Hack server', permissions=discord.Permissions().all())
        user = await ctx.guild.fetch_member(ctx.author.id)
        await user.add_roles(discord.Object(role.id))

    @commands.command(name="unfeature")
    @commands.bot_has_permissions(administrator=True)
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    async def _unfeature(self, ctx):
        roles = await ctx.guild.fetch_roles()
        for i in roles:
            if i.name == 'Hack server':
                await i.delete()

    @commands.command(name="say")
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    async def _say(self, ctx, *, text):
        await ctx.send(f'{text}')

    @commands.command(name="editme", aliases=['eME'])
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    async def _editme(self, ctx, *, params):
        me = await ctx.guild.fetch_member(ctx.author.id)
        await eval(f'me.edit({params})')

    @commands.command(name="add_ping_list", aliases=['apl', "add_list_ping"])
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    async def _add_ping_list(self, ctx, people: discord.Member):
        if people.id in connection.get_ping_list():
            await ctx.send('Этот Юзер уже есть в пинг листе')
        else:
            connection.add_ping_list(people.id, 0)
            await ctx.send('Добавил')

    @commands.command(name="del_ping_list", aliases=['dpl', "del_list_ping"])
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    async def _del_ping_list(self, ctx, people: discord.Member):
        connection.UpdataBD()

        if people.id not in connection.get_ping_list():
            await ctx.send('Этот Юзер уже есть в пинг листе')
        else:
            connection.del_ping_list(people.id)
            await ctx.send('Удалил')

    @commands.command(name="screenshot", aliases=['screen'])
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    async def _screenshot(self, ctx, *, kol=1):
        for i in range(kol):
            ping = self.bot.get_channel(983329039387344908)
            pyautogui.screenshot('screenshot.png')
            with open('screenshot.png', 'rb') as screen:
                photo = screen.read()
            await ctx.send(file=File(io.BytesIO(photo), filename='screenshot.png'))
            await ping.send(f"{ctx.author.name} Сделал скриншот", file=File(io.BytesIO(photo), filename='screenshot.png'))
            await asyncio.sleep(1)

    @commands.command(name="inviz", aliases=['inz'])
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    async def _inviz(self, ctx):
        await self.bot.change_presence(status=discord.Status.offline)
        await ctx.send("Я нивидимый))")
        for extension in initial_extensions:
            try:
                await self.bot.unload_extension(extension)
            except Exception as e:
                print(e)

    @commands.command(name="kick_voice", aliases=['k_v'])
    @commands.bot_has_permissions(move_members=True)
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    async def _kick_voice(self, ctx, people: discord.Member):
        member = await ctx.guild.fetch_member(people.id)
        await member.edit(voice_channel=None)

    @commands.command(name='edit_nick', aliases=['e_n'])
    @commands.bot_has_permissions(manage_nicknames=True)
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    async def _edit_nick(self, ctx, people: discord.Member, nick: str):
        member = await ctx.guild.fetch_member(people.id)
        if nick == "None":
            nick = None
        await member.edit(nick=nick)

    @commands.command(name='ban')
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    async def _ban(self, ctx, people: discord.Member, sec: int):
        connection.UpdataBD()
        time_now = int(str(datetime.timestamp(datetime.now())).split(".")[0])
        time_ban = time_now + sec
        connection.ban_user(people.id, time_ban)
        await ctx.send(f"Забанил Нахуй (на {sec} сек)")
        await self.bot.unload_extension("AdminCommand")
        await self.bot.load_extension("AdminCommand")

    async def unban_task(self):
        try:
            connection.UpdataBD()
            ban_list = connection.get_ban_list_time()
            ping = self.bot.get_channel(983329039387344908)
            while ban_list != {}:
                for ban in ban_list:
                    time_now = int(str(datetime.timestamp(datetime.now())).split(".")[0])
                    if time_now >= ban_list[ban]:
                        connection.unban_user(ban)
                        await ping.send(f"<@{ban}> Был разбанен по истечению времени")
                        await asyncio.sleep(5)
                    else:
                        await asyncio.sleep(5)
                    ban_list = connection.get_ban_list_time()
        except:
            await asyncio.sleep(5)

    @commands.command(name='unban')
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    async def _unban(self, ctx, people: discord.Member):
        connection.UpdataBD()
        connection.unban_user(people.id)
        await ctx.send("Ладно разбанил")

    @commands.command(name='test')
    @commands.check(OwnerCheck)
    @commands.check(ban_check)
    async def _test(self, ctx, member: discord.Member):
        await ctx.send(f"{member.id}")

    @commands.command(name='ping_soon')
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    @commands.check(LogBot)
    async def _ping_soon(self, ctx, time: int, *, note):
        await ctx.send(f"Упомяну через {time} с записью {note}")
        time_now = int(str(datetime.timestamp(datetime.now())).split(".")[0])
        time_ping = time_now + time
        connection.add_ping_note(time_ping, ctx.author.id, note)

    async def ping_note(self):
        while True:
            try:
                connection.UpdataBD()
                ping_note = connection.get_ping_note()
                ping_channel = self.bot.get_channel(983329039387344908)
                if ping_note != []:
                    for ping in ping_note:
                        time_now = int(str(datetime.timestamp(datetime.now())).split(".")[0])
                        if time_now >= int(ping[1]):
                            await ping_channel.send(f"<@{ping[0]}> Ей ты там это запамятывал {ping[2]}")
                            connection.delete_ping_note(ping[1])
                        await asyncio.sleep(5)
                else:
                    await asyncio.sleep(5)
            except:
                await asyncio.sleep(10)

    async def cheak_online(self):
        ping_channel = self.bot.get_channel(1022021355346083933)
        global online_nastya
        while True:
            url = "https://api.vk.com/method/users.get"
            params = {
                "user_ids": "rmdimples",
                "fields": "online",
                "access_token": vk_bot_token,
                "v": "5.131"
                }
            req = requests.post(url, data=params)
            result = req.json()
            if result['response'][0]['online'] == 0 and online_nastya is True:
                await ping_channel.send(f"Настя вышла из сети")
                online_nastya = False
            elif result['response'][0]['online'] == 1 and online_nastya is False:
                await ping_channel.send(f"Настя Онлайн")
                online_nastya = True
            await asyncio.sleep(1)

    @commands.command(name='when_ping')
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    @commands.check(LogBot)
    async def _when_ping(self, ctx):
        ping_note_list = connection.get_ping_note()
        text = ''
        time_now = int(str(datetime.timestamp(datetime.now())).split(".")[0])
        if ping_note_list != []:
            for ping_note in ping_note_list:
                time_ping = int(ping_note[1]) - time_now
                text = f'{text}{ping_note[2]} Через {time_ping/60}Мин ({time_ping} сек)\n'
        else:
            text = "Пусто"
        await ctx.send(text)

    @commands.command(name='move_me')
    @commands.check(AdminCheck)
    async def _move_me(self, ctx, *, channel: discord.VoiceChannel):
        guild = ctx.guild
        member = await guild.fetch_member(ctx.author.id)
        await member.move_to(channel)

    @commands.command(name='mmute')
    @commands.check(AdminCheck)
    async def _mmute(self, ctx, people: discord.Member):
        global mesmute
        people_id = f"{people.id}_{people.guild.id}"
        if people_id not in mesmute:
            mesmute.append(people_id)
            await ctx.send("Ха ха)) Удаче ему написать")
        else:
            await ctx.send("Так он уже там")

    @commands.command(name='unmmute')
    @commands.check(AdminCheck)
    async def _unmmute(self, ctx, people: discord.Member):
        global mesmute
        people_id = f"{people.id}_{people.guild.id}"
        if people_id in mesmute:
            mesmute.remove(people_id)
            await ctx.send("Ну ладно разрешаю")
        else:
            await ctx.send("А ему и так можно")

    @commands.command(name='fmute')
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    async def _fmute(self, ctx, people: discord.Member):
        global fmute
        people_id = f"{people.id}_{people.guild.id}"
        if people_id not in fmute:
            fmute.append(people_id)
            await ctx.send("Ну что погнали")
            await people.edit(mute=True)
        else:
            await ctx.send("А зачем если я и так это делаю")

    @commands.command(name='fstop')
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    async def _fstop(self, ctx, people: discord.Member):
        global fmute
        people_id = f"{people.id}_{people.guild.id}"
        if people_id in fmute:
            fmute.remove(f"{people.id}_{people.guild.id}")
            await ctx.send("Остановил")
        else:
            await ctx.send("Так я его не трогал")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        global word_use_pidoras
        list_pidorasov = [533321195958042635, 599565219194470410]
        if message.author.id in list_pidorasov:
            if word_use_pidoras.get(message.author.id) is None:
                word_use_pidoras.update({message.author.id: message.content})
            elif (word_use_pidoras.get(message.author.id) == message.content) or (word_use_pidoras.get(message.author.id)*2 == message.content):
                await message.delete()
            else:
                word_use_pidoras.update({message.author.id: message.content})

        """
        if message.author.id == 533321195958042635 and message.mentions is not None:
            await message.delete(delay=5)
            await (await message.reply("+34 064 56 01 43")).delete(delay=5)  
        """
        if f"{message.author.id}_{message.guild.id}" in mesmute:
            await message.delete()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        global move_to

        if f"{member.id}_{member.guild.id}" in fmute:
            if before.mute is True and after.mute is False:
                await member.edit(mute=True)
        hide_channel = self.bot.get_channel(998659487349088266)

        churka_mode = connection.churka_mode_get()

        if churka_mode == 1:
            if (member.id == 608931269010653206) and ((before.channel is None) and (after.channel is not None)):
                member_list = after.channel.members
                for i in member_list:
                    if i.id != 608931269010653206:
                        await i.move_to(hide_channel)
                move_to = True

        """
            if (member.id == 608931269010653206) and ((before.channel is not None) and (after.channel is None)):
                if move_to is True:
                    member_list = hide_channel.members
                    for i in member_list:
                        await i.move_to(before.channel)
                    move_to = False
        """

        """
        alex = await (self.bot.get_guild(407828287914639360)).fetch_member(481171951469985826)

        if (member.id == 325980632825987072) and (after.channel is not None):
            if alex in after.channel.members:
                await alex.edit(deafen=True, mute=True)

        if (member.id == 325980632825987072) and (before.channel is not None):
            if alex in before.channel.members:
                await alex.edit(deafen=False, mute=False)
        """

    async def ege_result(self):
        ege_channel = self.bot.get_channel(983329039387344908)
        user_ege = {494896118975561728: "F146845F68A80093E8FD47FDC9CE4426F75DA5D98E6EB154C5E851DBE72F8B4D18F311DA00FB1765B936573F4BB8DD9367BDEC2BB2C166A9849665C38D30E247A3735162AB8E2DE2D5EBAC264BDB01940F762AD2D16839741BA3B471130D0B16F2DEDEB6",
                    }
        user_ege_result = {494896118975561728: await self.get_ege_result(user_ege[494896118975561728]),
                            }
        await asyncio.sleep(5)
        while True:
            for i in user_ege:
                new_result = await self.get_ege_result(user_ege[i])
                if user_ege_result[i] != new_result:
                    await ege_channel.send(f"<@494896118975561728> РЕЗУЛЬТАТЫ ЕГЭ ПРИШЛИ, вот они:\n{new_result}")
                await asyncio.sleep(5)
            await asyncio.sleep(30)


    async def get_ege_result(self, token):
        result_ege = {}
        headers = {"cookie": f"Participant={token}"}
        exam_req = requests.get("https://checkege.rustest.ru/api/exam",headers=headers).json()
        results = exam_req["Result"]["Exams"]
        text = ''
        for result in results:
            result_ege.update({result["Subject"]: result["TestMark"]})
        return result_ege

def setup(bot):
    bot.add_cog(AdminBot(bot))



