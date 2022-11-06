import os


# 봇 기본정보
token = os.environ['Token'] # 봇의 토큰
Neis_key = str(os.environ['Neis_key']) # 나이스 API KEY
owner = os.environ['Owner'] # 봇 소유자

guild = int(os.environ['Guild']) # 테스트용(관리자 전용) 길드

#자가진단 설정 ----------------------------------------------------------------------------------------------

hcs_time_H = 7 #자가진단을 진행할 시각(시)
hcs_time_M = 9 #자가진단을 진행할 시각(분)

# 공통변수 ----------------------------------------------------------------------------------------------

DB_path ="User_info.json" # DB파일 경로

# 이미지 링크
ImageDict = {
    "List_Write": "https://cdn.discordapp.com/attachments/1029688812605022269/1029693763897012274/uxwing-list-edit.png",
    "List_Failed": "https://cdn.discordapp.com/attachments/978203984928047124/1029702925674618920/uxwing-list3-edit.png",
    "List_Done": "https://cdn.discordapp.com/attachments/1029688812605022269/1029695570513772604/uxwing-list2-edit.png",

    "Timer_On": "https://cdn.discordapp.com/attachments/1029688812605022269/1029709243831570432/uxwing-clock-on.png",
    "Timer_Off": "https://cdn.discordapp.com/attachments/1029688812605022269/1029709832590196766/uxwing-clock-off.png",

    "Meal":"https://cdn.discordapp.com/attachments/1029688812605022269/1029711154169262130/uxwing-meal.png",
    "Trash_can":"https://cdn.discordapp.com/attachments/1029688812605022269/1029688847665201192/noun-Trash-edit.png",
    "hcs_icon": "https://cdn.discordapp.com/attachments/972006686015516702/972008903242051624/hcskr.png"
            }

# 지역 나열
Areas = {
    "B10": ["서울", "서울특별시", "서울시"],
    "C10": ["부산", "부산광역시", "부산시"],
    "D10": ["대구", "대구광역시", "대구시"],
    "E10": ["인천", "인천광역시", "인천시"],
    "F10": ["광주", "광주광역시", "광주시"],
    "G10": ["대전", "대전광역시", "대전시"],
    "H10": ["울산", "울산광역시", "울산시"],
    "I10": ["세종", "세종특별자치시", "세종시", "세종특별시"],
    "J10": ["경기", "경기도"],
    "K10": ["강원", "강원도"],
    "M10": ["충북", "충청북도"],
    "N10": ["충남", "충청남도"],
    "P10": ["전북", "전라북도"],
    "Q10": ["전남", "전라남도"],
    "R10": ["경북", "경상북도"],
    "T10": ["경남", "경상남도"],
    "R10": ["제주", "제주특별자치도", "제주도", "제주특별자치시"]
}