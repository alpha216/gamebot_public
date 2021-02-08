import discord, sys
from discord.ext import commands, tasks
from commands import rosipa, game, minigame, coin

bot = commands.Bot(command_prefix='게임아 ')

@bot.event
async def on_ready():
    print('loged')

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)

    if isinstance(error, commands.CommandOnCooldown):
        minl = round(error.retry_after) // 60
        sec = round(error.retry_after) % 60
        if minl == 0: await ctx.send(f'{sec}초 이후에 다시 실행할수 있습니다')
        else: await ctx.send(f'{minl}분 {sec}초 이후에 다시 실행할수 있습니다')

@bot.command()
async def 핑(ctx):
    await ctx.send(f'{round(round(bot.latency, 4)*1000)}핑') 

if __name__ == "__main__":
    bot.add_cog(coin.Core(bot))
    bot.add_cog(rosipa.Core(bot))
    bot.add_cog(game.Core(bot))
    bot.add_cog(minigame.Core(bot))
    try: 
        if sys.argv[1] == 'test' : bot.run('')
        else : bot.run('')
    except IndexError : bot.run('')