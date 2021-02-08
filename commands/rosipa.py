import discord, random, json, asyncio, math
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
    async def 가위(self, ctx, arg):
        try:
            with open('coins.json', 'r') as f:
                j = json.load(f)

            if arg == '반띵':
                arg = round(j[str(ctx.author.id)] / 2)

            if arg == '올인':
                arg = j[str(ctx.author.id)]

            if int(arg) < 100:
                await ctx.send('100코인 이상부터')
                return

            if int(arg) > int(j[str(ctx.author.id)]):
                await ctx.send(f'코인이 {int(arg)-j[str(ctx.author.id)]}만큼 필요')
                return

            emoji = ['🤚','✌','✊']
            rando = str(random.choices(emoji, weights=[30,20,50]))[2]
            num = str(random.choices(range(2, 6), weights=[70,20,7,3]))[1]

            await asyncio.sleep(1)

            if rando  == '🤚':
                j[str(ctx.author.id)] += int(arg)*int(num)
                await ctx.send(f'''{ctx.author.mention} ✌ VS 🤚 \n이김.\n {arg}코인의 {num}배를 얻음. \n`+{int(arg)*int(num)}`''')
            if rando  == '✌':
                await ctx.send(f'''{ctx.author.mention} ✌ VS ✌ \n비김.''')
            if rando  == '✊':
                j[str(ctx.author.id)] -= int(arg)
                await ctx.send(f'''{ctx.author.mention} ✌ VS ✊ \n짐. \n`-{arg}`''')

            with open('coins.json', 'w') as outfile:
                json.dump(j, outfile, indent=4)
        except KeyError:
            await account(ctx.author.id)
            await ctx.send(f'{ctx.author.mention}님의 계좌가 만들어져\n50코인이 자동지급되었습니다.')
        except ValueError:
            await ctx.send('(가위바위보 숫자 또는 올인, 반띵) 꼴로 써야함')

    @commands.command()
    async def 바위(self, ctx, arg):
        try:
            with open('coins.json', 'r') as f:
                j = json.load(f)
            if arg == '반띵':
                arg = round(j[str(ctx.author.id)] / 2)
            if arg == '올인':
                arg = j[str(ctx.author.id)]          
            if int(arg) < 100:
                await ctx.send('100코인 이상부터')
                return
            if int(arg) > int(j[str(ctx.author.id)]):
                await ctx.send(f'코인이 {int(arg)-j[str(ctx.author.id)]}만큼 필요')
                return           
            emoji = ['🤚','✌','✊']
            rando = str(random.choices(emoji, weights=[50,30,20]))[2]
            num = str(random.choices(range(2, 6), weights=[70,20,7,3]))[1]
            await asyncio.sleep(1)
            if rando  == '🤚':
                j[str(ctx.author.id)] -= int(arg)
                await ctx.send(f'''{ctx.author.mention} ✊ VS 🤚 \n짐. \n`-{arg}`''')
            if rando  == '✌':
                j[str(ctx.author.id)] += int(arg)*int(num)
                await ctx.send(f'''{ctx.author.mention} ✊ VS ✌ \n이김.\n {arg}코인의 {int(num)}배를 얻음. \n`+{int(arg)*int(num)}`''')
            if rando  == '✊':
                await ctx.send(f'''{ctx.author.mention} ✊ VS ✊ \n비김.''')
            with open('coins.json', 'w') as outfile:
                    json.dump(j, outfile, indent=4)
        except KeyError:
            await account(ctx.author.id)
            await ctx.send(f'{ctx.author.mention}님의 계좌가 만들어져\n50코인이 자동지급되었습니다.')
        except ValueError:
            await ctx.send('(가위바위보 숫자 또는 올인, 반띵) 꼴로 써야함')

    @commands.command()
    async def 보(self, ctx, arg):
        try: 
            with open('coins.json', 'r') as f:
                j = json.load(f)

            if arg == '반띵':
                arg = round(j[str(ctx.author.id)] / 2)

            if arg == '올인':
                arg = j[str(ctx.author.id)]
            
            if int(arg) < 100:
                await ctx.send('100코인 이상부터')
                return

            if int(arg) > int(j[str(ctx.author.id)]):
                await ctx.send(f'코인이 {int(arg)-j[str(ctx.author.id)]}만큼 필요')
                return
            
            emoji = ['🤚','✌','✊']
            rando = str(random.choices(emoji, weights=[20,50,30]))[2]
            num = str(random.choices(range(2, 6), weights=[70,20,7,3]))[1]

            await asyncio.sleep(1)

            if rando  == '🤚':
                await ctx.send(f'''{ctx.author.mention} 🤚 VS 🤚 \n비김''')
            if rando  == '✌':
                j[str(ctx.author.id)] -= int(arg)
                await ctx.send(f'''{ctx.author.mention} 🤚 VS ✌ \n짐.\n`-{arg}`''')
            if rando  == '✊':
                j[str(ctx.author.id)] += int(arg)*int(num)
                await ctx.send(f'''{ctx.author.mention} 🤚 VS ✊ \n이김.\n {arg}코인의 {int(num)}배를 얻음. \n+`{int(arg)*int(num)}`''')
        
            with open('coins.json', 'w') as outfile:
                json.dump(j, outfile, indent=4)

        except KeyError:
            await account(ctx.author.id)
            await ctx.send(f'{ctx.author.mention}님의 계좌가 만들어져\n50코인이 자동지급되었습니다.')

        except ValueError:
            await ctx.send('(가위바위보 숫자 또는 올인, 반띵) 꼴로 써야함')
