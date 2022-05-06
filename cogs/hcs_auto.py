from discord.ext import commands, tasks
from hcskr import asyncSelfCheck
import datetime
import json

from setting import hcs_path, hcs_time_H, hcs_time_M

class hcs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Auto_check.start()

    @tasks.loop(seconds=40)
    async def Auto_check(self):
        select = str(datetime.time(hcs_time_H, hcs_time_M).strftime("%H:%M"))
        now = str(datetime.datetime.now().strftime("%H:%M"))
        weekday = datetime.datetime.now().weekday()

        weekend = [6, 7]
        if not weekday in weekend:
            if select == now:

                json_object = json.load(open(hcs_path,encoding="utf_8"))
                for k, v in json_object.items():
                    if v[0]['Auto_check'] == "O":
                        Nickname = v[0]['Nickname']
                        Name = v[0]['Name']
                        Birthday = v[0]['Birthday']
                        Area = v[0]['Area']
                        School = v[0]['School']
                        School_lv = v[0]['School_lv']
                        Password = v[0]['Password']

                        hcskr_result = await asyncSelfCheck(Name, Birthday, Area, School, School_lv, Password)

                        if hcskr_result['code'] == 'SUCCESS':
                            print(f"{Nickname} : 자가진단 완료")
                        else:
                            print(f"{Nickname} : 자가진단 실패 - {hcskr_result['code']}")
            else:
                pass
        else:
            pass

def setup(bot):
    bot.add_cog(hcs(bot))