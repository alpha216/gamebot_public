import discord, sys, asyncio, motor, motor.motor_asyncio
from discord.ext import commands, tasks
import config

class Gamebot(commands.Bot):
    def __init__(self):
        print('starting gamebot')
        super().__init__(commands.when_mentioned_or('게임아 '), intents=discord.Intents.default(), shard_count=8)
        self.dbclient = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{config.mongodb_host}:{config.mongodb_port}")
        self.db = self.dbclient.gamebot
        for ext in config.ext_list:
            self.load_extension(ext)
    
    async def on_ready(self):
        print(f'logged in {self.user}')

    async def on_error(self, event, *args,**kwargs):
        print(event)

bot = Gamebot()


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'test' and len(config.token_test) > 1 : 
            bot.run(config.token_test)
        else : bot.run(config.token)
    except IndexError : bot.run(config.token)