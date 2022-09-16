import discord
from discord.ext import commands, tasks
from hcskr import asyncSelfCheck
import datetime
import json
import random

from setting import hcs_path, hcs_time_H, hcs_time_M, DB_channel
file_path = hcs_path

class hcs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.time = 3
        self.Auto_check.start()

    @tasks.loop(seconds=40)
    async def Auto_check(self):
        select = str(datetime.time(hcs_time_H, hcs_time_M-self.time).strftime("%H:%M"))
        now = str(datetime.datetime.now().strftime("%H:%M"))
        weekday = datetime.datetime.now().weekday()

        weekend = [6, 7]
        if not weekday in weekend:
            if select == now:
                amount = 0
                json_object = json.load(open(hcs_path,encoding="utf_8"))
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
                with open(file_path, "r", encoding="utf_8") as json_file:
                    data = json.load(json_file)

                data[f'users'] = f"{amount}"

                with open(file_path, 'w',encoding="utf_8") as writefile:
                    json.dump(data, writefile, indent="\t", ensure_ascii=False)


                self.time = random.randrange(1,8)
            else:
                pass
        else:
            pass

    @Auto_check.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(hcs(bot))