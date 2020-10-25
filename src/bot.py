import logging
import traceback
from datetime import datetime
from logging.handlers import RotatingFileHandler

import discord
from discord.ext import commands

from src.db import db


handler = RotatingFileHandler(filename='discord.log', maxBytes=1024 * 10, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
logger.addHandler(handler)


intents = discord.Intents.none()
intents.members = True
intents.guild_messages = True
intents.guilds = True

allowed_mentions = discord.AllowedMentions(everyone=False, users=True, roles=False)

plugins = [
    "plugins.Plugin"
]


class RoleBot(commands.Bot):
    def __init__(self, config):
        super().__init__(
            command_prefix=commands.when_mentioned_or(config["prefix"]),
            intents=intents,
            allowed_mentions=allowed_mentions,
            case_insensitive=True)

        self.remove_command("help")
        self.logger = logger
        self.config = config
        self.version = [1, 0, 0, 'a']
        self.data = db.loadData()

    async def on_ready(self):
        print(f"Starting as {self.user}")
        logger.info(datetime.utcnow().strftime(f"Started at %H:%M:%S - %d/%m/%Y as {self.user}"))

        for plugin in plugins:
            try:
                self.load_extension(plugin)
            except Exception:
                logger.error(traceback.format_exc())


if __name__ == "__main__":
    config = db.loadConfig()
    if config is None:
        logger.exception("Config file not found or empty")
        exit()
    if config["token"] is not None:
        bot = RoleBot(config)
        bot.run(config["token"])
    else:
        logger.error("No token provided")