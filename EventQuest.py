from discord.ext import commands
from SQLMetod import SQL
from utilites import AdminCheck, ban_check

connection = SQL("localhost", "Bot", "Bot_Python")


class EventQuest(commands.Cog):
    """Ивент Для Всех можете спросить любой вопрос у админа и он вам ответит ответ доступен для всех Админов
     или задающего вопрос"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='intro_event', aliases=["int_event"])
    @commands.check(ban_check)
    async def _intro_event(self, ctx):
        await ctx.send("Тут я короче Ивент проготовил я хакнул Админа и могу отвечать на вопросы из его головы вы"
                       " просто &help EventQuest напишите и посмотрите команды а юзайте пока Админ не заметил")

    @commands.command(name='get_list_word', aliases=["GTW"])
    @commands.check(ban_check)
    @commands.dm_only()
    async def _get_list_word(self, ctx):
        """Получить список всех слов  формат слово - ###(если есть "#" то ответесть если "&" ответа нету)"""
        connection.UpdataBD()
        word_answer = connection.get_list_quest_word()
        text = 'Вопросы:\n'

        for word, answer in word_answer.items():
            if answer is None:
                znak_answer = "&&&"
            else:
                znak_answer = "###"
            text = f"{text} ${word} - {znak_answer}\n"
        await ctx.send(text)

    @commands.command(name='add_quest', aliases=["add_q"])
    @commands.check(ban_check)
    async def _add_quest(self, ctx, *, quest):
        """Добавить вопрос в базу данных"""
        connection.UpdataBD()
        connection.add_query_quest_word(quest, ctx.author.id)
        await ctx.send(f'Вопрос: {quest} Добавил')
        channel = self.bot.get_channel(985995463830417458)
        await channel.send(f'{ctx.author} Добавил Новый вопрос:{quest}\n<@494896118975561728>')

    @commands.command(name='answer_quest', aliases=["answ_q"])
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    async def answer_quest(self, ctx, *word_answer: str):
        """Команда для Админа чтоб на вопросы отвечать"""
        connection.UpdataBD()
        if ctx.author.id == 494896118975561728:
            connection.answer_quest_word(word_answer[0], word_answer[1])
            await ctx.message.delete()
            await ctx.send(f'На вопрос {word_answer[0]} Ответил')
            id_who = connection.get_who_word(word_answer[0])
            user = await self.bot.fetch_user(id_who)
            await user.send(
                f"Администратор ответил на ваш вопрос: {word_answer[0]}\nУзнать ответ:&get_answer {word_answer[0]}")
        elif ctx.author.id in connection.get_admin_list():
            await ctx.send('Мне чесно похую что ты админ но даже ты это юзать не можешь')

    @commands.command(name='get_answer', aliases=['get_a'])
    @commands.check(ban_check)
    @commands.dm_only()
    async def _get_answer(self, ctx, *, word):
        """Команда чтобы получить ответ на вопрос(Удалится через 5 сек.)"""
        connection.UpdataBD()

        word = connection.get_quest_word(word)

        if (ctx.author.id in connection.get_admin_list()) or (ctx.author.id == word[1]):
            await ctx.send(f'Ответ на твой вопрос: {word[0]}', delete_after=5.0)
        elif word[0] is None:
            await ctx.send("Такого вопроса неть")
        else:
            await ctx.send("Иди нахуй ты не задавал этого вопроса")

    @commands.command(name='delete_quest', aliases=['del_q'])
    @commands.check(AdminCheck)
    @commands.check(ban_check)
    async def _delete_quest(self, ctx, *, word):
        """Команда Для удаления вопроса(Естественно только для админа)"""
        connection.UpdataBD()
        if ctx.author.id == 494896118975561728:
            connection.delete_quest(word)
            await ctx.send(f"Удалил вопрос: {word}")
        elif ctx.author.id in connection.get_admin_list():
            await ctx.send("Блять Ты конечно Админ но я хуй удалю этот вопрос")


def setup(bot):
    bot.add_cog(EventQuest(bot))
