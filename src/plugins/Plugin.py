import discord
from discord.ext import commands as cmds

from src.db import db


class Plugin(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot


    @cmds.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if len(before.roles) == len(after.roles):
            return

        role = list(set(before.roles) - set(after.roles)) or list(set(after.roles) - set(before.roles))
        config = db.get(self.bot, before.guild.id, "roles")

        if str(role[0].id) in config:
            try:
                await after.send(config[str(role[0].id)])
            except discord.Forbidden:
                self.bot.logger.info(f"Could not send {after} [{after.id}] the message")


    @cmds.Cog.listener()
    async def on_cog_command_error(self, ctx, error):
        if isinstance(error, cmds.RoleNotFound):
            await ctx.send("Die Rolle konnte nicht gefunden werden.")
        if isinstance(error, cmds.MissingRequiredArgument):
            await ctx.send("Es wurden nicht alle nötigen Argumente angeben.")
        if isinstance(error, cmds.CommandNotFound):
            pass

    @cmds.bot_has_permissions(send_messages=True)
    @cmds.has_permissions(administrator=True)
    @cmds.group()
    async def role(self, ctx: cmds.Context):
        if ctx.invoked_subcommand is None:
            return await ctx.send("__Es wurde kein Subcommand angegeben.__\n>>> "
                                  "**add** < `Rolle` > < `Nachricht` >\n"
                                  "**edit** < `Rolle` > < `Nachricht` >\n"
                                  "**remove** < `Rolle` >\n"
                                  "**check** < `Rolle` >")

    @role.command()
    async def add(self, ctx: cmds.Context, role: discord.Role, *, message: str):
        config = db.get(self.bot, ctx.guild.id, "roles")
        if str(role.id) in config:
            return await ctx.send("Diese Rolle wird bereits verwendet.")

        config[role.id] = message
        db.set(self.bot, ctx.guild.id, "roles", config)

        await ctx.send("Die Rolle wurde hinzugefügt.")

    @role.command()
    async def edit(self, ctx: cmds.Context, role: discord.Role, *, message: str):
        config = db.get(self.bot, ctx.guild.id, "roles")
        if str(role.id) not in config:
            return await ctx.send("Diese Rolle wird nicht verwendet.")

        config[role.id] = message
        db.set(self.bot, ctx.guild.id, "roles", config)

        await ctx.send("Die Rolle wurde editiert.")

    @role.command()
    async def remove(self, ctx: cmds.Context, role: discord.Role):
        config = db.get(self.bot, ctx.guild.id, "roles")
        if str(role.id) not in config:
            return await ctx.send("Diese Rolle wird nicht verwendet.")

        config.pop(role.id)
        db.set(self.bot, ctx.guild.id, "roles", config)

        await ctx.send("Die Rolle wurde entfernt.")

    @role.command()
    async def check(self, ctx: cmds.Context, role: discord.Role):
        config = db.get(self.bot, ctx.guild.id, "roles")
        if str(role.id) not in config:
            return await ctx.send("Diese Rolle wird nicht verwendet.")

        await ctx.send(config[role.id])

    @role.command()
    async def help(self, ctx: cmds.Context):
        await ctx.send("__Command Hilfe__\n>>> "
                       "**role add** < `Rolle` > < `Nachricht` >\n"
                       "**role edit** < `Rolle` > < `Nachricht` >\n"
                       "**role remove** < `Rolle` >\n"
                       "**role check** < `Rolle` >\n"
                       "**role help **")


def setup(bot):
    bot.add_cog(Plugin(bot))