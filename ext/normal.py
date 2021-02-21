import discord, asyncio
from discord.ext import commands, tasks
import config, utils

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.db

    
    @commands.command(name='핑')
    async def ping(self, ctx):
        await ctx.send(f'{round(round(self.bot.latency, 4)*1000)}핑')

    @commands.command(name='가입')
    async def sign_in(self, ctx):
        if await self.db.user.find_one({"discordId":ctx.author.id}): 
            raise utils.exceptions.AlreadyRegistered
        await self.db.user.insert_one({"discordId" : ctx.author.id, "coin": 1000})
        await ctx.send(embed=utils.normal_embed('가입 완료', '가입이 완료되었습니다. \n 1000코인이 지급되었습니다.'))
    
    @commands.command(name='도움')
    async def help(self, ctx, *, comm = None):
        if not comm == None:
            return
        embed = utils.normal_embed('도움말', '명령어의 자세한 설명은 \n `도움 (명령어)`를 입력하세요')
        embed.add_field(name="일반", value= '핑', inline=False)
        embed.add_field(name="전적", value= '롤 / 배그', inline=False)
        embed.add_field(name="게임", value= '코인 / 코인줘 / 송금 \n 랜덤뽑기 / 가위바위보 ', inline=False)
        return await ctx.send(embed=embed)
        


def setup(bot):
    bot.add_cog(Core(bot))