import json, discord
from discord.ext import commands, tasks


async def account(user_id):
    with open('coins.json', 'r') as f:
        j = json.load(f)

    j[str(user_id)] = 1000

    with open('coins.json', 'w') as outfile:
        json.dump(j, outfile, indent=4)


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def 코인(self, ctx):
        try:
            with open('coins.json', 'r') as f: j = json.load(f)
            
            await ctx.send(f'{ctx.author.mention}님은\n{j[str(ctx.author.id)]} 코인을 보유중입니다')

        except KeyError:
            await account(ctx.author.id)
            await ctx.send(f'{ctx.author.mention}님의 계좌가 만들어져\n50코인이 자동지급되었습니다.')
        except ValueError:
            await ctx.send(f'`게임아 코인 (코인 양) *다른사람 조회시*(@맨션)`\n 양식으로 보내야 합니다')

    @commands.command()
    async def 송금(self, ctx, arg, user):
        try:
            arg = int(arg)
            with open('coins.json', 'r') as f: j = json.load(f)

            if arg < 100:
                await ctx.send(f'100코인 이상부터 보낼수 있습니다')
                return
            if arg > j[str(ctx.author.id)]:
                await ctx.send(f'{int(arg)-j[str(ctx.author.id)]}코인이 부족합니다')
                return
            j[str(ctx.author.id)] -= 200
            j[str(user.id)] += arg

            with open('coins.json', 'w') as outfile: json.dump(j, outfile, indent=4)

            await ctx.send(f'{user.mention}님에게 {arg}코인을 보냈습니다')
        except ValueError:
            await ctx.send(f'`게임아 돈보내기 (코인 양) (@맨션)`\n 양식으로 보내야 합니다')
        except KeyError:
            await account(ctx.author.id)
            await ctx.send(f'{ctx.author.mention}님의 계좌가 만들어져\n50코인이 자동지급되었습니다.')

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def 코인줘(self, ctx):
        try:
            with open('coins.json', 'r') as f:
                j = json.load(f)

            j[str(ctx.author.id)] += 200

            with open('coins.json', 'w') as outfile:
                json.dump(j, outfile, indent=4)

            await ctx.send('200코인을 계좌에 지급했습니다.')
            
        except KeyError:
            await account(ctx.author.id)
            await ctx.send(f'{ctx.author.mention}님의 계좌가 만들어져\n50코인이 자동지급되었습니다.')