import discord
from discord.commands import Option
from discord.ui import View, InputText, Modal

from hcskr import asyncSelfCheck
import json

from os import listdir
from sys import exit

try:
    from setting import token, owner, guild, hcs_path, ImageDict
    BOT_token = token
    file_path = hcs_path
except:
    print("=========================")
    print("[ setting.py ] 에서 정보를 불러오지 못했습니다.")
    print()
    print("환경변수가 제대로 작성되어있는지 확인해주세요")
    print("=========================") 
    exit()


bot = discord.Bot()


@bot.event # 봇 작동
async def on_ready():
    print("=========================")
    print("아래의 계정으로 로그인 : ")
    print(bot.user.name)
    print("연결에 성공했습니다.")
    print("=========================")
    await bot.change_presence(activity=discord.Game("/가이드"))

for filename in listdir('./cogs'): # Cogs 자동 로드(봇 작동시)
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'{filename[:-3]}가 정상적으로 로드되었습니다.')



@bot.slash_command(description="봇 도움말 확인")
async def 도움말(ctx):
    Help_Embed = discord.Embed(title=f"{bot.user.name} 도움말", description=f"­", colour=0xffdc16)
    Help_Embed.add_field(name=f"자가진단 정보 입력하기 ⠀⠀⠀⠀", value=f":small_blue_diamond: /자가진단 등록", inline=True)
    Help_Embed.add_field(name=f"자가진단 정보 삭제하기 ", value=f":small_blue_diamond: /자가진단 삭제", inline=True)
    Help_Embed.add_field(name="­", value=f"­", inline=True)
    Help_Embed.add_field(name=f"자가진단 실행하기 ⠀⠀⠀⠀", value=f":small_blue_diamond: /자가진단 실행", inline=True)
    Help_Embed.add_field(name=f"자가진단 예약하기", value=f":small_blue_diamond: /자가진단 예약", inline=True)
    Help_Embed.add_field(name="­", value=f"­", inline=True)
    Help_Embed.add_field(name="­", value=f"­", inline=False)
    Help_Embed.add_field(name="자가진단 매크로 등록 방법을 모른다면?", value=f":small_blue_diamond: /가이드", inline=False)
    Help_Embed.set_thumbnail(url=bot.user.display_avatar)
    await ctx.respond(embed=Help_Embed)


@bot.slash_command(description="자가진단 자동화 등록 가이드")
async def 가이드(ctx):
    guide = discord.Embed(title=f"자가진단 자동화 등록 가이드", description=f"­", colour=0xffdc16)
    guide.add_field(name=f"1. 자신의 정보 입력하기", value="`/자가진단 등록`으로 자신의 정보를 입력합니다.", inline=False)
    guide.add_field(name=f"2. 자가진단 예약하기", value="`/자가진단 예약`을 입력시 앞으로 매일 오전 7~7시 10분 사이 자가진단을 진행합니다.", inline=False)
    guide.add_field(name=f"3. 자가진단 예약 해제하기", value="`/자가진단 예약`을 다시 입력하시면 자동 자가진단이 종료됩니다.", inline=False)
    guide.add_field(name=f"4. 지금 자가진단하기", value=f"`/자가진단 실행`을 입력하면 지금 자가진단을 진행합니다.", inline=False)
    guide.set_thumbnail(url=bot.user.display_avatar)
    await ctx.respond(embed=guide)


@bot.command(description="봇 레이턴시 확인")
async def ping(ctx):
    ping = discord.Embed(title="Pong!", description=f"딜레이: {round(bot.latency * 1000)}ms 초", colour=0xffdc16)
    await ctx.respond(embed=ping)


@bot.command(description=f"봇에 대한 정보를 출력합니다.")
async def 정보(ctx):
    try:
        users = json.load(open(hcs_path,encoding="utf_8"))['users']
    except:
        users = "Erorr"

    bot_info = discord.Embed(title=bot.user.name, color=0xffdc16)
    bot_info.add_field(name="핑", value=f'`{round(bot.latency * 1000)}ms`', inline=True)
    bot_info.add_field(name='봇 접두사', value='`/{명령어}`', inline=True)
    bot_info.add_field(name="­", value="­", inline=True)
    bot_info.add_field(name="연결된 서버 수⠀⠀⠀", value=f'`{len(bot.guilds)}개 서버`', inline=True)
    bot_info.add_field(name="이용중인 유저 수", value=f'`{users}명`', inline=True)
    bot_info.add_field(name="­", value="­", inline=True)
    bot_info.add_field(name="개발 언어", value="Python [Pycord](https://docs.pycord.dev/en/master/)", inline=True)
    bot_info.add_field(name='GitHub', value='[Bot GitHub](https://github.com/justhuman1008/JustBot)', inline=True)
    bot_info.add_field(name="호스팅", value="Galaxy S9 UserLAnd", inline=True)
    bot_info.add_field(name="소유자", value=f"{owner}", inline=False)
    bot_info.set_thumbnail(url=bot.user.display_avatar)
    await ctx.respond(embed=bot_info)

@bot.command(description=f"봇 초대링크")
async def invite(ctx):
    invitelink = f"https://discord.com/oauth2/authorize?client_id={bot.application_id}&permissions=412317142080&scope=bot%20applications.commands"

    invite = discord.Embed(title=f"{bot.user.name} 초대하기", description=f"[봇 초대하기]({invitelink})", colour=0xffdc16)
    invite.set_thumbnail(url=bot.user.display_avatar)

    view = View()
    button = discord.ui.Button(label="봇 초대하기", url=invitelink, emoji="✉️")
    view.add_item(button)

    await ctx.respond(embed=invite,view=view)

@bot.slash_command(guild_ids=[guild], description="봇에서 유저 DB를 다운받습니다.")
async def db다운(ctx):
    await ctx.respond(file=discord.File(hcs_path))

#=================================================================================================================================
#=================================================================================================================================
#=================================================================================================================================


def is_register(DiscordID):
    with open(file_path, "r", encoding="utf_8") as json_file:
        contents = json_file.read()
        json_data = json.loads(contents)
    try:
        a=json_data[f'{DiscordID}']
        return True
    except:
        return False


def add_info(Nickname, DiscordID, Name, Birthday, Area, School, School_lv, Password):
    register = is_register(DiscordID)
    if register:
        return

    data = {}
    with open(file_path, "r", encoding="utf_8") as json_file:
        data = json.load(json_file)

    data[f'{DiscordID}'] = []
    data[f'{DiscordID}'].append({
        "Nickname": f"{Nickname}",
        "DiscordID": f"{DiscordID}",
        "Name": f"{Name}",
        "Birthday": f"{Birthday}",
        "Area": f"{Area}",
        "School": f"{School}",
        "School_lv": f"{School_lv}",
        "Password": f"{Password}",
        "Auto_check": f"X"})

    with open(file_path, 'w',encoding="utf_8") as writefile:
        json.dump(data, writefile, indent="\t", ensure_ascii=False)


def delete_info(DiscordID):
    register = is_register(DiscordID)
    if register:
        with open(file_path, "r", encoding="utf_8") as json_file:
            contents = json_file.read()
            json_data = json.loads(contents)

        json_data.pop(f'{DiscordID}')
        
        with open(file_path, 'w',encoding="utf_8") as writefile:
            json.dump(json_data, writefile, indent="\t", ensure_ascii=False)

        return True
    else:
        return False


@bot.slash_command(description="교육부 자가진단을 진행합니다.")
async def 자가진단(ctx, 작업:Option(str,"다음 중 하나를 선택하세요.", choices=["실행", "예약", "등록", "삭제"])):

    errorlist = {"FORMET":"존재하지 않는 지역, 학교급", "NOSCHOOL":"학교 검색 실패", "NOSTUDENT":"학생 검색 실패", "UNKNOWN":"알 수 없는 에러"}
    TrueFalse = is_register(ctx.author.id)
    UserID = str(ctx.author.id)

    not_registered = discord.Embed(title="등록되지 않은 사용자입니다.", description="해당 기능을 이용하시려면 `/자가진단 등록`을 입력해주세요", color=0xffdc16)
    not_registered.set_thumbnail(url=ImageDict["List"])

    if 작업 == "실행":
        if TrueFalse:
            with open(file_path, "r", encoding="utf_8") as json_file:
                json_data = json.load(json_file)
            #print(json_data[UserID][0])
            Name = json_data[UserID][0]['Name']
            Birthday = json_data[UserID][0]['Birthday']
            Area = json_data[UserID][0]['Area']
            School = json_data[UserID][0]['School']
            School_lv = json_data[UserID][0]['School_lv']
            Password = json_data[UserID][0]['Password']


            hcskr_result = await asyncSelfCheck(Name, Birthday, Area, School, School_lv, Password)
            if hcskr_result['code'] == 'SUCCESS':

                Success = discord.Embed(title="자가진단이 완료되었습니다.", description=f'완료시각: {hcskr_result["regtime"]}', color=0xffdc16)
                Success.set_thumbnail(url=ImageDict["hcs_icon"])
                await ctx.respond(embed=Success)

            else:

                error_reason = errorlist[hcskr_result['code']]
                fail = discord.Embed(title="자가진단이 실패했습니다.", description=f'사유: {error_reason}', color=0xffdc16)
                fail.set_thumbnail(url=ImageDict["hcs_icon"])
                await ctx.respond(embed=fail)
        else:
            await ctx.respond(embed=not_registered)


    if 작업 == "삭제":
        Delete = discord.Embed(title=f"{bot.user.name} 자가진단", description="­", color=0xffdc16)
        Delete.add_field(name="진단정보 제거시 `/자가진단 진행`을 사용할 수 없습니다.", value="자가진단 정보를 제거하시려면 `1분`내로 ✅를 클릭해주세요.", inline=False)
        Delete.set_thumbnail(url=ImageDict["Trash_can"])

        Delete_Failed = discord.Embed(title="진단정보 삭제가 취소되었습니다", description="­자가진단 정보를 삭제하시려면 다시 `/자가진단 삭제`를 입력해주세요.", color=0xffdc16)
        Delete_Failed.set_thumbnail(url=ImageDict["Trash_can"])

        if TrueFalse:
            class Button(discord.ui.View):
                @discord.ui.button(style=discord.ButtonStyle.green, emoji="✅")
                async def OK(self, button: discord.ui.Button, interaction: discord.Interaction):
                    TrueFalse = delete_info(ctx.author.id)
                    if TrueFalse:
                        Delete_Success = discord.Embed(title=f"{ctx.author.name}님의 진단정보 삭제가 완료되었습니다.", description="추후 자가진단을 진행하시려면 다시 `/자가진단 등록`을 입력해주세요", color=0xffdc16)
                        Delete_Success.set_thumbnail(url=ImageDict["Trash_can"])
                        await Question.edit_original_message(embed=Delete_Success, view=None)

                @discord.ui.button(style=discord.ButtonStyle.red, emoji="⛔")
                async def Nope(self, button: discord.ui.Button, interaction: discord.Interaction):
                    await Question.edit_original_message(embed=Delete_Failed, view=None)

                async def on_timeout(self):
                    await Question.edit_original_message(embed=Delete_Failed, view=None)

            Question = await ctx.respond(embed=Delete, view=Button(timeout=60))
        else:
            await ctx.respond(embed=not_registered)


    if 작업 == "등록":
        register = discord.Embed(title=f"{bot.user.name} 자가진단", description="­자가진단 정보 입력시  `자가진단용 정보가 저장`되어\n`/자가진단 진행`을 사용할 수 있습니다.", color=0xffdc16)
        register.add_field(name="­", value="❗ 자가진단 정보를 확인하기 위해 `1회 자가진단이 진행됩니다.`\n\n자가진단 정보를 입력하시려면 `1분`내로 ✅를 클릭해주세요.", inline=False)
        register.set_thumbnail(url=ImageDict["List"])

        Register_Failed = discord.Embed(title="자가진단 등록이 취소되었습니다.", description="­자가진단 정보를 입력하시려면 다시 `/자가진단 등록`을 입력해주세요", color=0xffdc16)
        Register_Failed.set_thumbnail(url=ImageDict["List"])

        if TrueFalse:
            Register_Already = discord.Embed(title="이미 정보가 입력되어 있습니다.", description="­자가진단 정보를 삭제하시려면 `/자가진단 삭제`를 입력해주세요", color=0xffdc16)
            Register_Already.set_thumbnail(url=ImageDict["List"])
            await ctx.respond(embed=Register_Already)
        else:
            class infoQ(Modal):
                def __init__(self) -> None:
                    super().__init__("자가진단 정보 입력하기")
                    self.add_item(InputText(label="이름",placeholder="본인의 본명을 입력해주세요.",max_length=30))
                    self.add_item(InputText(label="생년월일",placeholder="6자리 생년월일을 작성해주세요. (ex 051010)",max_length=6))
                    self.add_item(InputText(label="지역",placeholder="학교가 속한 지역을 작성해주세요. (ex 부산)",max_length=30))
                    self.add_item(InputText(label="학교명",placeholder='학교의 이름을 "정확히" 작성해주세요. (ex 부산중학교)',max_length=30))
                    self.add_item(InputText(label="비밀번호",placeholder="자가진단 비밀번호를 작성해주세요.",max_length=4))

                async def callback(self, interaction:discord.Interaction):
                    if self.children[3].value.find("고등학교") > -1:
                        School_lv = "고등학교"
                    elif self.children[3].value.find("중학교") > -1:
                        School_lv = "중학교"
                    elif self.children[3].value.find("초등학교") > -1:
                        School_lv = "초등학교"
                    elif self.children[3].value.find("특수학교") > -1:
                        School_lv = "특수학교"

                    Name = self.children[0].value
                    Birthday = self.children[1].value
                    Area = self.children[2].value
                    School = self.children[3].value
                    Password = self.children[4].value
                    
                    #print(Name,Birthday,Area,School,Password,School_lv)
                    class Button(discord.ui.View):
                        @discord.ui.button(style=discord.ButtonStyle.green, emoji="✅")
                        async def OK(self, button: discord.ui.Button, interaction: discord.Interaction):
                            try:
                                hcskr_result = await asyncSelfCheck(Name, Birthday, Area, School, School_lv, Password)
                                if hcskr_result['code'] == 'SUCCESS':
                                    add_info(ctx.author.name, ctx.author.id, Name, Birthday, Area, School, School_lv, Password)

                                    Register_Success = discord.Embed(title=f"{ctx.author}님의 자가진단 정보 입력이 완료되었습니다.", description="`/자가진단 진행`으로 자가진단을 진행할 수 있습니다.",color=0xffdc16)
                                    Register_Success.set_thumbnail(url=ImageDict["List"])
                                    await Question.edit_original_message(embed=Register_Success, view=None)
                                    print(f"{ctx.author}님의 자가진단 정보가 입력되었습니다.")
                                    return
                                else:
                                    error_reason = errorlist[hcskr_result['code']]
                                    Register_Test_Fail = discord.Embed(title=f"{ctx.author}님의 자가진단 정보 입력이 실패하였습니다.", description=f"입력된 오류: {error_reason}",color=0xffdc16)
                                    Register_Test_Fail.set_thumbnail(url=ImageDict["List"])
                                    await Question.edit_original_message(embed=Register_Test_Fail, view=None)
                                    return
                            except:
                                error_reason = errorlist[hcskr_result['code']]
                                Failed_reg = discord.Embed(title="자가진단 정보 등록에 실패했습니다.", description=f'정보를 모두 "정확히" 입력했는지 확인해주세요\n 입력된 오류: {error_reason}', color=0xffdc16)
                                Failed_reg.set_thumbnail(url=ImageDict["List"])
                                await Question.edit_original_message(embed=Failed_reg)
                                return
                            
                        @discord.ui.button(style=discord.ButtonStyle.red, emoji="⛔")
                        async def Nope(self, button: discord.ui.Button, interaction: discord.Interaction):
                            await Question.edit_original_message(embed=Register_Failed, view=None)

                        async def on_timeout(self):
                            await Question.edit_original_message(embed=Register_Failed, view=None)

                    Question = await interaction.response.send_message(embed=register,view=Button(timeout=60))
            await ctx.interaction.response.send_modal(infoQ())

    if 작업 == "예약":
        if TrueFalse:
            with open(file_path, "r", encoding="utf_8") as json_file:
                json_data = json.load(json_file)

            if json_data[UserID][0]['Auto_check'] == "O":
                json_data[UserID][0]['Auto_check'] = "X"

                Auto_off = discord.Embed(title=f"{bot.user.name} 자가진단 매크로", description="­이제부터 자동 자가진단이 종료됩니다.", color=0xffdc16)
                Auto_off.set_thumbnail(url=ImageDict["hcs_icon"])
                await ctx.respond(embed=Auto_off)

            else:
                json_data[UserID][0]['Auto_check'] = "O"

                Auto_on = discord.Embed(title=f"{bot.user.name} 자가진단 매크로", description="­이제부터 자가진단이 매일 오전 7시 ~ 7시 10분 사이에 진행됩니다.", color=0xffdc16)
                Auto_on.set_thumbnail(url=ImageDict["hcs_icon"])
                await ctx.respond(embed=Auto_on)


            with open(file_path, 'w',encoding="utf_8") as writefile:
                json.dump(json_data, writefile, indent="\t", ensure_ascii=False)
        else:
            await ctx.respond(embed=not_registered)
            return

@bot.slash_command(guild_ids=[guild], description="자가진단 정보를 강제로 입력합니다[관리자 한정]")
async def 강제추가(ctx, 디스코드닉네임, 디스코드id, 이름, 생년월일, 지역, 학교명, 비밀번호, 예약유무:Option(str,"다음 중 하나를 선택하세요.", choices=["O", "X"])):
    try:
        if 학교명.find("고등학교") > -1:
            School_lv = "고등학교"
        elif 학교명.find("중학교") > -1:
            School_lv = "중학교"
        elif 학교명.find("초등학교") > -1:
            School_lv = "초등학교"
        elif 학교명.find("특수학교") > -1:
            School_lv = "특수학교"

        add_info(디스코드닉네임, 디스코드id, 이름, 생년월일, 지역, 학교명, School_lv, 비밀번호)

        with open(file_path, "r", encoding="utf_8") as json_file:
            json_data = json.load(json_file)
            
        if 예약유무 == "O":
            json_data[디스코드id][0]['Auto_check'] = "O"
        else:
            json_data[디스코드id][0]['Auto_check'] = "X"

        with open(file_path, 'w',encoding="utf_8") as writefile:
            json.dump(json_data, writefile, indent="\t", ensure_ascii=False)
        await ctx.respond("입력 성공")
    except:
        await ctx.respond("입력 실패")

bot.run(BOT_token)