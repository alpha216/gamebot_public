import discord, json, re, random
from discord.ext import commands, tasks

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def 랜덤뽑기(self, ctx):

        with open('coins.json', 'r') as f: j = json.load(f)

        choice = [0, 200, 500 , 1000, 2000, 5000, 10000, 100000]
        num = re.findall("\\d+", str(random.choices(choice, weights=[50,25,15,4,3,2,0.999,0.001])))[0]

        if 500 > int(j[str(ctx.author.id)]):
            await ctx.send('500코인이 필요')
            return

        j[str(ctx.author.id)]-= 500

        if int(num) == 0:
            await ctx.send('0코인을 뽑았습니다.')
        if int(num) == 200:
            await ctx.send('200코인을 뽑았습니다.')
            j[str(ctx.author.id)] += 200
        if int(num) == 500:
            await ctx.send('500코인을 뽑았습니다.')
            j[str(ctx.author.id)] += 500
        if int(num) == 1000:
            await ctx.send('1,000코인을 뽑았습니다.')
            j[str(ctx.author.id)] += 1000
        if int(num) == 2000:
            await ctx.send('2,000코인을 뽑았습니다.')
            j[str(ctx.author.id)] += 2000
        if int(num) == 5000:
            await ctx.send('5,000코인을 뽑았습니다.')
            j[str(ctx.author.id)] += 5000
        if int(num) == 10000:
            await ctx.send('10,000코인을 뽑았습니다.')
            j[str(ctx.author.id)] += 10000
        if int(num) == 100000:
            await ctx.send('100,000코인을 뽑았습니다.')
            j[str(ctx.author.id)] += 100000

        with open('coins.json', 'w') as outfile: json.dump(j, outfile, indent=4)
