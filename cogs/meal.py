import discord
from discord.ext import commands
from discord.commands import slash_command, Option

import requests
import datetime
import json

from setting import Neis_key, DB_path, ImageDict, Areas

#------------------------------------------------------------------------------------------

class MEAL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="우리학교의 오늘 점심 급식을 확인합니다.")
    async def 급식(self, ctx, 식사시간:Option(str,"다음 중 하나를 선택하세요. [기본값:점심]", choices=["아침", "점심", "저녁"])="점심"):

        meal_dic = {"아침":1, "점심":2, "저녁":3}
        meal_code =meal_dic[식사시간]
        UserID = str(ctx.author.id)
        try:
            with open(DB_path, "r", encoding="utf_8") as json_file:
                json_data = json.load(json_file)

            School = json_data[UserID][0]['School'] # 학교명
            School_lv = json_data[UserID][0]['School_lv'] # 학교분류
            day = datetime.datetime.now().strftime("%y%m%d") #오늘날짜
        except:
            not_registered = discord.Embed(title="등록되지 않은 사용자입니다.", description="해당 기능을 이용하시려면 `/자가진단 등록`을 입력해주세요", color=0xffdc16)
            not_registered.set_thumbnail(url=ImageDict["List_Failed"])
            return await ctx.respond(embed=not_registered)

        try:
            API_Main = "https://open.neis.go.kr/hub/schoolInfo?"
            API_String = f"KEY={Neis_key}&Type=json&pIndex=1&pSize=5&SCHUL_NM={School}&SCHUL_KND_SC_NM={School_lv}"
            API = API_Main + API_String

            SchoolAPI = requests.get(API).json()
            School_code = SchoolAPI['schoolInfo'][1]['row'][0]['SD_SCHUL_CODE']
            Moe_code = SchoolAPI['schoolInfo'][1]['row'][0]['ATPT_OFCDC_SC_CODE']

            Area = Areas[Moe_code][1]
        except:
            print(SchoolAPI)
            API1_error = discord.Embed(title="학교 검색에 실패했습니다.", description="-", color=0xffdc16)
            API1_error.set_thumbnail(url=ImageDict["List_Failed"])
            return await ctx.respond(embed=API1_error)


        API_Main = "https://open.neis.go.kr/hub/mealServiceDietInfo?"
        API_String =f"KEY={Neis_key}&Type=json&pIndex=1&pSize=5&ATPT_OFCDC_SC_CODE={Moe_code}&SD_SCHUL_CODE={School_code}&MLSV_YMD={day}&MMEAL_SC_CODE={meal_code}"
        API = API_Main + API_String

        mealAPI = requests.get(API).json()

        try:
            Api_row = mealAPI['mealServiceDietInfo'][1]['row'][0]
            school_name = Api_row["SCHUL_NM"] #학교명
            meal_type = Api_row["MMEAL_SC_NM"] #급식종류
            #meal_nutrient = Api_row["NTR_INFO"] #영양정보
            #meal_nutrient = meal_nutrient.replace("<br/>","\n")

            meal = Api_row["DDISH_NM"] #급식(raw)
            meal = meal.replace("<br/>","\n")
            meal = meal.replace(".","")
            meal = meal.replace(" ","")
            for i in range(0,30):
                meal = meal.replace(f"{i}", "")
            meal = meal.replace("()","")

            Meal_Embed = discord.Embed(title=f"{school_name} 오늘의 {meal_type}", description=f"{meal}", color=0xffdc16)
            Meal_Embed.set_thumbnail(url=ImageDict["Meal"])
            await ctx.respond(embed=Meal_Embed)

        except:
            Api_res = mealAPI['RESULT']
            code = Api_res['CODE']
            msg = Api_res['MESSAGE']

            Meal_Embed = discord.Embed(title=f"급식 조회에 실패했습니다.", description=f"오류코드:{code} \n오류내용:{msg}", color=0xffdc16)
            Meal_Embed.set_thumbnail(url=ImageDict["Meal"])
            await ctx.respond(embed=Meal_Embed)

def setup(bot):
    bot.add_cog(MEAL(bot))