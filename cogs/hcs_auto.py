from discord.ext import commands, tasks
from hcskr import asyncSelfCheck
import datetime
import json
import random

from setting import hcs_time_H, hcs_time_M, DB_path

#------------------------------------------------------------------------------------------

class hcs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.time = 3
        self.last_Day = "None"
        self.Auto_check.start()

    @tasks.loop(seconds=40)
    async def Auto_check(self):
        select = str(datetime.time(hcs_time_H, hcs_time_M-self.time).strftime("%H:%M"))
        now = str(datetime.datetime.now().strftime("%H:%M"))
        today = datetime.datetime.now().strftime("%y/%m/%d")
        today_weekday = datetime.datetime.now().weekday()

        if not today == self.last_Day: # 마지막으로 자가진단을 진행한날이 오늘이 아니면
            if select == now: # 지금이 설정된 시간이라면
                if today_weekday in [5, 6]: # 오늘이 주말이라면
                    self.last_Day = datetime.datetime.now().strftime("%y/%m/%d")
                    print(f'주말입니다 자가진단을 진행하지 않습니다. [ {datetime.datetime.now().strftime("%y/%m/%d, %H:%M")} ]')

                else: # 오늘이 주말이 아니라면
                    amount = 0
                    json_object = json.load(open(DB_path,encoding="utf_8"))
                    print(f'자가진단이 시작됩니다. [ {datetime.datetime.now().strftime("%y/%m/%d, %H:%M")} ]')
                    for k, v in json_object.items():
                        if k == 'users':
                            continue
                        if v[0]['Auto_check'] == "O":
                            Nickname = v[0]['Nickname']
                            Name = v[0]['Name']
                            Birthday = v[0]['Birthday']
                            Area = v[0]['Area']
                            School = v[0]['School']
                            School_lv = v[0]['School_lv']
                            Password = v[0]['Password']

                            hcskr_result = await asyncSelfCheck(Name, Birthday, Area, School, School_lv, Password)
                            amount = amount + 1

                            if hcskr_result['code'] == 'SUCCESS':
                                print(f" -{Nickname} : 자가진단 완료")
                            else:
                                print(f" -{Nickname} : 자가진단 실패 - {hcskr_result['code']}")

                    print(f" - 오늘 진행한 자가진단 횟수: {amount}")
                    with open(DB_path, "r", encoding="utf_8") as json_file:
                        data = json.load(json_file)
                    data[f'users'] = f"{amount}"

                    with open(DB_path, 'w',encoding="utf_8") as writefile:
                        json.dump(data, writefile, indent="\t", ensure_ascii=False)

                    self.time = random.randrange(1,8)
                    self.last_Day = datetime.datetime.now().strftime("%y/%m/%d")
            else:
                pass
            

    @Auto_check.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(hcs(bot))