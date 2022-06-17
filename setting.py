import os

# 봇 기본정보
token = os.environ['Token'] # 봇의 토큰
guild = int(os.environ['Guild']) # 테스트용(관리자 전용) 길드
owner = os.environ['Owner'] # 봇 소유자
DB_channel = int(os.environ['DB_channel']) # JSON파일을 보낼 채널


#자가진단 설정 ----------------------------------------------------------------------------------------------

hcs_path ="hcs_info.json"
hcs_time_H = 7
hcs_time_M = 7

# 이미지 URL ----------------------------------------------------------------------------------------------

ImageDict = {
    "Trash_can":"https://cdn.discordapp.com/attachments/972006686015516702/972007178544226334/Trash.png",
    "List": "https://cdn.discordapp.com/attachments/972006686015516702/972007850085842994/document.png",
    "hcs_icon": "https://cdn.discordapp.com/attachments/972006686015516702/972008903242051624/hcskr.png"
            }