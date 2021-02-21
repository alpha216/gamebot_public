import discord, motor
from discord.ext import commands
import utils

class checkcog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.check = utils.check(bot.db)

    @commands.Cog.listener('on_command_error')
    async def error_handle(self, ctx: commands.Context, error: Exception):
        print(error)
        if isinstance(error, commands.CommandOnCooldown):
            minl = round(error.retry_after) // 60
            sec = round(error.retry_after) % 60
            if minl == 0: return await ctx.send(f'{sec}초 이후에 명령어를 다시 실행할수 있습니다')
            else: return await ctx.send(f'{minl}분 {sec}초 이후에 명령어를 다시 실행할수 있습니다')
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(embed=utils.info_embed(f"올바르지 않은 사용",f"올바른 사용법: `{ctx.prefix}{ctx.command} {ctx.command.usage}`",author=ctx.author))
        if isinstance(error, utils.exceptions.NotRegistered):
            return await ctx.send(embed=utils.info_embed("가입 필요",f"`{ctx.prefix}가입`을 통해 가입을 진행해 주세요.", author=ctx.author))
        if isinstance(error, utils.exceptions.SendNotRegistered):
            return await ctx.send(embed=utils.info_embed("송금 요류",f"송금하는 대상이 가입되어 있지 않습니다.", author=ctx.author))
        if isinstance(error, utils.exceptions.AlreadyRegistered):
            return await ctx.send(embed=utils.error_embed(f"이미 가입되어 있는 이용자입니다!",footer=f"{ctx.prefix}탈퇴 로 가입을 해제할수 있어요!",author=ctx.author))
        
        embed = discord.Embed(title='오류', description= f'`{error}`', color=config.embed_color)
        return await ctx.send(embed=utils.normal_embed('오류', error, ctx.author))

def setup(bot):
    bot.add_cog(checkcog(bot))