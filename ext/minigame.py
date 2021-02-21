import discord, re, random, math, asyncio, motor, motor.motor_asyncio
from discord.ext import commands, tasks
import config, utils

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.check = utils.check(bot.db)
        check = self.check
        for cmds in self.get_commands():
            cmds.add_check(self.check.registered)
    
    @commands.command(name='가위바위보', usage='(코인)')
    async def rps(self, ctx, coin):
        emoji = ['🤚','✌','✊']
        #코인 db
        user_data = await self.db.user.find_one({"discordId": ctx.author.id})
        user_coin = int(user_data['coin'])
        
        #가위바위보 비교
        if coin == '반띵': coin = round(user_coin / 2)
        if coin == '올인': coin = user_coin
        if user_coin < int(coin) : return await ctx.reply(embed=utils.normal_embed('코인부족', f'코인이 {int(coin) - user_coin}만큼 부족합니다.', ctx.author))
        if int(coin) < 100: return await ctx.reply(embed=utils.normal_embed('코인부족', '100코인 이상부터 가능합니다', ctx.author))
        
        coin = int(coin)
        num = int(str(random.choices(range(2, 6), weights=[70,20,7,3]))[1])

        embed = discord.Embed(title='가위바위보', description=f'걸은 코인 : {coin}코인', color=config.embed_color)
        embed.add_field(name='가위/바위/보 내기', value='아래 리액션을 선택해주세요', inline=False)
        msg = await ctx.send(embed=embed)

        for r in emoji: #emoji
            await msg.add_reaction(r)

        async def embeded(stat, use, give):
            value = f'{use} {ctx.author.mention}\n VS \n {give} {self.bot.user.mention}'
            edit_embed = discord.Embed(title='가위바위보', description='', color=config.embed_color)
            if stat == '승리': 
                edit_embed.add_field(name=f'{stat} / {coin * num}코인을 얻었습니다', value=value,inline=False)
                await self.db.user.find_one_and_update({"discordId" : ctx.author.id}, {"$inc" : {"coin" : coin}})
            elif stat == '무승부': edit_embed.add_field(name=f'{stat}', value=value,inline=False)
            elif stat == '패배': 
                edit_embed.add_field(name=f'{stat} / {coin}코인을 잃었습니다', value=value,inline=False)
                await self.db.user.find_one_and_update({"discordId" : ctx.author.id}, {"$set" : {"coin" : int(user_coin - coin)}})

            return edit_embed
        
        def check(reaction, user):
            return str(reaction) in emoji and user == ctx.author and reaction.message.id == msg.id
        try: reaction, _user = await self.bot.wait_for("reaction_add", check=check, timeout=5.0)
        except asyncio.TimeoutError: await ctx.send("시간이 초과되었습니다.")
        else:
            if str(reaction) == '🤚':
                rando = str(random.choices(emoji, weights=[20,50,30]))[2]
                await msg.delete()
                if rando  == '🤚': return await ctx.send(embed=await embeded('무승부', reaction, '🤚'))
                elif rando  == '✌': return await ctx.send(embed=await embeded('패배', reaction, '✌'))
                elif rando  == '✊': return await ctx.send(embed=await embeded('승리', reaction, '✊'))
            if str(reaction) == '✌':
                rando = str(random.choices(emoji, weights=[30,20,50]))[2]
                await msg.delete()
                if rando  == '🤚': return await ctx.send(embed=await embeded('승리', reaction, '🤚'))
                elif rando  == '✌': return await ctx.send(embed=await embeded('무승부', reaction, '✌'))
                elif rando  == '✊': return await ctx.send(embed=await embeded('패배', reaction, '✊'))
            if str(reaction) == '✊':
                rando = str(random.choices(emoji, weights=[50,30,20]))[2]
                await msg.delete()
                if rando  == '🤚':return await ctx.send(embed=await embeded('패배', reaction, '🤚'))
                elif rando  == '✌':return await ctx.send(embed=await embeded('승리', reaction, '✌'))
                elif rando  == '✊':return await ctx.send(embed=await embeded('무승부', reaction, '✊'))

    @commands.command()
    async def 랜덤뽑기(self, ctx):

        user_data = await self.db.user.find_one({"discordId": ctx.author.id})
        user_coin = int(user_data['coin'])

        choice = [0, 200, 500 , 1000, 2000, 5000, 10000, 100000]
        num = random.choices(choice, weights=[50,25,15,4,3,2,0.999,0.001])[0]

        if 500 > user_coin:
            return await ctx.send('500코인이 필요')

        await self.db.user.find_one_and_update({"discordId" : ctx.author.id}, {"$set" : {"coin" : user_coin - 300}})

        if int(num) == 0: await ctx.send('0코인을 뽑았습니다.')
        elif int(num) == 200:
            await ctx.send(embed=utils.normal_embed('랜덤 뽑기', '200코인을 뽑았습니다.', author=ctx.author))
            await self.db.user.find_one_and_update({"discordId" : ctx.author.id}, {"$inc" : {"coin" : 200}})
        elif int(num) == 500:
            await ctx.send(embed=utils.normal_embed('랜덤 뽑기', '500코인을 뽑았습니다.', author=ctx.author))
            await self.db.user.find_one_and_update({"discordId" : ctx.author.id}, {"$inc" : {"coin" : 500}})
        elif int(num) == 1000:
            await ctx.send(embed=utils.normal_embed('랜덤 뽑기', '1,000코인을 뽑았습니다.', author=ctx.author))
            await self.db.user.find_one_and_update({"discordId" : ctx.author.id}, {"$inc" : {"coin" : 1000}})
        elif int(num) == 2000:
            await ctx.send(embed=utils.normal_embed('랜덤 뽑기', '2,000코인을 뽑았습니다.', author=ctx.author))
            await self.db.user.find_one_and_update({"discordId" : ctx.author.id}, {"$inc" : {"coin" : 2000}})
        elif int(num) == 5000:
            await ctx.send(embed=utils.normal_embed('랜덤 뽑기', '5,000코인을 뽑았습니다.', author=ctx.author))
            await self.db.user.find_one_and_update({"discordId" : ctx.author.id}, {"$inc" : {"coin" : 5000}})
        elif int(num) == 10000:
            await ctx.send(embed=utils.normal_embed('랜덤 뽑기', '10,000코인을 뽑았습니다.', author=ctx.author))
            await self.db.user.find_one_and_update({"discordId" : ctx.author.id}, {"$inc" : {"coin" : 10000}})
        elif int(num) == 100000:
            await ctx.send(embed=utils.normal_embed('랜덤 뽑기', '100,000코인을 뽑았습니다.', author=ctx.author))
            await self.db.user.find_one_and_update({"discordId" : ctx.author.id}, {"$inc" : {"coin" : 100000}})


def setup(bot):
    bot.add_cog(Core(bot))