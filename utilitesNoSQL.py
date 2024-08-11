import discord

Admin_list = [410183717106089994, 537775183566733314, 494896118975561728, 599565219194470410, 415578980436017152]


def AdminCheckNoSQL(ctx):
    if type(ctx) == discord.ApplicationContext:
        return (ctx.author.id in Admin_list) or (ctx.author.id == 494896118975561728)
    else:
        return (ctx.message.author.id in Admin_list) or (ctx.message.author.id == 494896118975561728)


def DungeonParty(ctx):
    if ctx.guild is None:
        return False
    else:
        return ctx.guild.id == 407828287914639360


def OwnerCheck(ctx):
    return ctx.message.author.id == 494896118975561728


def LogBot(ctx):
    if ctx.guild is None:
        return False
    else:
        return ctx.guild.id == 983302513325387816
