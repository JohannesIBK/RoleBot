import json


def loadConfig():
    with open("db/config.json", "r") as f:
        data = json.load(f)
    return data

def loadData():
    with open("db/db.json", "r") as f:
        data = json.load(f)
    return data

def get(bot, guild_id: int, key: str) -> dict:
    if str(guild_id) not in bot.data:
        addGuild(bot.data, guild_id)

    guild = bot.data[str(guild_id)]
    return guild[key]


def addGuild(data, guild_id: int, new=None):
    data[str(guild_id)] = {"roles": new or {}}

    with open("db/db.json", "w") as f:
        json.dump(data, f)


def set(bot, guild_id: int, key, config):
    if guild_id not in bot.data is None:
        addGuild(bot.data, guild_id, config)
        return

    bot.data[str(guild_id)][key] = config

    with open("db/db.json", "w") as f:
        json.dump(bot.data, f)
