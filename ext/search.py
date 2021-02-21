import urllib, urllib.parse, requests
from urllib.request import Request
from bs4 import BeautifulSoup
import discord, asyncio
from discord.ext import commands, tasks
import config, utils

hdr = { 'User-Agent': ('Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Mobile Safari/537.36')}

async def google_search(search_name):
    encode = urllib.parse.quote_plus(search_name.replace(' ','+'))
    url = f"https://www.google.com/search?q={encode}"
    html = requests.get(url, headers=hdr).content
    soup = BeautifulSoup(html, 'html.parser')

    hylink = []
    result = []
    result_ex = []
    
    for ab in soup.findAll('div', {'class' :'mnr-c xpd O9g5cc uUPGi'}):
        hylink.append(ab.find('a', {'class' : 'C8nzq BmP5tf'}).get('href')) #링크
        result.append(ab.find('div', {'class':'V7Sr0 p5AXld gsrt PpBGzd YcUVQe'}).text) # 제목
        if not ab.find('div', {'class':'MUxGbd yDYNvb'}) == None: #내용 감지
            result_ex.append(ab.find('div', {'class':'MUxGbd yDYNvb'}).text) # 내용
        else: 
            hylink.remove(ab.find('a', {'class' : 'C8nzq BmP5tf'}).get('href')) #링크 없애기
            result.remove(ab.find('div', {'class':'V7Sr0 p5AXld gsrt PpBGzd YcUVQe'}).text) # 제목 없애기
        if len(result) >= 5: break

    return {
        'links' : hylink,
        'result' : result,
        'result_ex' : result_ex
    }

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='검색')
    async def embeded(self, ctx , * , search_names):
        
        res = await google_search(search_names)
        hylink = res['links']
        result = res['result']
        result_ex = res['result_ex']
        
        embed = discord.Embed(title=f'{search_names} 검색 결과', description='최상위 5개 검색결과',color=0xfcd1d1)
        num = int(len(hylink))
        for i in range(0, num):
            embed.add_field(name=f"{result[i]}", 
                            value=f"[link]({hylink[i]}) \n {result_ex[i]}", inline=False)
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Core(bot))