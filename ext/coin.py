import discord, motor, logging, asyncio
from discord.ext import commands, tasks
import utils


class coinclass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.check = utils.check(bot.db)
        check = self.check
        for cmds in self.get_commands():
            cmds.add_check(self.check.registered)

    @commands.command(name='코인')
    async def coin(self, ctx):
        user_data = await self.db.user.find_one({"discordId": ctx.author.id})
        coin = user_data['coin']

        await ctx.send(embed=utils.normal_embed('보유코인', f'{coin} 코인', author=ctx.author))

    @commands.command(name='송금', usage='(코인 양) (@맨션)')
    async def send_coin(self, ctx, arg:int, users: discord.User):
        user_data = await self.db.user.find_one({"discordId": ctx.author.id})
        coin = user_data['coin']

        await self.check.sendRegistered(users)

        if arg < 100:
            return await ctx.reply(embed=utils.normal_embed('코인부족', '100코인 이상부터 보낼 수 있습니다', ctx.author))
        if arg > coin:
            return await ctx.reply(embed=utils.normal_embed('코인부족', f'코인이 {int(arg) - user_coin}만큼 부족합니다.', ctx.author))

        await self.db.user.find_one_and_update({"discordId":ctx.author.id},{'$set':{"coin": coin - arg}})
        await self.db.user.find_one_and_update({"discordId":users.id},{'$inc':{"coin": arg}})

        await ctx.send(embed=utils.normal_embed('송금 완료', f'{user.mention}님께 {arg}코인을 보냈습니다', ctx.author))

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def 코인줘(self, ctx):
        await self.db.user.find_one_and_update({"discordId":ctx.author.id},{'$inc':{"coin": 200}})
        await ctx.send(embed=utils.info_embed('지급 완료', '1000코인을 지급하였습니다.', author=ctx.author))

def setup(bot):
    bot.add_cog(coinclass(bot))