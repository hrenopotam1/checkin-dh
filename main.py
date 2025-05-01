{\rtf1\ansi\ansicpg1251\cocoartf2709
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import asyncio\
import sqlite3\
import pandas as pd\
from datetime import datetime\
from aiogram import Bot, Dispatcher, types\
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton\
from aiogram.utils import executor\
from fastapi import FastAPI\
from fastapi.responses import FileResponse\
import uvicorn\
import threading\
\
API_TOKEN = 7838973738:AAHTZc9NJd1delkQwiW8VvPz-33pDpNN1Qc\
DB_NAME = shifts.db\
\
bot = Bot(token=API_TOKEN)\
dp = Dispatcher(bot)\
\
app = FastAPI()\
\
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)\
keyboard.add(KeyboardButton("\uc0\u55357 \u56596  \u1042 \u1099 \u1096 \u1077 \u1083  \u1085 \u1072  \u1089 \u1084 \u1077 \u1085 \u1091 "))\
keyboard.add(KeyboardButton("\uc0\u55357 \u56597  \u1047 \u1072 \u1074 \u1077 \u1088 \u1096 \u1080 \u1083  \u1089 \u1084 \u1077 \u1085 \u1091 "))\
\
def init_db():\
    conn = sqlite3.connect(DB_NAME)\
    c = conn.cursor()\
    c.execute('''\
        CREATE TABLE IF NOT EXISTS shifts (\
            id INTEGER PRIMARY KEY AUTOINCREMENT,\
            user_id INTEGER,\
            full_name TEXT,\
            start_time TEXT,\
            end_time TEXT\
        )\
    ''')\
    conn.commit()\
    conn.close()\
\
@dp.message_handler(commands=['start'])\
async def start_cmd(message: types.Message):\
    await message.answer(\
        f"\uc0\u1055 \u1088 \u1080 \u1074 \u1077 \u1090 , \{message.from_user.full_name\}!\\n\u1053 \u1072 \u1078 \u1084 \u1080  \u1082 \u1085 \u1086 \u1087 \u1082 \u1091 , \u1095 \u1090 \u1086 \u1073 \u1099  \u1085 \u1072 \u1095 \u1072 \u1090 \u1100  \u1080 \u1083 \u1080  \u1079 \u1072 \u1074 \u1077 \u1088 \u1096 \u1080 \u1090 \u1100  \u1089 \u1084 \u1077 \u1085 \u1091 .",\
        reply_markup=keyboard\
    )\
\
@dp.message_handler(lambda m: m.text == "\uc0\u55357 \u56596  \u1042 \u1099 \u1096 \u1077 \u1083  \u1085 \u1072  \u1089 \u1084 \u1077 \u1085 \u1091 ")\
async def start_shift(message: types.Message):\
    user_id = message.from_user.id\
    full_name = message.from_user.full_name\
    now = datetime.now().isoformat()\
\
    conn = sqlite3.connect(DB_NAME)\
    c = conn.cursor()\
    c.execute("SELECT * FROM shifts WHERE user_id = ? AND end_time IS NULL", (user_id,))\
    if c.fetchone():\
        await message.answer("\uc0\u10071  \u1059  \u1090 \u1077 \u1073 \u1103  \u1091 \u1078 \u1077  \u1077 \u1089 \u1090 \u1100  \u1072 \u1082 \u1090 \u1080 \u1074 \u1085 \u1072 \u1103  \u1089 \u1084 \u1077 \u1085 \u1072 .")\
    else:\
        c.execute("INSERT INTO shifts (user_id, full_name, start_time) VALUES (?, ?, ?)",\
                  (user_id, full_name, now))\
        conn.commit()\
        await message.answer(f"\uc0\u9989  \u1057 \u1084 \u1077 \u1085 \u1072  \u1085 \u1072 \u1095 \u1072 \u1090 \u1072  \u1074  \{datetime.now().strftime('%H:%M:%S')\}.")\
    conn.close()\
\
@dp.message_handler(lambda m: m.text == "\uc0\u55357 \u56597  \u1047 \u1072 \u1074 \u1077 \u1088 \u1096 \u1080 \u1083  \u1089 \u1084 \u1077 \u1085 \u1091 ")\
async def end_shift(message: types.Message):\
    user_id = message.from_user.id\
    now = datetime.now().isoformat()\
\
    conn = sqlite3.connect(DB_NAME)\
    c = conn.cursor()\
    c.execute("SELECT id, start_time FROM shifts WHERE user_id = ? AND end_time IS NULL", (user_id,))\
    row = c.fetchone()\
    if row:\
        shift_id, start_time = row\
        c.execute("UPDATE shifts SET end_time = ? WHERE id = ?", (now, shift_id))\
        conn.commit()\
        start_dt = datetime.fromisoformat(start_time)\
        end_dt = datetime.fromisoformat(now)\
        duration = end_dt - start_dt\
        hours = round(duration.total_seconds() / 3600, 2)\
        await message.answer(f"\uc0\u55357 \u56602  \u1057 \u1084 \u1077 \u1085 \u1072  \u1079 \u1072 \u1074 \u1077 \u1088 \u1096 \u1077 \u1085 \u1072 . \u1054 \u1090 \u1088 \u1072 \u1073 \u1086 \u1090 \u1072 \u1085 \u1086 : \{hours\} \u1095 .")\
    else:\
        await message.answer("\uc0\u10071  \u1040 \u1082 \u1090 \u1080 \u1074 \u1085 \u1072 \u1103  \u1089 \u1084 \u1077 \u1085 \u1072  \u1085 \u1077  \u1085 \u1072 \u1081 \u1076 \u1077 \u1085 \u1072 .")\
    conn.close()\
\
@app.get("/report")\
def get_report():\
    conn = sqlite3.connect(DB_NAME)\
    df = pd.read_sql_query("SELECT * FROM shifts", conn)\
    df['start_time'] = pd.to_datetime(df['start_time'])\
    df['end_time'] = pd.to_datetime(df['end_time'])\
    df['worked_hours'] = (df['end_time'] - df['start_time']).dt.total_seconds() / 3600\
    df.to_excel("shifts_report.xlsx", index=False)\
    conn.close()\
    return FileResponse("shifts_report.xlsx", media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename="shifts_report.xlsx")\
\
def start_fastapi():\
    uvicorn.run(app, host="0.0.0.0", port=8000)\
\
if __name__ == '__main__':\
    init_db()\
    threading.Thread(target=start_fastapi, daemon=True).start()\
    executor.start_polling(dp, skip_updates=True)\
}