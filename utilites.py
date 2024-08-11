from SQLMetod import SQL
import discord

connection = SQL("localhost", "Bot", "Bot_Python")
Admin_list = [410183717106089994, 537775183566733314, 494896118975561728, 599565219194470410]


def AdminCheck(ctx):
    connection.UpdataBD()
    if type(ctx) == discord.ApplicationContext:
        return (ctx.author.id in connection.get_admin_list()) or (ctx.author.id == 494896118975561728)
    else:
        return (ctx.message.author.id in connection.get_admin_list()) or (ctx.message.author.id == 494896118975561728)


def AdminCheckNoSQL(ctx):
    connection.UpdataBD()
    return (ctx.message.author.id in Admin_list) or (ctx.message.author.id == 494896118975561728)


def DungeonParty(ctx):
    if ctx.guild is None:
        return False
    else:
        return ctx.guild.id == 407828287914639360


def OwnerCheck(ctx):
    return ctx.message.author.id == 494896118975561728


def Armagedon_check(ctx):
    if connection.is_armagedon() is False:
        return True
    elif connection.is_armagedon() is True:
        return False


def ban_check(ctx):
    connection.UpdataBD()
    if type(ctx) == discord.ApplicationContext:
        return ctx.author.id not in connection.get_ban_list()
    else:
        return ctx.message.author.id not in connection.get_ban_list()



def LogBot(ctx):
    if ctx.guild is None:
        return False
    else:
        return ctx.guild.id == 983302513325387816


def ChurkaChel(ctx):
    return ctx.author.id != 608931269010653206


def ban_gpt(ctx):
    return ctx.author.id not in connection.get_gtp_ban_list()
