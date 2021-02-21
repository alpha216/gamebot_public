import discord, re, urllib
from urllib.request import Request, urlopen, HTTPError
from bs4 import BeautifulSoup
from discord.ext import commands, tasks

hdr = {'Accept-Language': 'ko_KR,en;q=0.8', 'User-Agent': (
    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Mobile Safari/537.36')}

class Record(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #롤 전적
    @commands.command(name='롤')
    async def LOL_record(self, ctx, *, nickname:str):
        # 불러오기, 기본
        url = f"https://www.op.gg/summoner/userName={nickname.replace(' ','+')}"
        html = urlopen(Request(url, headers=hdr))
        soup = BeautifulSoup(html, 'html.parser')
        Container = {}

        try:
            # 내용 불러오기
            Container['src'] = soup.find("div", {"class" : "ProfileIcon"}).find('img').get('src').replace('//', 'https://')
            Container['Name'] = soup.find("div", {"class" : "SummonerName"}).text 
            Container['levels'] = soup.find('span', {'title': '레벨'}).text
            Container['tier'] = soup.find('div', {'class' : 'Tier'}).text.replace('\n', '').replace('\t', '')
            Container['win'] = soup.find('span', {'class': 'win'}).text
            Container['lose'] = soup.find('span', {'class': 'lose'}).text
            Container['winratio'] = soup.find('b', {'class': 'WinRatio'}).text
            #임베드
            embed = discord.Embed(title='롤 전적 조회', description= "", color=0xd1373a) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
            embed.set_thumbnail(url=str(Container['src']))
            embed.add_field(name="이름", value= Container['Name'], inline=True)
            embed.add_field(name="레벨", value= Container['levels'] + ' 레벨', inline=True)
            embed.add_field(name="티어", value= Container['tier'], inline=True)
            embed.add_field(name="최근 20게임", value= Container['win'] + ' 승 / ' + Container['lose'] + ' 패 / 승률 ' + Container['winratio'], inline=True)
            embed.set_footer(text="OP.GG에서 검색") # 하단에 들어가는 조그마한 설명을 잡아줍니다

            await ctx.send(embed=embed)
        except AttributeError:
            embed = discord.Embed(title='이런!', description= '조회중 오류가 났습니다.', color=0xd1373a) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
            embed.add_field(name="해결법", value= '저희 봇은 한국 서버 소환사만 지원합니다.', inline=True)
            embed.add_field(name="입력법", value= '게임아 롤 (소환사명)', inline=True)
            await ctx.send(embed=embed)

    #배그 솔랭
    @commands.command(name='배그')
    async def batleground_record(self, ctx, arg):
        try:
        #조회
            url = 'https://dak.gg/pubg/profile/' + arg
            html = urlopen(url)

            html = BeautifulSoup(html,'html.parser')

            img = html.find("div", {"class" : "userInfo"}).find('img').get('src')

            if re.search('kakao', img):
                img = img.replace('//', 'https://')

            solran = html.findAll('div',{'class' : re.compile('solo ranked [A-Za-z0-9]')})[0]
            sr = {}
            if solran.find('div',{'class' : 'no_record'}) != None:
                    sr['error'] = 'error'
            else:
                sr['stats'] = solran.find('p',{'class' : 'win-stats'}).text.strip() #최근 승 / 탑 / 패
                sr['ranking'] = solran.find('div',{'class' : 'rating'}).find('span',{'class' : 'value'}).text #티어
                img_rank = solran.find('img',{'class' : 'grade-icon'}).get('src').replace('//', 'https://')
                sr['rp'] = solran.find('div',{'class' : 'rating'}).find('span',{'class' : 'caption'}).text # rp / 배치 판수
                sr['k/da'] = solran.find('div',{'class' : 'kd stats-item stats-top-graph'}).find('p',{'class' : 'value'}).text.strip() #k/da
                sr['winper'] = solran.find('div',{'class' : 'winratio stats-item stats-top-graph'}).find('p',{'class' : 'value'}).text.strip().replace('\n', '')# 승률
                sr['top10'] = solran.find('div',{'class' : 'top10s stats-item stats-top-graph'}).find('p',{'class' : 'value'}).text.strip().replace('\n', '') # top10         
                sr['dill'] = solran.find('div',{'class' : 'deals stats-item stats-top-graph'}).find('p',{'class' : 'value'}).text.strip() # 평균 딜    
                sr['games'] = solran.find('div',{'class' : 'games stats-item stats-top-graph'}).find('p',{'class' : 'value'}).text.strip() #게임 수       
                sr['rank'] = solran.find('div',{'class' : 'avgRank stats-item stats-top-graph'}).find('p',{'class' : 'value'}).text.strip() # 평균 등수      

        #임베드
            embed = discord.Embed(title='', description= '', color=0xf3c421) # Embed의 기본 틀
            embed.set_author(name=arg, url=url, icon_url=img)

            #솔로 랭크
            if 'error' in sr:
                embed.add_field(name="솔로랭크", value= '기록 없음', inline=False) #오류
            else:
                embed.set_thumbnail(url=img_rank)
                embed.add_field(name="솔로 - 랭크 게임", value= sr['stats'], inline=False) # 전적

                if sr['ranking'] == '배치 중': RP = '판'  #배치 중 RP -> 판
                else: RP = 'RP'
                
                embed.add_field(name=sr['ranking'], value= sr['rp'] + " " + RP, inline=False) # 티어

                embed.add_field(name='K/DA', value= sr['k/da'], inline=True) # K/DA
                embed.add_field(name="승률", value= sr['winper'], inline=True) # 승률
                embed.add_field(name="Top 10", value= sr['top10'], inline=True) # Top 10

                embed.add_field(name="평균 딜량", value= sr['dill'], inline=True) # 평균 딜량
                embed.add_field(name="게임 수", value= sr['games'], inline=True) # 게임 수
                embed.add_field(name="평균 등수", value= sr['rank'], inline=True) # 평균 딜량
            await ctx.send(embed=embed)

        except HTTPError:
            embed = discord.Embed(title='이런!', description= '조회중 문제가 발생했습니다.', color=0xf3c421) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
            embed.add_field(name="해결법", value= '플레이어명을 재대로 입력했는지 확인해주세요.', inline=False)
            embed.add_field(name="입력법", value= '게임아 배그 (플레이어 명)', inline=True)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Record(bot))