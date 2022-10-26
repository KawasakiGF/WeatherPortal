import re
import requests
import os
import json
import urllib.request
import random
import math
from bs4 import BeautifulSoup

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, ConfirmTemplate, ButtonsTemplate, CarouselTemplate, CarouselColumn
)

# アプリケーションの名前となる文字列
# ファイルをスクリプトとして直接実行した場合、 __name__ は __main__ になる
app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

#環境変数を実用的な変数に代入しているかも
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

#対話内容を管理するクラスとインスタンスの初期設定
class Status:
    def __init__(self):
          self.context = "0"
          self.date = 0
          self.area = ""
          self.areaT = ""
          self.basyoList = ""
          self.date2 = 0
          self.area2 = ""
          self.areaT2 = ""
          self.basyoList2 = ""
          self.Hdate = 0
          self.Harea = ""
          self.HareaT = ""
          self.HbasyoList = ""
          self.count = 0
          self.oyasumi = 0

    def get_context(self):
        return self.context
    def set_context(self, context):
          self.context = context

    def get_date(self):
        return self.date
    def set_date(self, date):
          self.date = date

    def get_area(self):
        return self.area
    def set_area(self, area):
          self.area = area

    def get_areaT(self):
        return self.areaT
    def set_areaT(self, areaT):
          self.areaT = areaT

    def get_basyoList(self):
        return self.basyoList
    def set_basyoList(self, basyoList):
          self.basyoList = basyoList


    def get_date2(self):
        return self.date2
    def set_date2(self, date2):
          self.date2 = date2

    def get_area2(self):
        return self.area2
    def set_area2(self, area2):
          self.area2 = area2

    def get_areaT2(self):
        return self.areaT2
    def set_areaT2(self, areaT2):
          self.areaT2 = areaT2

    def get_basyoList2(self):
        return self.basyoList2
    def set_basyoList2(self, basyoList2):
          self.basyoList2 = basyoList2


    def get_Hdate(self):
        return self.Hdate
    def set_Hdate(self, Hdate):
          self.Hdate = Hdate

    def get_Harea(self):
        return self.Harea
    def set_Harea(self, Harea):
          self.Harea = Harea

    def get_HareaT(self):
        return self.HareaT
    def set_HareaT(self, HareaT):
          self.HareaT = HareaT

    def get_HbasyoList(self):
        return self.HbasyoList
    def set_HbasyoList(self, HbasyoList):
          self.HbasyoList = HbasyoList


    def get_para(self):
        return self.para
    def set_para(self, para):
          self.para = para


    def get_count(self):
        return self.count
    def set_count(self, count):
          self.count = count

    def get_oyasumi(self):
        return self.oyasumi
    def set_oyasumi(self, oyasumi):
          self.oyasumi = oyasumi


class MySession:
    _status_map = dict()

    def register(user_id):
        if MySession._get_status(user_id) is None:
            MySession._put_status(user_id, Status())

    def reset(user_id):
        MySession._put_status(user_id, Status())

    def _get_status(user_id):
        return MySession._status_map.get(user_id)
    def _put_status(user_id, status: Status):
        MySession._status_map[user_id]= status

    def read_context(user_id):
        return MySession._status_map.get(user_id).get_context()
    def update_context(user_id, context):
        new_status = MySession._status_map.get(user_id)
        new_status.set_context(context)
        MySession._status_map[user_id] = new_status

    def read_date(user_id):
        return MySession._status_map.get(user_id).get_date()
    def update_date(user_id, date):
        new_status = MySession._status_map.get(user_id)
        new_status.set_date(date)
        MySession._status_map[user_id] = new_status

    def read_area(user_id):
        return MySession._status_map.get(user_id).get_area()
    def update_area(user_id, area):
        new_status = MySession._status_map.get(user_id)
        new_status.set_area(area)
        MySession._status_map[user_id] = new_status

    def read_areaT(user_id):
        return MySession._status_map.get(user_id).get_areaT()
    def update_areaT(user_id, areaT):
        new_status = MySession._status_map.get(user_id)
        new_status.set_areaT(areaT)
        MySession._status_map[user_id] = new_status

    def read_basyoList(user_id):
        return MySession._status_map.get(user_id).get_basyoList()
    def update_basyoList(user_id, basyoList):
        new_status = MySession._status_map.get(user_id)
        new_status.set_basyoList(basyoList)
        MySession._status_map[user_id] = new_status


    def read_date2(user_id):
        return MySession._status_map.get(user_id).get_date2()
    def update_date2(user_id, date2):
        new_status = MySession._status_map.get(user_id)
        new_status.set_date2(date2)
        MySession._status_map[user_id] = new_status

    def read_area2(user_id):
        return MySession._status_map.get(user_id).get_area2()
    def update_area2(user_id, area2):
        new_status = MySession._status_map.get(user_id)
        new_status.set_area2(area2)
        MySession._status_map[user_id] = new_status

    def read_areaT2(user_id):
        return MySession._status_map.get(user_id).get_areaT2()
    def update_areaT2(user_id, areaT2):
        new_status = MySession._status_map.get(user_id)
        new_status.set_areaT2(areaT2)
        MySession._status_map[user_id] = new_status

    def read_basyoList2(user_id):
        return MySession._status_map.get(user_id).get_basyoList2()
    def update_basyoList2(user_id, basyoList2):
        new_status = MySession._status_map.get(user_id)
        new_status.set_basyoList2(basyoList2)
        MySession._status_map[user_id] = new_status


    def read_Hdate(user_id):
        return MySession._status_map.get(user_id).get_Hdate()
    def update_Hdate(user_id, Hdate):
        new_status = MySession._status_map.get(user_id)
        new_status.set_Hdate(Hdate)
        MySession._status_map[user_id] = new_status

    def read_Harea(user_id):
        return MySession._status_map.get(user_id).get_Harea()
    def update_Harea(user_id, Harea):
        new_status = MySession._status_map.get(user_id)
        new_status.set_Harea(Harea)
        MySession._status_map[user_id] = new_status

    def read_HareaT(user_id):
        return MySession._status_map.get(user_id).get_HareaT()
    def update_HareaT(user_id, HareaT):
        new_status = MySession._status_map.get(user_id)
        new_status.set_HareaT(HareaT)
        MySession._status_map[user_id] = new_status

    def read_HbasyoList(user_id):
        return MySession._status_map.get(user_id).get_HbasyoList()
    def update_HbasyoList(user_id, HbasyoList):
        new_status = MySession._status_map.get(user_id)
        new_status.set_HbasyoList(HbasyoList)
        MySession._status_map[user_id] = new_status


    def read_para(user_id):
        return MySession._status_map.get(user_id).get_para()
    def update_para(user_id, para):
        new_status = MySession._status_map.get(user_id)
        new_status.set_para(para)
        MySession._status_map[user_id] = new_status


    def read_count(user_id):
        return MySession._status_map.get(user_id).get_count()
    def update_count(user_id, count):
        new_status = MySession._status_map.get(user_id)
        new_status.set_count(count)
        MySession._status_map[user_id] = new_status

    def read_oyasumi(user_id):
        return MySession._status_map.get(user_id).get_oyasumi()
    def update_oyasumi(user_id, oyasumi):
        new_status = MySession._status_map.get(user_id)
        new_status.set_oyasumi(oyasumi)
        MySession._status_map[user_id] = new_status



#都道府県コードを返す
def todoufukenNum(num):
     if num < 9:
          codeNum = num + 1
          return "0" + str(codeNum)
     elif num == 9:
          return "10"
     else:
          codeNum = num + 1
          return str(codeNum)

#都道府県の場所コード探す
def codeKaraFind(finder):
     teijiBasyoList = ""
     for i in range(0, len(Tcode)):
          if re.match((finder + "...."), Tcode[i]):
               teijiBasyoList += "\n・" + Tname[i]

     return teijiBasyoList
      
#天気メッセージを作る
def OtenkiMessageMaker(code, itu):
     url="https://weather.tsukumijima.net/api/forecast/city/" + code
     response=requests.get(url)
     jsonData=response.json()
     #天気データ取得
     date="--"
     weather="--"
     tempMAX=0
     tempMIN=0
     amCOR="--"
     pmCOR="--"
     date=jsonData["forecasts"][itu]["date"]
     weather=jsonData["forecasts"][itu]["telop"]
     tempMAX=jsonData["forecasts"][itu]["temperature"]["max"]["celsius"]
     tempMIN=jsonData["forecasts"][itu]["temperature"]["min"]["celsius"]
     am1COR=jsonData["forecasts"][itu]["chanceOfRain"]["T00_06"]
     am2COR=jsonData["forecasts"][itu]["chanceOfRain"]["T06_12"]
     pm1COR=jsonData["forecasts"][itu]["chanceOfRain"]["T12_18"]
     pm2COR=jsonData["forecasts"][itu]["chanceOfRain"]["T18_24"] 
     #天気メッセージ作成
     tenkiInfo = '＜日付＞:{0}\n＜天気＞:{1}\n＜気温＞\n最低気温:{2}℃\n最高気温:{3}℃\n＜降水確率＞\n深夜:{4}　朝:{5}\n　昼:{6}　夜:{7}'.format(date,weather,tempMIN,tempMAX,am1COR,am2COR,pm1COR,pm2COR)
     return tenkiInfo

#知りたい場所の天気を作る
def needWeatherMaker(code, itu):
     url="https://weather.tsukumijima.net/api/forecast/city/" + code
     response=requests.get(url)
     jsonData=response.json()
     #天気データ取得
     weather="--"
     weather=jsonData["forecasts"][itu]["telop"]
     return weather

#気温の平均を作る
def tempMEANMaker(code, itu):
     url="https://weather.tsukumijima.net/api/forecast/city/" + code
     response=requests.get(url)
     jsonData=response.json()
     #天気データ取得
     tempMAX=0
     tempMIN=0
     tempMAX=jsonData["forecasts"][itu]["temperature"]["max"]["celsius"]
     tempMIN=jsonData["forecasts"][itu]["temperature"]["min"]["celsius"]
     if ((tempMAX is None) and (tempMIN is None)):
        return 100
     elif tempMAX is None: tempMAX=tempMIN
     elif tempMIN is None: tempMIN=tempMAX
     tempMEAN=(int(tempMAX)+int(tempMIN))/2.0-1.0
     return tempMEAN

#気温情報に欠けがないか調べる
def kionnHantei(code, itu):
     url="https://weather.tsukumijima.net/api/forecast/city/" + code
     response=requests.get(url)
     jsonData=response.json()
     #天気データ取得
     tempMAX=0
     tempMIN=0
     tempMAX=jsonData["forecasts"][itu]["temperature"]["max"]["celsius"]
     tempMIN=jsonData["forecasts"][itu]["temperature"]["min"]["celsius"]
     if ((tempMAX is None) or (tempMIN is None)): return "だめです"
     else: return "いいです"

#1か所の傘の有無判定
def kasaHantei(code, itu):
     url="https://weather.tsukumijima.net/api/forecast/city/" + code
     response=requests.get(url)
     jsonData=response.json()
     #天気データ取得
     weather="--"
     amCOR="--"
     pmCOR="--"
     weather=jsonData["forecasts"][itu]["telop"]
     amCOR=jsonData["forecasts"][itu]["chanceOfRain"]["T06_12"]
     pmCOR=jsonData["forecasts"][itu]["chanceOfRain"]["T12_18"]
     AC=re.sub(r"\D", "", amCOR)
     PC=re.sub(r"\D", "", pmCOR)
     if ((AC == "") and (PC == "")):
        kasaInfo = "傘情報を取得できませんでした…"
        return kasaInfo
     elif AC == "": AC=PC
     elif PC == "": PC=AC
     CORMEAN=int((int(AC)+int(PC))/2.0)
     if CORMEAN >= 50:
        kasaInfo = "雨が降りそうです。傘を持ってお出かけください。"
     elif (CORMEAN >= 30 and "雨" in weather):
        kasaInfo = "雨が降りそうです。傘を持ってお出かけください。"
     elif CORMEAN >= 30:
        kasaInfo = "雨が降らないこともありそうです。折り畳み傘があれば十分そうですね。"
     else:
        kasaInfo = "傘は必要ありません。"
     return kasaInfo

#1か所の服装判定
def fukusouHantei(tempMEAN, weather):
  if tempMEAN <= 5:
    fukusou = '＜服装情報＞\n重ね着をして、もふもふのコートやダウンジャケットを着てください。また、手袋やマフラー、暖かい靴下などがあれば積極的に利用して、できるだけ暖かい服装にしてください。'
  elif tempMEAN <= 9:
    fukusou = '＜服装情報＞\n重ね着をして、ダウンコートやジャケットを着てください。風が強いときは手袋やマフラーがあると安心です。'
  elif tempMEAN <= 13:
    fukusou = '＜服装情報＞\nジャケットやコートなど、風を通さない服装がおススメです。ヒートテックなんかがあると安心ですよ。'
  elif tempMEAN <= 16 and weather == "晴れ":
    fukusou = '＜服装情報＞\nニットやセーターにするか、風が吹いていなければ軽い羽織りものを着てもよさそうです。'
  elif tempMEAN <= 16:
    fukusou = '＜服装情報＞\nニットやセーターで大丈夫と思いますが、もし寒く感じるときはジャケットやコートを着てください。'
  elif tempMEAN <= 19:
    fukusou = '＜服装情報＞\n薄手のジャケットやパーカーにして、重ね着をするといい感じです。'
  elif tempMEAN <= 22:
    fukusou = '＜服装情報＞\n着脱可能な羽織りものにし、温度に合わせて調節できるようにするといいですよ。'
  elif tempMEAN <= 24:
    fukusou = '＜服装情報＞\n長袖が一枚あればOKです。半袖と薄い羽織りものでも大丈夫ですね。'
  elif tempMEAN <= 29:
    fukusou = '＜服装情報＞\n半袖で過ごせそうです。長袖にして腕まくりをするのも一つの手です。'
  elif tempMEAN <= 99:
    fukusou = '＜服装情報＞\n半袖の涼しい服装にして、暑さ対策や熱中症対策を怠らないようにしてください。熱射病にはお気をつけて！'
  else:
    fukusou = '＜服装情報＞\n気温の情報を取得できませんでした…'
  return fukusou

#2か所の服装判定
def fukusouHantei2(STM, MTM, para):
  kandansa = ""
  tempMEAN = int((int(STM)+int(MTM))/2.0) + para
  if tempMEAN <= 5:
    fukusou = '＜服装情報＞\n重ね着をして、もふもふのコートやダウンジャケットを着てください。また、手袋やマフラー、暖かい靴下などがあれば積極的に利用して、できるだけ暖かい服装にしてください。'
  elif tempMEAN <= 9:
    fukusou = '＜服装情報＞\n重ね着をして、ダウンコートやジャケットを着てください。風が強いときは手袋やマフラーがあると安心です。'
  elif tempMEAN <= 13:
    fukusou = '＜服装情報＞\nジャケットやコートなど、風を通さない服装がおススメです。ヒートテックなんかがあると安心ですよ。'
  elif tempMEAN <= 16 and weather == "晴れ":
    fukusou = '＜服装情報＞\nニットやセーターにするか、風が吹いていなければ軽い羽織りものを着てもよさそうです。'
  elif tempMEAN <= 16:
    fukusou = '＜服装情報＞\nニットやセーターで大丈夫と思いますが、もし寒く感じるときはジャケットやコートを着てください。'
  elif tempMEAN <= 19:
    fukusou = '＜服装情報＞\n薄手のジャケットやパーカーにして、重ね着をするといい感じです。'
  elif tempMEAN <= 22:
    fukusou = '＜服装情報＞\n着脱可能な羽織りものにし、温度に合わせて調節できるようにするといいですよ。'
  elif tempMEAN <= 24:
    fukusou = '＜服装情報＞\n長袖が一枚あればOKです。半袖と薄い羽織りものでも大丈夫ですね。'
  elif tempMEAN <= 29:
    fukusou = '＜服装情報＞\n半袖で過ごせそうです。長袖にして腕まくりをするのも一つの手です。'
  elif tempMEAN <= 99:
    fukusou = '＜服装情報＞\n半袖の涼しい服装にして、暑さ対策や熱中症対策を怠らないようにしてください。熱射病にはお気をつけて！'
  else:
    fukusou = '＜服装情報＞\n気温の情報を取得できませんでした…'
  return (fukusou + kandansa)

#2か所の傘の有無判定
def kasaHantei2(codeS, ituS, codeM, ituM, ST, MT):
     url="https://weather.tsukumijima.net/api/forecast/city/" + codeS
     response=requests.get(url)
     jsonData=response.json()
     #天気データ取得
     weather="--"
     amCOR="--"
     pmCOR="--"
     weather=jsonData["forecasts"][ituS]["telop"]
     amCOR=jsonData["forecasts"][ituS]["chanceOfRain"]["T06_12"]
     pmCOR=jsonData["forecasts"][ituS]["chanceOfRain"]["T12_18"]
     AC=re.sub(r"\D", "", amCOR)
     PC=re.sub(r"\D", "", pmCOR)
     if ((AC == "") and (PC == "")):
        kasaInfo = "傘情報を取得できませんでした…"
     elif AC == "": AC=PC
     elif PC == "": PC=AC
     CORMEANS=(int(AC)+int(PC))/2.0

     urlM="https://weather.tsukumijima.net/api/forecast/city/" + codeM
     responseM=requests.get(urlM)
     jsonDataM=responseM.json()
     #天気データ取得
     weatherM="--"
     amCORM="--"
     pmCORM="--"
     weatherM=jsonDataM["forecasts"][ituM]["telop"]
     amCORM=jsonDataM["forecasts"][ituM]["chanceOfRain"]["T06_12"]
     pmCORM=jsonDataM["forecasts"][ituM]["chanceOfRain"]["T12_18"]
     ACM=re.sub(r"\D", "", amCORM)
     PCM=re.sub(r"\D", "", pmCORM)
     if ((ACM == "") and (PCM == "")):
        kasaInfo2 = "傘情報を取得できませんでした…"
     elif ACM == "": ACM=PCM
     elif PCM == "": PCM=ACM
     CORMEANM=(int(ACM)+int(PCM))/2.0

     CORMEAN = int((CORMEANS+CORMEANS)/2.0)

     if CORMEANS >= 50 and CORMEANM >= 50:
        kasaInfo = "雨が降りそうです。傘を持ってお出かけください。"
     elif (CORMEANS >= 50 and (CORMEANM >= 30 and "雨" in weather)) or (CORMEANM >= 50 and (CORMEANS >= 30 and "雨" in weather)):
        kasaInfo = "雨が降りそうです。傘を持ってお出かけください。"
     elif (CORMEANS >= 50 or (CORMEANS >= 30 and "雨" in weather)) and CORMEANM < 30:
        kasaInfo = ST + "では雨が降りそうですが、" + MT + "では雨が降らなさそうです。傘を持つ余裕があれば傘を、無ければ折り畳み傘を持ってお出かけください。"
     elif (CORMEANM >= 50 or (CORMEANM >= 30 and "雨" in weather)) and CORMEANS < 30:
        kasaInfo = ST + "では雨が降らなさそうですが、" + MT + "では雨が降りそうです。傘を持つ余裕があれば傘を、無ければ折り畳み傘を持ってお出かけください。"
     elif CORMEANS >= 30 or CORMEANM >= 30:
        kasaInfo = "雨が降らないこともありそうです。折り畳み傘があれば十分そうですね。"
     else:
        kasaInfo = "傘は必要ありません。"
     return kasaInfo

#天気アイコン判定
def picUrlMaker(weather):
    if weather=="晴れ" or weather=="晴山沿い雷雨" or weather=="晴山沿い雪" or weather=="朝の内霧後晴" or weather=="晴明け方霧":
        picUrl="https://i.ibb.co/v3Q1SzX/Sun.png"
    elif weather=="晴のち曇" or weather=="晴のち一時曇" or weather=="晴のち時々曇":
        picUrl="https://i.ibb.co/47Zp7tf/Sun-To-Cloud.png"
    elif weather=="晴のち雨" or weather=="晴のち一時雨" or weather=="晴のち時々雨" or weather=="晴のち雨か雪" or weather=="晴のち雨か雷雨" or weather=="晴夕方一時雨" or weather=="晴午後は雷雨" or weather=="晴昼頃から雨" or weather=="晴夕方から雨" or weather=="晴夜は雨" or weather=="晴夜半から雨":
        picUrl="https://i.ibb.co/w6yBmKP/Sun-To-Rain.png"
    elif weather=="晴のち雪" or weather=="晴のち一時雪" or weather=="晴のち時々雪" or weather=="晴のち雪か雨":
        picUrl="https://i.ibb.co/2hWsVQy/Sun-To-Snow.png"
    #存在しないパターン
    elif weather=="晴時々曇" or weather=="晴一時曇":
        picUrl="https://i.ibb.co/vJn5mwZ/Sun-Or-Cloud.png"
    elif weather=="晴時々雨" or weather=="晴一時雨" or weather=="晴時々雨か雪" or weather=="晴一時雨か雪" or weather=="晴一時雨か雷雨" or weather=="晴朝夕一時雨" or weather=="晴時々雨で雷雨を伴う":
        picUrl="https://i.ibb.co/cc9c8F1/Sun-Or-Rain.png"
    elif weather=="晴時々雪" or weather=="晴一時雪" or weather=="晴時々雪か雨" or weather=="晴一時雪か雨":
        picUrl="https://i.ibb.co/gZvsSzn/Sun-Or-Snow.png"
    elif weather=="曇り" or weather=="霧" or weather=="曇海上海岸は霧か霧雨":
        picUrl="https://i.ibb.co/V32pwjv/Cloud.png"
    elif weather=="曇のち晴" or weather=="曇のち一時晴" or weather=="曇のち時々晴":
        picUrl="https://i.ibb.co/wwc1J9P/Cloud-To-Sun.png"
    elif weather=="曇のち雨" or weather=="曇のち一時雨" or weather=="曇のち時々雨" or weather=="曇のち雨か雪" or weather=="曇のち雨か雷雨" or weather=="曇夕方一時雨" or weather=="曇昼頃から雨" or weather=="曇夕方から雨" or weather=="曇夜は雨" or weather=="曇夜半から雨":
        picUrl="https://i.ibb.co/mSXWrsm/Cloud-To-Rain.png"
    elif weather=="曇のち雪" or weather=="曇のち一時雪" or weather=="曇のち時々雪" or weather=="曇昼頃から雪" or weather=="曇夕方から雪" or weather=="曇夜は雪" or weather=="曇のち雪か雨":
        picUrl="https://i.ibb.co/Tv42FLY/Cloud-To-Snow.png"
    elif weather=="曇時々晴" or weather=="曇一時晴" or weather=="曇日中時々晴":
        picUrl="https://i.ibb.co/XX9sp2Y/Cloud-Or-Sun.png"
    elif weather=="曇時々雨" or weather=="曇一時雨" or weather=="曇時々雨か雪" or weather=="曇一時雨か雪" or weather=="曇一時雨か雷雨" or weather=="曇朝方一時雨" or weather=="曇時々雨で雷を伴う":
        picUrl="https://i.ibb.co/fkRCR7m/Cloud-Or-Rain.png"
    elif weather=="曇時々雪" or weather=="曇一時雪" or weather=="曇時々雪で雷を伴う" or weather=="曇一時雪か雨" or weather=="曇時々雪か雨":
        picUrl="https://i.ibb.co/9nyfKy5/Cloud-Or-Snow.png"
    elif weather=="雨" or weather=="大雨" or weather=="風雨共に強い" or weather=="雨一時強く降る" or weather=="雨で雷を伴う":
        picUrl="https://i.ibb.co/5xkdS8V/Rain.png"
    #存在しないパターン
    elif weather=="雨のち曇" or weather=="雨のち一時曇" or weather=="雨のち時々曇" or weather=="雨か雪のち曇" or weather=="朝の内雨のち曇":
        picUrl="https://i.ibb.co/vPgg2nt/Rain-To-Cloud.png"
    elif weather=="雨のち晴" or weather=="晴朝の内一時雨" or weather=="雨か雪のち晴" or weather=="朝の内雨のち晴" or weather=="雨昼頃から晴" or weather=="雨夕方から晴" or weather=="雨夜は晴":
        picUrl="https://i.ibb.co/mzYX8j4/Rain-To-Sun.png"
    elif weather=="雨のち雪" or weather=="雨のち一時雪" or weather=="雨のち時々雪" or weather=="雨夕方から雪" or weather=="雨夜は雪":
        picUrl="https://i.ibb.co/GsMs2bN/Rain-To-Snow.png"
    elif weather=="雨時々曇" or weather=="雨一時曇" or weather=="雨時々止む" or weather=="雨一時止む":
        picUrl="https://i.ibb.co/TbR1wRW/Rain-Or-Cloud.png"
    elif weather=="雨時々晴" or weather=="雨一時晴":
        picUrl="https://i.ibb.co/9sdjnNs/Rain-Or-Sun.png"
    elif weather=="雨時々雪" or weather=="雨一時雪" or weather=="雨か雪" or weather=="雨朝晩一時雪" or weather=="雨一時霙" or weather=="雨一時みぞれ":
        picUrl="https://i.ibb.co/nMDzd7d/Rain-Or-Snow.png"
    elif weather=="雪" or weather=="雪一時強く降る":
        picUrl="https://i.ibb.co/qrDSG2F/Snow.png"
    elif weather=="雪のち曇" or weather=="雪か雨のち曇" or weather=="朝の内雪のち曇":
        picUrl="https://i.ibb.co/qdftDWR/Snow-To-Cloud.png"
    elif weather=="雪のち晴" or weather=="雪か雨のち晴" or weather=="朝の内雪のち晴":
        picUrl="https://i.ibb.co/d4y70W9/Snow-To-Sun.png"
    elif weather=="雪のち雨" or weather=="雪のち霙" or weather=="雪のちみぞれ" or weather=="雪昼頃から雨" or weather=="雪夕方から雨" or weather=="雪夜から雨" or weather=="雪夜半から雨":
        picUrl="https://i.ibb.co/KqnPzr7/Snow-To-Rain.png"
    elif weather=="雪時々曇" or weather=="雪一時曇" or weather=="雪時々止む" or weather=="雪一時止む":
        picUrl="https://i.ibb.co/ZmYkPZW/Snow-Or-Cloud.png"
    elif weather=="雪時々晴" or weather=="雪一時晴":
        picUrl="https://i.ibb.co/y8M4vgH/Snow-Or-Sun.png"
    elif weather=="雪時々雨" or weather=="雪一時雨" or weather=="雪か雨" or weather=="雪一時霙" or weather=="雪一時みぞれ":
        picUrl="https://i.ibb.co/Zm5JnKh/Snow-Or-Rain.png"
    elif weather=="暴風雨" or weather=="雨で暴風を伴う":
        picUrl="https://i.ibb.co/y6X5z5X/Typhon.png "
    elif weather=="暴風雪" or weather=="大雪" or weather=="風雪強い" or weather=="雪で雷を伴う":
        picUrl="https://i.ibb.co/2NMQLDS/Heavy-Snow.png"
    else: picUrl="未知の天気"
    return picUrl




#####################通信の検証####################
# @app.route("/callback"...はappに対して/callbackというURLに対応するアクションを記述
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value 署名検証
    signature = request.headers['X-Line-Signature']

    # get request body as text リクエストボディ取得(これも検証の一環かしら)
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        # 署名を検証し、問題なければhandleに定義されている関数を呼び出す
        handler.handle(body, signature)
    # 署名検証で失敗したときは例外をあげる
    except InvalidSignatureError:
        abort(400)

    return 'OK'
###############################################

##############################################
##########実行するプログラムの内容をここに書く################
#@handler.addのメソッドの引数にはイベントのモデルを入れる(MessageEvent=メッセージを受けたら)
@handler.add(MessageEvent,message=TextMessage)
#関数名handle_messageは自由
#statusで1か所or2か所を管理。1x...1か所。2x...2か所
def handle_message(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    user_name = profile.display_name
    talk = event.message.text

    MySession.register(user_id)

    #if文の侵入が1つだけしか行けないならこれが原因で動かないかも
    if "県" in talk:
        basyo = talk.split("県", 1)
        ken = basyo[0] + "県"
        si = basyo[1].rsplit("市", 1)[0]

    if "都" in talk:
        basyo = talk.split("都", 1)
        ken = basyo[0] + "都"
        si = basyo[1].rsplit("市", 1)[0]

    if "道" in talk:
        basyo = talk.split("道", 1)
        ken = basyo[0] + "道"
        si = basyo[1].rsplit("市", 1)[0]

    if "府" in talk:
        basyo = talk.split("府", 1)
        ken = basyo[0] + "府"
        si = basyo[1].rsplit("市", 1)[0]

#会話を中断したいとき
    if (talk == "リセット"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("最初からリセットします。1か所or2か所を入力してください。"))
        # 現在のstatusを消して新規statusで初期化。
        MySession.reset(user_id)

#ヘルプ
    if ("ヘルプ" in talk or "help" in talk or "へるぷ" in talk):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "・天気情報を知るキーワードを忘れた\n→キーワード「1か所」or「2か所」を入力してください。1か所は普段の天気確認に、2か所は旅行時などの天気確認に適しています。\n・途中で会話を止めたい\n→キーワード「リセット」を入力してください。\n・現在のバージョンの確認\n→キーワード「バージョン」を入力してください。\n・アンケートのリンク、アンケートで答える内容が分からない\n→キーワード「アンケート」を入力してください。"))

#すやすやフォグくん
    if (MySession.read_oyasumi(user_id) == 3 or MySession.read_oyasumi(user_id) == 2 or MySession.read_oyasumi(user_id) == 1):
        if MySession.read_oyasumi(user_id) == 3 or MySession.read_oyasumi(user_id) == 2:
            #レアな寝言は4%の確率で聞ける
            if random.randint(0, 24) == 0: negoto = suyasuyaFogKunRare[0]
            elif random.randint(0, 24) == 1: negoto = suyasuyaFogKunRare[1]
            else:
                s = random.randint(0, len(suyasuyaFogKun)) - 1
                negoto = suyasuyaFogKun[s]
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text = negoto))
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text = "ふあぁ...よく寝たです...\nあ、" + user_name + ohayou))
        MySession.update_oyasumi(user_id, MySession.read_oyasumi(user_id)-1)

#いつものセットでお天気検索
    elif MySession.read_context(user_id) == "0" and (talk == "いつもの" or talk == "いつもので" or talk == "いつものでお願い" or talk == "いつものでおねがい" or talk == "いつものお願い" or talk == "いつものおねがい" or talk == "いつもの頼む" or talk == "いつもの頼んだ" or talk == "いつものたのむ" or talk == "いつものたのんだ"):
          para = MySession.read_para(user_id)
          picUrl = picUrlMaker(needWeatherMaker(Tcode[Tname.index(MySession.read_Harea(user_id))], MySession.read_Hdate(user_id)))
          fukusouInfo = fukusouHantei((tempMEANMaker(Tcode[Tname.index(MySession.read_Harea(user_id))], MySession.read_Hdate(user_id)) + int(para)), needWeatherMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id)))
          tenkiInfo = OtenkiMessageMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id))
          kasaInfo = kasaHantei(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id))
          if picUrl == "未知の天気":
               line_bot_api.reply_message(
                    event.reply_token,
                    [TextSendMessage(text=day[MySession.read_date(user_id)] + "の" + MySession.read_areaT(user_id) + MySession.read_area(user_id) + "の天気情報を表示します！"),
                    TextSendMessage(text=tenkiInfo),
                    TextSendMessage(text=kasaInfo),
                    TextSendMessage(text=fukusouInfo)])
          else:
               line_bot_api.reply_message(
                    event.reply_token,
                    [TextSendMessage(text=day[MySession.read_date(user_id)] + "の" + MySession.read_areaT(user_id) + MySession.read_area(user_id) + "の天気情報を表示します！"),
                    TextSendMessage(text=tenkiInfo),
                    ImageSendMessage(original_content_url=picUrl, preview_image_url=picUrl),
                    TextSendMessage(text=kasaInfo),
                    TextSendMessage(text=fukusouInfo)])

#1か所の場所を聞く####################
    elif MySession.read_context(user_id) == "0" and ("県" in talk or "都" in talk or "道" in talk or "府" in talk):
       if ken in todoufuken:
          #保持情報はいったん避難
          Hdate = MySession.read_Hdate(user_id)
          Harea = MySession.read_Harea(user_id)
          HareaT = MySession.read_HareaT(user_id)
          HbasyoList = MySession.read_HbasyoList(user_id)
          para = MySession.read_para(user_id)
          #全部消した後、
          MySession.reset(user_id)
          #保持情報を再度覚えさせる
          MySession.update_Hdate(user_id, Hdate)
          MySession.update_Harea(user_id, MySession.read_area(user_id))
          MySession.update_HareaT(user_id, MySession.read_areaT(user_id))
          MySession.update_HbasyoList(user_id, MySession.read_HbasyoList(user_id))
          MySession.update_para(user_id, para)

          MySession.update_areaT(user_id, ken)
          MySession.update_area(user_id, si)

          #日にちを聞くとこ###########################################
          if si in Tname:
              buttons_template = ButtonsTemplate(
                  text="日時を選択してください。", actions=[
                      PostbackAction(label="今日", data="今日", text="今日"),
                      PostbackAction(label="明日", data="明日", text="明日"),
                      PostbackAction(label="明後日", data="明後日", text="明後日")
                  ])
              template_message = TemplateSendMessage(
                  alt_text="日時を選択してください", template=buttons_template)
              line_bot_api.reply_message(
                  event.reply_token, template_message)
              MySession.update_context(user_id, "11")
                      
          else:
              TBasyo = todoufukenNum(int(todoufuken.index(ken)))
              kwsiBasyoList = codeKaraFind(TBasyo)

              if len(kwsiBasyoList) == 1:
                  carousel_template = CarouselTemplate(columns=[
                      CarouselColumn(text="1/1", actions=[
                                                PostbackAction(label=BasyoList[0], data=BasyoList[0], text=BasyoList[0])
                      ])
                  ])
              elif len(kwsiBasyoList) == 2:
                  carousel_template = CarouselTemplate(columns=[
                      CarouselColumn(text="1/1", actions=[
                                                PostbackAction(label=BasyoList[0], data=BasyoList[0], text=BasyoList[0]),
                                                PostbackAction(label=BasyoList[1], data=BasyoList[1], text=BasyoList[1])
                      ])
                  ])
              elif len(kwsiBasyoList) == 3:
                  carousel_template = CarouselTemplate(columns=[
                      CarouselColumn(text="1/1", actions=[
                                                PostbackAction(label=BasyoList[0], data=BasyoList[0], text=BasyoList[0]),
                                                PostbackAction(label=BasyoList[1], data=BasyoList[1], text=BasyoList[1]),
                                                PostbackAction(label=BasyoList[2], data=BasyoList[2], text=BasyoList[2])
                      ])
                  ])
              elif len(kwsiBasyoList) == 4:
                  carousel_template = CarouselTemplate(columns=[
                      CarouselColumn(text="1/1", actions=[
                                                PostbackAction(label=BasyoList[0], data=BasyoList[0], text=BasyoList[0]),
                                                PostbackAction(label=BasyoList[1], data=BasyoList[1], text=BasyoList[1]),
                                                PostbackAction(label=BasyoList[2], data=BasyoList[2], text=BasyoList[2]),
                                                PostbackAction(label=BasyoList[3], data=BasyoList[3], text=BasyoList[3])
                      ])
                  ])
              elif len(kwsiBasyoList) == 5:
                  carousel_template = CarouselTemplate(columns=[
                      CarouselColumn(text="1/2", actions=[
                                                PostbackAction(label=BasyoList[0], data=BasyoList[0], text=BasyoList[0]),
                                                PostbackAction(label=BasyoList[1], data=BasyoList[1], text=BasyoList[1]),
                                                PostbackAction(label=BasyoList[2], data=BasyoList[2], text=BasyoList[2]),
                                                PostbackAction(label=BasyoList[3], data=BasyoList[3], text=BasyoList[3])
                      ]),
                      CarouselColumn(text="2/2", actions=[
                                                PostbackAction(label=BasyoList[4], data=BasyoList[4], text=BasyoList[4])
                      ])
                  ])
              elif len(kwsiBasyoList) == 6:
                  carousel_template = CarouselTemplate(columns=[
                      CarouselColumn(text="1/2", actions=[
                                                PostbackAction(label=BasyoList[0], data=BasyoList[0], text=BasyoList[0]),
                                                PostbackAction(label=BasyoList[1], data=BasyoList[1], text=BasyoList[1]),
                                                PostbackAction(label=BasyoList[2], data=BasyoList[2], text=BasyoList[2]),
                                                PostbackAction(label=BasyoList[3], data=BasyoList[3], text=BasyoList[3])
                      ]),
                      CarouselColumn(text="2/2", actions=[
                                                PostbackAction(label=BasyoList[4], data=BasyoList[4], text=BasyoList[4]),
                                                PostbackAction(label=BasyoList[5], data=BasyoList[5], text=BasyoList[5])
                      ])
                  ])
              elif len(kwsiBasyoList) == 7:
                  carousel_template = CarouselTemplate(columns=[
                      CarouselColumn(text="1/2", actions=[
                                                PostbackAction(label=BasyoList[0], data=BasyoList[0], text=BasyoList[0]),
                                                PostbackAction(label=BasyoList[1], data=BasyoList[1], text=BasyoList[1]),
                                                PostbackAction(label=BasyoList[2], data=BasyoList[2], text=BasyoList[2]),
                                                PostbackAction(label=BasyoList[3], data=BasyoList[3], text=BasyoList[3])
                      ]),
                      CarouselColumn(text="2/2", actions=[
                                                PostbackAction(label=BasyoList[4], data=BasyoList[4], text=BasyoList[4]),
                                                PostbackAction(label=BasyoList[5], data=BasyoList[5], text=BasyoList[5]),
                                                PostbackAction(label=BasyoList[6], data=BasyoList[6], text=BasyoList[6])
                      ])
                  ])
              elif len(kwsiBasyoList) == 8:
                  carousel_template = CarouselTemplate(columns=[
                      CarouselColumn(text="1/2", actions=[
                                                PostbackAction(label=BasyoList[0], data=BasyoList[0], text=BasyoList[0]),
                                                PostbackAction(label=BasyoList[1], data=BasyoList[1], text=BasyoList[1]),
                                                PostbackAction(label=BasyoList[2], data=BasyoList[2], text=BasyoList[2]),
                                                PostbackAction(label=BasyoList[3], data=BasyoList[3], text=BasyoList[3])
                      ]),
                      CarouselColumn(text="2/2", actions=[
                                                PostbackAction(label=BasyoList[4], data=BasyoList[4], text=BasyoList[4]),
                                                PostbackAction(label=BasyoList[5], data=BasyoList[5], text=BasyoList[5]),
                                                PostbackAction(label=BasyoList[6], data=BasyoList[6], text=BasyoList[6]),
                                                PostbackAction(label=BasyoList[7], data=BasyoList[7], text=BasyoList[7])
                      ])
                  ])
              elif len(kwsiBasyoList) == 9:
                  carousel_template = CarouselTemplate(columns=[
                      CarouselColumn(text="1/3", actions=[
                                                PostbackAction(label=BasyoList[0], data=BasyoList[0], text=BasyoList[0]),
                                                PostbackAction(label=BasyoList[1], data=BasyoList[1], text=BasyoList[1]),
                                                PostbackAction(label=BasyoList[2], data=BasyoList[2], text=BasyoList[2]),
                                                PostbackAction(label=BasyoList[3], data=BasyoList[3], text=BasyoList[3])
                      ]),
                      CarouselColumn(text="2/3", actions=[
                                                PostbackAction(label=BasyoList[4], data=BasyoList[4], text=BasyoList[4]),
                                                PostbackAction(label=BasyoList[5], data=BasyoList[5], text=BasyoList[5]),
                                                PostbackAction(label=BasyoList[6], data=BasyoList[6], text=BasyoList[6]),
                                                PostbackAction(label=BasyoList[7], data=BasyoList[7], text=BasyoList[7])
                      ]),
                      CarouselColumn(text="3/3", actions=[
                                                PostbackAction(label=BasyoList[8], data=BasyoList[8], text=BasyoList[8])
                      ])
                  ])
              elif len(kwsiBasyoList) == 10:
                  carousel_template = CarouselTemplate(columns=[
                      CarouselColumn(text="1/3", actions=[
                                                PostbackAction(label=BasyoList[0], data=BasyoList[0], text=BasyoList[0]),
                                                PostbackAction(label=BasyoList[1], data=BasyoList[1], text=BasyoList[1]),
                                                PostbackAction(label=BasyoList[2], data=BasyoList[2], text=BasyoList[2]),
                                                PostbackAction(label=BasyoList[3], data=BasyoList[3], text=BasyoList[3])
                      ]),
                      CarouselColumn(text="2/3", actions=[
                                                PostbackAction(label=BasyoList[4], data=BasyoList[4], text=BasyoList[4]),
                                                PostbackAction(label=BasyoList[5], data=BasyoList[5], text=BasyoList[5]),
                                                PostbackAction(label=BasyoList[6], data=BasyoList[6], text=BasyoList[6]),
                                                PostbackAction(label=BasyoList[7], data=BasyoList[7], text=BasyoList[7])
                      ]),
                      CarouselColumn(text="3/3", actions=[
                                                PostbackAction(label=BasyoList[8], data=BasyoList[8], text=BasyoList[8]),
                                                PostbackAction(label=BasyoList[9], data=BasyoList[9], text=BasyoList[9])
                      ])
                  ])
              elif len(kwsiBasyoList) == 11:
                  carousel_template = CarouselTemplate(columns=[
                      CarouselColumn(text="1/3", actions=[
                                                PostbackAction(label=BasyoList[0], data=BasyoList[0], text=BasyoList[0]),
                                                PostbackAction(label=BasyoList[1], data=BasyoList[1], text=BasyoList[1]),
                                                PostbackAction(label=BasyoList[2], data=BasyoList[2], text=BasyoList[2]),
                                                PostbackAction(label=BasyoList[3], data=BasyoList[3], text=BasyoList[3])
                      ]),
                      CarouselColumn(text="2/3", actions=[
                                                PostbackAction(label=BasyoList[4], data=BasyoList[4], text=BasyoList[4]),
                                                PostbackAction(label=BasyoList[5], data=BasyoList[5], text=BasyoList[5]),
                                                PostbackAction(label=BasyoList[6], data=BasyoList[6], text=BasyoList[6]),
                                                PostbackAction(label=BasyoList[7], data=BasyoList[7], text=BasyoList[7])
                      ]),
                      CarouselColumn(text="3/3", actions=[
                                                PostbackAction(label=BasyoList[8], data=BasyoList[8], text=BasyoList[8]),
                                                PostbackAction(label=BasyoList[9], data=BasyoList[9], text=BasyoList[9]),
                                                PostbackAction(label=BasyoList[10], data=BasyoList[10], text=BasyoList[10])
                      ])
                  ])
              elif len(kwsiBasyoList) == 12:
                  carousel_template = CarouselTemplate(columns=[
                      CarouselColumn(text="1/3", actions=[
                                                PostbackAction(label=BasyoList[0], data=BasyoList[0], text=BasyoList[0]),
                                                PostbackAction(label=BasyoList[1], data=BasyoList[1], text=BasyoList[1]),
                                                PostbackAction(label=BasyoList[2], data=BasyoList[2], text=BasyoList[2]),
                                                PostbackAction(label=BasyoList[3], data=BasyoList[3], text=BasyoList[3])
                      ]),
                      CarouselColumn(text="2/3", actions=[
                                                PostbackAction(label=BasyoList[4], data=BasyoList[4], text=BasyoList[4]),
                                                PostbackAction(label=BasyoList[5], data=BasyoList[5], text=BasyoList[5]),
                                                PostbackAction(label=BasyoList[6], data=BasyoList[6], text=BasyoList[6]),
                                                PostbackAction(label=BasyoList[7], data=BasyoList[7], text=BasyoList[7])
                      ]),
                      CarouselColumn(text="3/3", actions=[
                                                PostbackAction(label=BasyoList[8], data=BasyoList[8], text=BasyoList[8]),
                                                PostbackAction(label=BasyoList[9], data=BasyoList[9], text=BasyoList[9]),
                                                PostbackAction(label=BasyoList[10], data=BasyoList[10], text=BasyoList[10]),
                                                PostbackAction(label=BasyoList[11], data=BasyoList[11], text=BasyoList[11])
                      ])
                  ])
              elif len(kwsiBasyoList) == 13:
                  carousel_template = CarouselTemplate(columns=[
                      CarouselColumn(text="1/4", actions=[
                                                PostbackAction(label=BasyoList[0], data=BasyoList[0], text=BasyoList[0]),
                                                PostbackAction(label=BasyoList[1], data=BasyoList[1], text=BasyoList[1]),
                                                PostbackAction(label=BasyoList[2], data=BasyoList[2], text=BasyoList[2]),
                                                PostbackAction(label=BasyoList[3], data=BasyoList[3], text=BasyoList[3])
                      ]),
                      CarouselColumn(text="2/4", actions=[
                                                PostbackAction(label=BasyoList[4], data=BasyoList[4], text=BasyoList[4]),
                                                PostbackAction(label=BasyoList[5], data=BasyoList[5], text=BasyoList[5]),
                                                PostbackAction(label=BasyoList[6], data=BasyoList[6], text=BasyoList[6]),
                                                PostbackAction(label=BasyoList[7], data=BasyoList[7], text=BasyoList[7])
                      ]),
                      CarouselColumn(text="3/4", actions=[
                                                PostbackAction(label=BasyoList[8], data=BasyoList[8], text=BasyoList[8]),
                                                PostbackAction(label=BasyoList[9], data=BasyoList[9], text=BasyoList[9]),
                                                PostbackAction(label=BasyoList[10], data=BasyoList[10], text=BasyoList[10]),
                                                PostbackAction(label=BasyoList[11], data=BasyoList[11], text=BasyoList[11])
                      ]),
                      CarouselColumn(text="4/4", actions=[
                                                PostbackAction(label=BasyoList[12], data=BasyoList[12], text=BasyoList[12])
                      ])
                  ])
              elif len(kwsiBasyoList) == 14:
                  carousel_template = CarouselTemplate(columns=[
                      CarouselColumn(text="1/4", actions=[
                                                PostbackAction(label=BasyoList[0], data=BasyoList[0], text=BasyoList[0]),
                                                PostbackAction(label=BasyoList[1], data=BasyoList[1], text=BasyoList[1]),
                                                PostbackAction(label=BasyoList[2], data=BasyoList[2], text=BasyoList[2]),
                                                PostbackAction(label=BasyoList[3], data=BasyoList[3], text=BasyoList[3])
                      ]),
                      CarouselColumn(text="2/4", actions=[
                                                PostbackAction(label=BasyoList[4], data=BasyoList[4], text=BasyoList[4]),
                                                PostbackAction(label=BasyoList[5], data=BasyoList[5], text=BasyoList[5]),
                                                PostbackAction(label=BasyoList[6], data=BasyoList[6], text=BasyoList[6]),
                                                PostbackAction(label=BasyoList[7], data=BasyoList[7], text=BasyoList[7])
                      ]),
                      CarouselColumn(text="3/4", actions=[
                                                PostbackAction(label=BasyoList[8], data=BasyoList[8], text=BasyoList[8]),
                                                PostbackAction(label=BasyoList[9], data=BasyoList[9], text=BasyoList[9]),
                                                PostbackAction(label=BasyoList[10], data=BasyoList[10], text=BasyoList[10]),
                                                PostbackAction(label=BasyoList[11], data=BasyoList[11], text=BasyoList[11])
                      ]),
                      CarouselColumn(text="4/4", actions=[
                                                PostbackAction(label=BasyoList[12], data=BasyoList[12], text=BasyoList[12]),
                                                PostbackAction(label=BasyoList[13], data=BasyoList[13], text=BasyoList[13])
                      ])
                  ])
              elif len(kwsiBasyoList) == 15:
                  carousel_template = CarouselTemplate(columns=[
                      CarouselColumn(text="1/4", actions=[
                                                PostbackAction(label=BasyoList[0], data=BasyoList[0], text=BasyoList[0]),
                                                PostbackAction(label=BasyoList[1], data=BasyoList[1], text=BasyoList[1]),
                                                PostbackAction(label=BasyoList[2], data=BasyoList[2], text=BasyoList[2]),
                                                PostbackAction(label=BasyoList[3], data=BasyoList[3], text=BasyoList[3])
                      ]),
                      CarouselColumn(text="2/4", actions=[
                                                PostbackAction(label=BasyoList[4], data=BasyoList[4], text=BasyoList[4]),
                                                PostbackAction(label=BasyoList[5], data=BasyoList[5], text=BasyoList[5]),
                                                PostbackAction(label=BasyoList[6], data=BasyoList[6], text=BasyoList[6]),
                                                PostbackAction(label=BasyoList[7], data=BasyoList[7], text=BasyoList[7])
                      ]),
                      CarouselColumn(text="3/4", actions=[
                                                PostbackAction(label=BasyoList[8], data=BasyoList[8], text=BasyoList[8]),
                                                PostbackAction(label=BasyoList[9], data=BasyoList[9], text=BasyoList[9]),
                                                PostbackAction(label=BasyoList[10], data=BasyoList[10], text=BasyoList[10]),
                                                PostbackAction(label=BasyoList[11], data=BasyoList[11], text=BasyoList[11])
                      ]),
                      CarouselColumn(text="4/4", actions=[
                                                PostbackAction(label=BasyoList[12], data=BasyoList[12], text=BasyoList[12]),
                                                PostbackAction(label=BasyoList[13], data=BasyoList[13], text=BasyoList[13]),
                                                PostbackAction(label=BasyoList[14], data=BasyoList[14], text=BasyoList[14])
                      ])
                  ])
              elif len(kwsiBasyoList) == 16:
                  carousel_template = CarouselTemplate(columns=[
                      CarouselColumn(text="1/4", actions=[
                                                PostbackAction(label=BasyoList[0], data=BasyoList[0], text=BasyoList[0]),
                                                PostbackAction(label=BasyoList[1], data=BasyoList[1], text=BasyoList[1]),
                                                PostbackAction(label=BasyoList[2], data=BasyoList[2], text=BasyoList[2]),
                                                PostbackAction(label=BasyoList[3], data=BasyoList[3], text=BasyoList[3])
                      ]),
                      CarouselColumn(text="2/4", actions=[
                                                PostbackAction(label=BasyoList[4], data=BasyoList[4], text=BasyoList[4]),
                                                PostbackAction(label=BasyoList[5], data=BasyoList[5], text=BasyoList[5]),
                                                PostbackAction(label=BasyoList[6], data=BasyoList[6], text=BasyoList[6]),
                                                PostbackAction(label=BasyoList[7], data=BasyoList[7], text=BasyoList[7])
                      ]),
                      CarouselColumn(text="3/4", actions=[
                                                PostbackAction(label=BasyoList[8], data=BasyoList[8], text=BasyoList[8]),
                                                PostbackAction(label=BasyoList[9], data=BasyoList[9], text=BasyoList[9]),
                                                PostbackAction(label=BasyoList[10], data=BasyoList[10], text=BasyoList[10]),
                                                PostbackAction(label=BasyoList[11], data=BasyoList[11], text=BasyoList[11])
                      ]),
                      CarouselColumn(text="4/4", actions=[
                                                PostbackAction(label=BasyoList[12], data=BasyoList[12], text=BasyoList[12]),
                                                PostbackAction(label=BasyoList[13], data=BasyoList[13], text=BasyoList[13]),
                                                PostbackAction(label=BasyoList[14], data=BasyoList[14], text=BasyoList[14]),
                                                PostbackAction(label=BasyoList[15], data=BasyoList[15], text=BasyoList[15])
                      ])
                  ])


              template_message = TemplateSendMessage(
                  alt_text="お探しの場所が見つかりませんでした…\nお手数ですが、つぎの中から選んでください。" , template=carousel_template)
              line_bot_api.reply_message(
                  event.reply_token, 
                  [TextSendMessage(text="お探しの場所が見つかりませんでした…\nお手数ですが、つぎの中から選んでください。"),
                  template_message])
              MySession.update_context(user_id, "10")

###############################

#2か所の場所を聞く####################
    elif MySession.read_context(user_id) == "0" and ("県" in talk and "から" in talk):
       if "2" in talk or "２" in talk or "二" in talk:
          MySession.reset(user_id)
          line_bot_api.reply_message(
               event.reply_token,
               TextSendMessage(text=tellDay2_1 + " (1/7)"))
          MySession.update_context(user_id, "20")
          MySession.update_count(user_id, 0)
       else:
          line_bot_api.reply_message(
               event.reply_token,
               TextSendMessage(text=tellDayError))

#出発する日にちを聞く
    elif MySession.read_context(user_id) == "20":
       if ("今日" in talk or "きょう" in talk) or ("明日" in talk or "あした" in talk) or ("明後日" in talk or "あさって" in talk):
           if "今日" in talk or "きょう" in talk:    MySession.update_date(user_id, 0)
           elif "明日" in talk or "あした" in talk: MySession.update_date(user_id, 1)
           else:                                                       MySession.update_date(user_id, 2)
           line_bot_api.reply_message(
           event.reply_token,
           TextSendMessage(text=tellBasyo2_1 + " (2/7)"))
           MySession.update_context(user_id, "21")
       else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="「今日」、「明日」、「明後日」の中から入力してください。"))

#出発地の場所を聞く
    elif MySession.read_context(user_id) == "21":
       if talk in todoufuken:
          MySession.update_areaT(user_id, talk)
          TBasyo = todoufukenNum(int(todoufuken.index(talk)))
          #TBasyoは文字型
          MySession.update_area(user_id, TBasyo)
          #area, basyoListは文字型
          kwsiBasyoList = codeKaraFind(MySession.read_area(user_id))
          MySession.update_basyoList(user_id, kwsiBasyoList)
          line_bot_api.reply_message(
               event.reply_token,
               TextSendMessage(text=(talk + tellBasyoKwsk2_1 + " (3/7)" + MySession.read_basyoList(user_id))))
          MySession.update_context(user_id, "22")
       else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="出発地" + tellBasyoError))

#出発地の場所の詳細を聞く
    elif MySession.read_context(user_id) == "22":
       if talk in MySession.read_basyoList(user_id):
          MySession.update_area(user_id, talk)
          line_bot_api.reply_message(
               event.reply_token,
               TextSendMessage(text=("出発地は" + MySession.read_areaT(user_id) + talk + tellDay2_2 + " (4/7)")))
          MySession.update_context(user_id, "23")
       else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text= tellBasyoKwskError +  MySession.read_basyoList(user_id)))


#目的地に到着する日にちを聞く
    elif MySession.read_context(user_id) == "23":
       if ("今日" in talk or "きょう" in talk) or ("明日" in talk or "あした" in talk) or ("明後日" in talk or "あさって" in talk):
           if "今日" in talk or "きょう" in talk:    MySession.update_date2(user_id, 0)
           elif "明日" in talk or "あした" in talk: MySession.update_date2(user_id, 1)
           else:                                                       MySession.update_date2(user_id, 2)
           line_bot_api.reply_message(
           event.reply_token,
           TextSendMessage(text=tellBasyo2_2 + " (5/7)"))
           MySession.update_context(user_id, "24")
       else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="「今日」、「明日」、「明後日」の中から入力してください。"))

#目的地の場所を聞く
    elif MySession.read_context(user_id) == "24":
       if talk in todoufuken:
          MySession.update_areaT2(user_id, talk)
          TBasyo2 = todoufukenNum(int(todoufuken.index(talk)))
          #TBasyoは文字型
          MySession.update_area2(user_id, TBasyo2)
          #area, basyoListは文字型
          kwsiBasyoList2 = codeKaraFind(MySession.read_area2(user_id))
          MySession.update_basyoList2(user_id, kwsiBasyoList2)
          line_bot_api.reply_message(
               event.reply_token,
               TextSendMessage(text=(talk + tellBasyoKwsk2_2 + " (6/7)" + MySession.read_basyoList2(user_id))))
          MySession.update_context(user_id, "25")
       else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="目的地" + tellBasyoError))

#目的地の場所の詳細を聞く
    elif MySession.read_context(user_id) == "25":
       if talk in MySession.read_basyoList2(user_id):
          MySession.update_area2(user_id, talk)
          line_bot_api.reply_message(
               event.reply_token,
               TextSendMessage(text=("目的地は" + MySession.read_areaT2(user_id) + talk + tellHotOrCold + " (7/7)")))
          MySession.update_context(user_id, "26")
       else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text= tellBasyoKwskError +  MySession.read_basyoList2(user_id)))

#体調を聞く&2か所の天気情報と総合情報を教える
    elif MySession.read_context(user_id) == "26":
       if "暑" in talk or "あつ" in talk or "寒" in talk or "さむ" in talk or "どちら" in talk or "どっち" in talk or "該当" in talk:
          if "暑" in talk or "あつ" in talk:
              MySession.update_para(user_id, 4)
              para = 4
          elif "寒" in talk or "さむ" in talk:
              MySession.update_para(user_id, -2)
              para = -2
          elif "どちら" in talk or "どっち" in talk or "該当" in talk:
              MySession.update_para(user_id, 1)
              para = 1
          picUrlS = picUrlMaker(needWeatherMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id)))
          tenkiInfoS = OtenkiMessageMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id))
          picUrlM = picUrlMaker(needWeatherMaker(Tcode[Tname.index(MySession.read_area2(user_id))], MySession.read_date2(user_id)))
          tenkiInfoM = OtenkiMessageMaker(Tcode[Tname.index(MySession.read_area2(user_id))], MySession.read_date2(user_id))
          STM = tempMEANMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id))
          MTM = tempMEANMaker(Tcode[Tname.index(MySession.read_area2(user_id))], MySession.read_date(user_id))
          fukusouInfo = fukusouHantei2(STM, MTM, para)
          ST = MySession.read_areaT(user_id) + MySession.read_area(user_id)
          MT = MySession.read_areaT2(user_id) + MySession.read_area2(user_id)
          kasaInfo = kasaHantei2(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id), Tcode[Tname.index(MySession.read_area2(user_id))], MySession.read_date2(user_id), ST, MT)
          kionnInfo = kionnHantei(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id))
          caution = ""
          if "だめです" in kionnInfo and "傘情報を取得できませんでした" in kasaInfo: caution="\n\n※「今日」の天気情報で情報取得時刻が遅い場合、正常に情報を取得できないことがあります。"
          if picUrlS == "未知の天気" or picUrlM == "未知の天気":
               line_bot_api.reply_message(
                    event.reply_token,
                    [TextSendMessage(text=MySession.read_areaT(user_id) + MySession.read_area(user_id) + "から" + MySession.read_areaT2(user_id) + MySession.read_area2(user_id) + "への天気情報を表示します！"),
                    TextSendMessage(text="[出発地]" + MySession.read_areaT(user_id) + MySession.read_area(user_id) + "\n" + tenkiInfoS),
                    TextSendMessage(text="[目的地]" + MySession.read_areaT2(user_id) + MySession.read_area2(user_id) + "\n" + tenkiInfoM),
                    TextSendMessage(text=kasaInfo),
                    TextSendMessage(text=fukusouInfo + caution)])
          else:
               line_bot_api.reply_message(
                    event.reply_token,
                    #メッセージは1～5個まで
                    [#TextSendMessage(text=MySession.read_areaT(user_id) + MySession.read_area(user_id) + "から" + MySession.read_areaT2(user_id) + MySession.read_area2(user_id) + "への天気情報を表示します！"),
                    TextSendMessage(text="[出発地]" + MySession.read_areaT(user_id) + MySession.read_area(user_id) + "\n" + tenkiInfoS),
                    ImageSendMessage(original_content_url=picUrlS, preview_image_url=picUrlS),
                    TextSendMessage(text="[目的地]" + MySession.read_areaT2(user_id) + MySession.read_area2(user_id) + "\n" + tenkiInfoM),
                    ImageSendMessage(original_content_url=picUrlM, preview_image_url=picUrlM),
                    TextSendMessage(text=kasaInfo + "\n\n" +fukusouInfo + caution)])
          MySession.reset(user_id)
       else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=tellHotOrColdError))

###############################

#基礎info#########################
    elif MySession.read_context(user_id) == "0" and ("バージョン" in talk or "ver" in talk or "ばーじょん" in talk):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "現在のバージョンはver1.0です。"))
#フォグ君が追加されたらアンケートに一個メッセージを追加する
    elif MySession.read_context(user_id) == "0" and ("アンケート" in talk or "questionnaire" in talk or "あんけーと" in talk) and talk != "アンケート回答した":
        line_bot_api.reply_message(
            event.reply_token,
           [TextSendMessage(text = "↓アンケートはこちらから\nhttps://forms.office.com/r/890X6LLyRU"),
           TextSendMessage(text = "アンケートでは、あなたが現在使用している天気予報のアプリやシステムなどと比べ、WeatherNewsBotがどれくらい便利か、システムの完成度や利便性はどの程度か、追加してほしい機能や不満点、バグの有無などについてお伺いしています。")])
           #TextSendMEssage(text = "ver1.1では、ver1.0を利用した方と利用されていない方で別にアンケート項目を設けております(ver1.0からご利用いただいている方は、1.0の時に比べどの程度改善したかなどを伺っています)。さらに、WeatherNewsBotのマスコットキャラクター「フォグ」との会話を意識したアップデートを通して使用意欲の向上があったか、知名度や利用者の増加は見込めるかなどについてもお伺いしています")])
###############################

#その他の会話#######################
    #'''
    elif MySession.read_context(user_id) == "0" and ("狐" in talk or "キツネ" in talk or "きつね" in talk):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = teachKituneTenki))
    elif MySession.read_context(user_id) == "0" and ("鳥" in talk or "ツバメ" in talk):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = teachTubameTenki))
    elif MySession.read_context(user_id) == "0" and ("猫" in talk or "ネコ" in talk or "ねこ" in talk):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = teachNekoTenki))
    elif MySession.read_context(user_id) == "0" and ("蜘蛛" in talk or "クモ" in talk or "くも" in talk):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = teachKumonosuTenki))
    elif MySession.read_context(user_id) == "0" and (talk == "のみもの" or talk == "飲み物"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = sukinaNomimono))
    elif MySession.read_context(user_id) == "0" and (talk == "たべもの" or talk == "食べ物"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = sukinaTabemono))
    elif MySession.read_context(user_id) == "0" and (("犬" in talk or "猫" in talk or "虎" in talk or "鳥" in talk) and "が良かった" in talk):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "ボクじゃ…だめですか…？(ｳﾙｳﾙ)"))
    elif MySession.read_context(user_id) == "0" and (("君" in talk or "あなた" in talk or "フォグ" in talk) and "化か" in talk):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = bakasanaidesu))
    elif MySession.read_context(user_id) == "0" and (talk == "フォグ" or talk == "フォグくん" or talk == "フォグ君" or talk == "フォグさん"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = FogDesu))
    elif MySession.read_context(user_id) == "0" and talk == "自己紹介してくれる？":
        line_bot_api.reply_message(
            event.reply_token,
            [ImageSendMessage(original_content_url=FogDesuPic, preview_image_url=FogDesuPic),
            TextSendMessage(text = jikosyoukai)])
    elif MySession.read_context(user_id) == "0" and talk == "卒研が終わらない" or talk == "卒研終わらない" or talk == "卒研終わらん" or talk == "卒研が終わらん" or talk == "卒研詰んでる" or talk == "卒研が詰んでる" or talk == "卒研終わってる" or talk == "卒研が終わってる":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "それは大変です！急いで頑張らないと…ですが、頑張りすぎて根を詰めちゃうのはダメですよ！ときには一人で抱え込まず誰かに相談すると少しは焦る気持ちも楽になるかもしれません。\nボクもここからあなたことを応援してますよ、ファイトです！"))
    elif MySession.read_context(user_id) == "0" and talk == "その帽子って？":
        b = random.randint(0, len(bousiInfo)) - 1
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = bousiInfo[b]))
    elif MySession.read_context(user_id) == "0" and talk == "制作秘話":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = seisakuhiwa))
    elif MySession.read_context(user_id) == "0" and talk == "意識していること" or talk == "気をつけていること" :
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "ボクは ウソや言い訳をしない ということを肝に銘じています。そんなことをしてもなにもいいことは無いですからね。\n最近ウソをついたことはあるか、ですか？…も、もちろんあるわけないじゃないですか。ウソじゃないですよ？…ウソじゃないもんっ！"))
    elif MySession.read_context(user_id) == "0" and (talk == "さみしい" or talk == "寂しい" or talk == "淋しい" or talk == "つらい" or talk == "しんどい" or talk == "消えたい"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = bokugaimasuyo))
    elif MySession.read_context(user_id) == "0" and talk == "雑談しよう":
        x = random.randint(0, len(zatudan)) - 1
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = zatudan[x]))
    elif MySession.read_context(user_id) == "0" and (talk == "おはよう" or talk == "おはようございます" or talk == "おはよう！" or talk == "おはようございます！"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "おはようございます！今日も一日がんばりましょう！"))
    elif MySession.read_context(user_id) == "0" and talk == "こんにちは" or talk == "こんにちは！":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "こんにちはです！今日もお仕事やお勉強は順調に進んでいますか？頑張るのも大事ですが、適度に休憩するもの大事ですよ！"))
    elif MySession.read_context(user_id) == "0" and talk == "こんばんは" or talk == "こんばんは！":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "こんばんはです！今日も一日お疲れさまでした！疲れたなと思ったらすぐに休むのが大事ですよ。明日の天気のチェックもお忘れなく！"))
    elif MySession.read_context(user_id) == "0" and (talk == "優しいね" or talk == "お気遣いありがとう" or talk == "お気遣いどうも" or talk == "お気遣いありがとうございます" or talk == "優しい" or talk == "やさしいね" or talk == "やさしい" or talk == "いい子だね" or talk == "いいコだね" or talk == "いい仔だね"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "いえいえ！"))
    elif MySession.read_context(user_id) == "0" and (talk == "元気？" or talk == "調子どう？"):
        line_bot_api.reply_message(
            event.reply_token,
            [ImageSendMessage(original_content_url=keireiFogPic, preview_image_url=keireiFogPic),
            TextSendMessage(text = genki)])
    elif MySession.read_context(user_id) == "0" and talk == "後悔":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = koukaisitemo))
    elif MySession.read_context(user_id) == "0" and (talk == "愛" or talk == "恋"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = koinokatikann))
    elif MySession.read_context(user_id) == "0" and "どこ" in talk and "いる" in talk and "？" in talk:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = imanobasyo))
    elif MySession.read_context(user_id) == "0" and talk == "今何してる？" or talk == "今何してるの？":
        #レアセリフは1%の確率で聞ける
        if random.randint(0, 99) == 0: imanani = imananisiteruRare
        else:
            i = random.randint(0, len(imananisiteru)) - 1
            imanani = imananisiteru[i]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = imanani))
    elif MySession.read_context(user_id) == "0" and (talk == "疲れた" or talk == "仕事疲れた" or talk == "つかれた" or talk == "仕事つかれた"):
        line_bot_api.reply_message(
            event.reply_token,
            [ImageSendMessage(original_content_url=osyaberiFogPic, preview_image_url=osyaberiFogPic),
            TextSendMessage(text = negirai)])
    elif MySession.read_context(user_id) == "0" and (talk == "しね" or talk == "死ね" or talk == "きえろ" or talk == "消えろ" or talk == "嫌い" or talk == "きらい" or talk == "気に食わない" or talk == "殺す" or talk == "ころす"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "そ、そんなひどいコト言わないでくださいっ！ぐすんっ…"))
    elif MySession.read_context(user_id) == "0" and (talk == "こんぺいとう" or talk ==  "ツナマヨ" or talk == "ツナマヨネーズ"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "じゅるり…"))
    elif MySession.read_context(user_id) == "0" and (("君" in talk or "あなた" in talk or "フォグ" in talk or "おまえ" in talk or "お前" in talk) and "食べ" in talk):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "ひぇっ…ボ、ボクを食べてもおいしくないですよっ！"))
    elif MySession.read_context(user_id) == "0" and ("こんぺいとう" in talk and ("あげる" in talk or "食べる？" in talk or "たべる？" in talk)):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = getKonpeitou))
    elif MySession.read_context(user_id) == "0" and (("ツナマヨ" in talk or "ツナマヨネーズ" in talk) and ("あげる" in talk or "食べる？" in talk or "たべる？" in talk)):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = getTunamayo))
    elif MySession.read_context(user_id) == "0" and (talk == "頑張って" or talk == "頑張ってるね" or talk == "がんばって" or talk == "がんばってるね" or talk == "お仕事頑張って" or talk == "お仕事頑張ってるね" or talk == "お仕事がんばって" or talk == "お仕事がんばってるね" or talk == "お仕事ご苦労様" or talk == "ご苦労様" or talk == "お仕事ごくろうさま" or talk == "ごくろうさま" or talk == "真面目だね" or talk == "真面目やね"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "お気遣いありがとうございます！" + user_name + "さんも頑張って下さい！ただ、無理だけはしちゃダメですよ～！"))
    elif MySession.read_context(user_id) == "0" and (talk == "かわいい" or talk == "かわいいね"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "えへへ、ありがとうございます！"))
    elif MySession.read_context(user_id) == "0" and (talk == "ありがとうね" or talk == "ありがとう" or talk == "教えてくれてありがとう" or talk == "お仕事ご苦労様" or talk == "お仕事えらいね" or talk == "お仕事偉いね" or talk == "お仕事がんばってるね" or talk == "お仕事がんばってね" or talk == "お気遣いありがとう"):
        thanks = ""
        if talk == "教えてくれてありがとう" or talk == "ありがとうね" or talk == "ありがとう": thanks = "こちらこそ、ご利用くださり誠に"
        line_bot_api.reply_message(
            event.reply_token,
            [ImageSendMessage(original_content_url=keireiFogPic, preview_image_url=keireiFogPic),
            TextSendMessage(text = thanks + "ありがとうございます！" + user_name +"さんのお役に立てるよう、精一杯頑張ります！")])
    elif MySession.read_context(user_id) == "0" and (talk == "もういらない" or talk == "お前を消す方法"):
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text = mouiranai),
            TextSendMessage(text = howToUninstallPC),
            TextSendMessage(text = howToUninstallSP),
            TextSendMessage(text = user_name + "さん、今までお世話になりました。これからもお体に気を付けて元気でお過ごし下さい。\n\n(ぐすっ、さようならっ…)")])
    elif MySession.read_context(user_id) == "0" and (talk == "使うのを止めたい" or talk == "botの消し方" or talk == "botの消し方を教えて" or talk == "チャットの消し方" or talk == "チャットの止め方" or talk == "チャットの消し方を教えて" or talk == "チャットの止め方を教えて" or talk == "トークの消し方" or talk == "トークの止め方" or talk == "トークの消し方を教えて" or talk == "トークの止め方を教えて" or talk == "botの削除" or talk == "botの削除方法"):
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text = imamadearigatou),
            TextSendMessage(text = howToUninstallPC),
            TextSendMessage(text = howToUninstallSP),
            TextSendMessage(text = user_name + "さん、今までお世話になりました。これからもお体に気を付けて元気でお過ごし下さい！")])
    elif MySession.read_context(user_id) == "0" and (talk == "おやすみ" or talk == "おやすみなさい" or talk == "お休み" or talk == "お休みなさい" or talk == "寝ます" or talk == "寝る" or talk == "ねます" or talk == "ねる" or talk == "眠い" or talk == "ねむい" or talk == "眠たい" or talk == "ねむたい" or talk == "寝不足" or talk == "ねぶそく"):
        nemuitokiha = ""
        if talk == "眠い" or talk == "ねむい" or talk == "眠たい" or talk == "ねむたい": nemuitokiha = "眠たいときは素直に寝ちゃうのがイチバンですよ！"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = nemuitokiha + netyaimasyou))
        MySession.update_oyasumi(user_id, 11)
    elif MySession.read_context(user_id) == "0" and (talk == "寝なよ" or talk == "寝てもいいよ" or talk == "一緒に寝よう" or talk == "休んでもいいよ" or talk == "休んじゃいなよ" or talk == "一緒に寝る？" or talk == "休んでもいいんじゃない？" or talk == "寝ちゃいなよ" or talk == "寝ちゃってもいいよ" or talk == "寝ちゃってもいいんじゃない？") and MySession.read_oyasumi(user_id) == 11:
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text = bokumonetyaou),
            TextSendMessage(text = user_name + "さん、おやすみなさいです…"),
            ImageSendMessage(original_content_url=oyasumiFogPic, preview_image_url=oyasumiFogPic)])
        MySession.update_oyasumi(user_id, 3)
    elif MySession.read_context(user_id) == "0" and (talk == "寝なよ" or talk == "寝てもいいよ" or talk == "一緒に寝よう" or talk == "休んでもいいよ" or talk == "休んじゃいなよ" or talk == "一緒に寝る？" or talk == "休んでもいいんじゃない？" or talk == "寝ちゃいなよ" or talk == "寝ちゃってもいいよ" or talk == "寝ちゃってもいいんじゃない？"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = madaneruwakeniha))
    elif MySession.read_context(user_id) == "0" and (talk == "git add" or talk == "git commit" or talk == "git push" or talk == "C" or talk == "C++" or talk == "C#" or talk == "Java" or talk == "JavaScript" or talk == "PHP" or talk == "Ruby" or talk == "TypeScript" or talk == "Python" or talk == "R言語" or talk == "GO言語" or talk == "Swift" or talk == "Kotlin" or talk == "Objective-C" or talk == "VisualBasic" or talk == "VBScript" or talk == "BASIC" or talk == "GoogleAppsScript" or talk == "Haskell" or talk == "Scala" or talk == "Groovy" or talk == "Delphi" or talk == "Dart" or talk == "D言語" or talk == "Perl" or talk == "COBOL" or talk == "SQL" or talk == "FORTRAN" or talk == "MATLAB" or talk == "Scratch"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "むむ、その言葉は...。さてはあなた、プログラミングしたことありますね？"))
    elif MySession.read_context(user_id) == "0" and talk == "heroku logs --tail":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "あっ！お世話になっております、ヘロクログさん！今日も--尻尾が素敵ですね！（？）"))
    elif MySession.read_context(user_id) == "0" and talk == "vore" or talk == "ボア"  or talk == "ぼあ":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "ぼあ？それってなんですか？\nうーん、ぼあ？なんだか背筋がぞわぞわするような…？"))
    elif MySession.read_context(user_id) == "0" and (((("性能" in talk or "精度" in talk) and ("悪い" in talk or "わるい" in talk)) or (("あて" in talk or "参考" in talk) and ("なら" in talk)) or talk == "使えない" or talk == "使えないね") or (talk == "嘘つき" or talk == "うそつき")):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = gomennnasai))
    elif MySession.read_context(user_id) == "0" and (talk == "ごみの捨て方" or talk == "捨て方" or talk == "分別" or talk == "分別方法" or talk == "ごみの分別" or talk == "ゴミの分別"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "あー...すみません、ごみの捨て方はボクの仕事の範疇ではないんです。ただ、頼りになる方を知っているのでご紹介いたしますね！\n墨田区のごみ捨て案内bot\n＜リンク＞\nhttps://www.city.sumida.lg.jp/kurashi/gomi_recycle/kateikei/oyakudachi/gomi-bunbetu-chatbot.html\n(右下の黒猫さん「すみにゃーる」を押すと利用開始です！)"))
    elif MySession.read_context(user_id) == "0" and talk == "スペシャルサンクス":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "このシステムを作るにあたり、ボクのキャラクターデザインのご意見などをイラストレーターのほまけさんから頂きました。ボクの面倒を見てくれてありがとうございました！ここからじゃボクの声は届かないだろうけど、この気持ちが届くといいな。"))
    elif MySession.read_context(user_id) == "0" and (talk == "バグ" or talk == "不具合" or talk == "バグある" or talk == "不具合ある" or talk == "バグってる" or talk == "不具合あったよ" or talk == "バグあったよ" or talk == "不具合見つけた" or talk == "不具合見つけたよ" or talk == "バグ見つけた" or talk == "バグ見つけたよ"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "バグがあったんですね！？不具合があり申し訳ございません！\n実施しているアンケートの中に[追加してほしい機能や不具合がありましたら、こちらにご記入ください]という欄がありますので、お手数をおかけしますがそちらに入力していただけますと幸いです！\nアンケートはこちらから↓\nhttps://forms.office.com/r/qep9rrbQKD"))
    elif MySession.read_context(user_id) == "0" and (talk == "－－－－　・－・－・　－・－・　・・－・　－・・・" or talk == "－・－・・　－－－－　－・－－－　－・・－　－－－・－　・－・・"):
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text = "ん、もーるす信号だ。えっと、えっと…これがこれで、これがこうかな…よし、送信っと。"),
            TextSendMessage(text = "－－－－　・－・－・　－・－・　・・－・　－・・・　・・－　－・－－－　－・－・－　・・　・－－・－　－・－・　－・・－－　・－－・－　－－－・－　－・・　・・　・・－・・　・－・－－　・・　－－－・－")])
    elif MySession.read_context(user_id) == "0" and talk == "見えるかな":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "きっとお父さんとお母さんは空から見てくれてますよ。そう、きっと。\nたから"))
    elif MySession.read_context(user_id) == "0" and talk == "アンケート回答した":
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text = ankeThanks1 + user_name + ankeThanks2),
            TextSendMessage(text = ankeThanks3),
            ImageSendMessage(original_content_url=ankeThanksPic, preview_image_url=ankeThanksPic)])
    elif MySession.read_context(user_id) == "0" and ("不満" in talk or  "ダメ" in talk):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = "至らない点があり申し訳ございません。\n実施しているアンケートの中で悪かった点や改善点などをお聞きしておりますので、お手数をおかけしますがそちらに入力していただけますと幸いです！\nアンケートはこちらから↓\nhttps://forms.office.com/r/qep9rrbQKD"))

    #'''
###############################

#該当しないメッセージが送られてきた場合#########
    else:

###'''で囲めばその間の行をコメントアウトできる
###以下は間違えすぎた時のBOTの反応######
      #'''
      MySession.update_count(user_id, MySession.read_count(user_id)+1)

      if MySession.read_count(user_id) >= 17:
          line_bot_api.reply_message(
              event.reply_token,
              TextSendMessage(text=kaiwa1_4))
      elif MySession.read_count(user_id) == 16:
          if talk == "うん" or talk == "せやで" or talk == "そうだよ" or talk == "そうだけど" or talk == "ばれた？":
              rep = talk + "って…からかわないでくださいよもう…。\nあれ、"
              line_bot_api.reply_message(
                  event.reply_token,
                  [ImageSendMessage(original_content_url=jitomeFogPic, preview_image_url=jitomeFogPic),
                  TextSendMessage(text=rep + kaiwa1_3)])
          else:
              line_bot_api.reply_message(
                  event.reply_token,
                  TextSendMessage(text=kaiwa1_3))
      elif MySession.read_count(user_id) == 15:
          line_bot_api.reply_message(
              event.reply_token,
              TextSendMessage(text=kaiwa1_2))
      elif MySession.read_count(user_id) > 10:
          line_bot_api.reply_message(
              event.reply_token,
              [TextSendMessage(text=kaiwa1_1),
              TextSendMessage(text=kaiwa1_1a)])
      else:
      #'''
############################
          line_bot_api.reply_message(
              event.reply_token,
              TextSendMessage(text="最初からやり直します。「1か所」or「2か所」を入力してください。"))
          #リプライはLineBotApiのメソッドを用いる。 第一引数のevent.reply_tokenはイベントの応答に
          #用いるトークン。 第二引数にはlinebot.modelsに定義されている返信用の
          #TextSendMessageオブジェクトを渡しています。

#ボタン操作はここから#################
(場合によっては市の情報合致しなかったパターンとは別に作る必要があるかもしれん)
#ボタンの入力を受け取るPostbackEvent
@handler.add(PostbackEvent)
def postback(event):
    user_id = event.soure.user_id
    postback_msg = event.postback.data

    if MySession.read_context(user_id) == "10":
        MySession.update_area(user_id, postback_msg)
        buttons_template = ButtonsTemplate(
            text="日時を選択してください。", actions=[
                PostbackAction(label="今日", data="今日", text="今日"),
                PostbackAction(label="明日", data="明日", text="明日"),
                PostbackAction(label="明後日", data="明後日", text="明後日")
            ])
        template_message = TemplateSendMessage(
            alt_text="日時を選択してください", template=buttons_template)
        line_bot_api.reply_message(
            event.reply_token, template_message)
        MySession.update_context(user_id, "11")

    if postback_msg == "今日" and MySession.read_context(user_id) == "11":
        MySession.update_date(user_id, 0)
        buttons_template = ButtonsTemplate(
            text="最も近いものは？", actions=[
                      PostbackAction(label="暑がり", data="暑がり", text="暑がり"),
                      PostbackAction(label="寒がり", data="寒がり", text="寒がり"),
                      PostbackAction(label="どちらでもない", data="どちらでもない", text="どちらでもない")
            ])
        template_message = TemplateSendMessage(
            alt_text="最も近いものは？", template=buttons_template)
        line_bot_api.reply_message(
            event.reply_token, template_message)
              MySession.update_context(user_id, "12")

    if postback_msg == "明日" and MySession.read_context(user_id) == "11":
        MySession.update_date(user_id, 1)
        buttons_template = ButtonsTemplate(
            text="最も近いものは？", actions=[
                      PostbackAction(label="暑がり", data="暑がり", text="暑がり"),
                      PostbackAction(label="寒がり", data="寒がり", text="寒がり"),
                      PostbackAction(label="どちらでもない", data="どちらでもない", text="どちらでもない")
            ])
        template_message = TemplateSendMessage(
            alt_text="最も近いものは？", template=buttons_template)
        line_bot_api.reply_message(
            event.reply_token, template_message)
              MySession.update_context(user_id, "12")

    if postback_msg == "明後日" and MySession.read_context(user_id) == "11":
        MySession.update_date(user_id, 2)
        buttons_template = ButtonsTemplate(
            text="最も近いものは？", actions=[
                      PostbackAction(label="暑がり", data="暑がり", text="暑がり"),
                      PostbackAction(label="寒がり", data="寒がり", text="寒がり"),
                      PostbackAction(label="どちらでもない", data="どちらでもない", text="どちらでもない")
            ])
        template_message = TemplateSendMessage(
            alt_text="最も近いものは？", template=buttons_template)
        line_bot_api.reply_message(
            event.reply_token, template_message)
              MySession.update_context(user_id, "12")


    if postback_msg == "暑がり" and MySession.read_context(user_id) == "12":
        MySession.update_para(user_id, 3)
        para = MySession.read_para(user_id)

        confirm_template = ConfirmTemplate(text="情報を保持しますか？", actions=[
            PostbackAction(label="はい", data="はい", text="はい"),
            PostbackAction(label="いいえ", data="いいえ", text="いいえ")
        ])
        template_message = TemplateSendMessage(
            alt_text="情報を保持しますか？", template=confirm_template)

        picUrl = picUrlMaker(needWeatherMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id)))
        fukusouInfo = fukusouHantei((tempMEANMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id)) + int(para)), needWeatherMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id)))
        tenkiInfo = OtenkiMessageMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id))
        kasaInfo = kasaHantei(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id))
        kionnInfo = kionnHantei(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id))
        caution = ""
        if "だめです" in kionnInfo or "傘情報を取得できませんでした" in kasaInfo: caution="\n\n※「今日」の天気情報で情報取得時刻が遅い場合、正常に情報を取得できないことがあります。"
        if picUrl == "未知の天気":
             line_bot_api.reply_message(
                  event.reply_token,
                  [TextSendMessage(text="それでは、" + day[MySession.read_date(user_id)] + "の" + MySession.read_areaT(user_id) + MySession.read_area(user_id) + "の天気情報を表示します！" + " (1/2)"),
                  TextSendMessage(text=tenkiInfo),
                  TextSendMessage(text=kasaInfo + fukusouInfo + caution),
                  template_message)])
        else:
             line_bot_api.reply_message(
                  event.reply_token,
                  [TextSendMessage(text="それでは、" + day[MySession.read_date(user_id)] + "の" + MySession.read_areaT(user_id) + MySession.read_area(user_id) + "の天気情報を表示します！" + " (1/2)"),
                  TextSendMessage(text=tenkiInfo),
                  ImageSendMessage(original_content_url=picUrl, preview_image_url=picUrl),
                  TextSendMessage(text=kasaInfo + fukusouInfo + caution),
                  template_message)])
        MySession.update_context(user_id, "13")

    if postback_msg == "どちらでもない" and MySession.read_context(user_id) == "12":
        MySession.update_para(user_id, 0)
        para = MySession.read_para(user_id)

        confirm_template = ConfirmTemplate(text="情報を保持しますか？", actions=[
            PostbackAction(label="はい", data="はい", text="はい"),
            PostbackAction(label="いいえ", data="いいえ", text="いいえ")
        ])
        template_message = TemplateSendMessage(
            alt_text="情報を保持しますか？", template=confirm_template)

        picUrl = picUrlMaker(needWeatherMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id)))
        fukusouInfo = fukusouHantei((tempMEANMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id)) + int(para)), needWeatherMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id)))
        tenkiInfo = OtenkiMessageMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id))
        kasaInfo = kasaHantei(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id))
        kionnInfo = kionnHantei(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id))
        caution = ""
        if "だめです" in kionnInfo or "傘情報を取得できませんでした" in kasaInfo: caution="\n\n※「今日」の天気情報で情報取得時刻が遅い場合、正常に情報を取得できないことがあります。"
        if picUrl == "未知の天気":
             line_bot_api.reply_message(
                  event.reply_token,
                  [TextSendMessage(text="それでは、" + day[MySession.read_date(user_id)] + "の" + MySession.read_areaT(user_id) + MySession.read_area(user_id) + "の天気情報を表示します！" + " (1/2)"),
                  TextSendMessage(text=tenkiInfo),
                  TextSendMessage(text=kasaInfo + fukusouInfo + caution),
                  template_message)])
        else:
             line_bot_api.reply_message(
                  event.reply_token,
                  [TextSendMessage(text="それでは、" + day[MySession.read_date(user_id)] + "の" + MySession.read_areaT(user_id) + MySession.read_area(user_id) + "の天気情報を表示します！" + " (1/2)"),
                  TextSendMessage(text=tenkiInfo),
                  ImageSendMessage(original_content_url=picUrl, preview_image_url=picUrl),
                  TextSendMessage(text=kasaInfo + fukusouInfo + caution),
                  template_message)])
        MySession.update_context(user_id, "13")

    if postback_msg == "寒がり" and MySession.read_context(user_id) == "12":
        MySession.update_para(user_id, -3)
        para = MySession.read_para(user_id)

        confirm_template = ConfirmTemplate(text="情報を保持しますか？", actions=[
            PostbackAction(label="はい", data="はい", text="はい"),
            PostbackAction(label="いいえ", data="いいえ", text="いいえ"),
        ])
        template_message = TemplateSendMessage(
            alt_text="情報を保持しますか？", template=confirm_template)

        picUrl = picUrlMaker(needWeatherMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id)))
        fukusouInfo = fukusouHantei((tempMEANMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id)) + int(para)), needWeatherMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id)))
        tenkiInfo = OtenkiMessageMaker(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id))
        kasaInfo = kasaHantei(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id))
        kionnInfo = kionnHantei(Tcode[Tname.index(MySession.read_area(user_id))], MySession.read_date(user_id))
        caution = ""
        if "だめです" in kionnInfo or "傘情報を取得できませんでした" in kasaInfo: caution="\n\n※「今日」の天気情報で情報取得時刻が遅い場合、正常に情報を取得できないことがあります。"
        if picUrl == "未知の天気":
             line_bot_api.reply_message(
                  event.reply_token,
                  [TextSendMessage(text="それでは、" + day[MySession.read_date(user_id)] + "の" + MySession.read_areaT(user_id) + MySession.read_area(user_id) + "の天気情報を表示します！" + " (1/2)"),
                  TextSendMessage(text=tenkiInfo),
                  TextSendMessage(text=kasaInfo + fukusouInfo + caution),
                  template_message)])
        else:
             line_bot_api.reply_message(
                  event.reply_token,
                  [TextSendMessage(text="それでは、" + day[MySession.read_date(user_id)] + "の" + MySession.read_areaT(user_id) + MySession.read_area(user_id) + "の天気情報を表示します！" + " (1/2)"),
                  TextSendMessage(text=tenkiInfo),
                  ImageSendMessage(original_content_url=picUrl, preview_image_url=picUrl),
                  TextSendMessage(text=kasaInfo + fukusouInfo + caution),
                  template_message)])
        MySession.update_context(user_id, "13")

        if postback_msg == "はい" and MySession.read_context(user_id) == "13":
            if MySession.read_date(user_id) == 0: date="今日"
            elif MySession.read_date(user_id) == 1: date="明日"
            elif MySession.read_date(user_id) == 2: date="明後日"
            if MySession.read_para(user_id) == 3: para="暑がり"
            elif MySession.read_para(user_id) == 0: para="どちらでもない"
            elif MySession.read_para(user_id) == -3: para="寒がり"
            line_bot_api.reply_message(
               event.reply_token,
               [TextSendMessage(text="情報保持しました！次回以降「いつもの」と入力すれば以下の条件で天気情報を検索できます！"),
               TextSendMessage(text="<日付>" + date + "\n<場所>" + MySession.read_areaT(user_id) + MySession.read_area(user_id) + "\n<体調>" + para),
               TextSendMessage(text="情報は次の1か所or2か所の天気情報検索時まで保持されます。")])
            MySession.update_context(user_id, "0")
            MySession.update_Hdate(user_id, MySession.read_date(user_id))
            MySession.update_Harea(user_id, MySession.read_area(user_id))
            MySession.update_HareaT(user_id, MySession.read_areaT(user_id))
            MySession.update_HbasyoList(user_id, MySession.read_HbasyoList(user_id))

        if postback_msg == "いいえ" and MySession.read_context(user_id) == "13":
            line_bot_api.reply_message(
               event.reply_token,
               TextSendMessage(text="保持しませんでした。またご利用になられる場合は「1か所」もしくは「2か所」を入力してください。"))
            #保持情報はいったん避難
            Hdate = MySession.read_Hdate(user_id)
            Harea = MySession.read_Harea(user_id)
            HareaT = MySession.read_HareaT(user_id)
            HbasyoList = MySession.read_HbasyoList(user_id)
            para = MySession.read_para(user_id)
            #全部消した後、
            MySession.reset(user_id)
            #保持情報を再度覚えさせる
            MySession.update_Hdate(user_id, Hdate)
            MySession.update_Harea(user_id, MySession.read_area(user_id))
            MySession.update_HareaT(user_id, MySession.read_areaT(user_id))
            MySession.update_HbasyoList(user_id, MySession.read_HbasyoList(user_id))
            MySession.update_para(user_id, para)
#############################
#############################


##################################
##############################################
##############################################

##################その他のinfo#####################
todoufuken=["北海道","青森県","岩手県","宮城県","秋田県","山形県","福島県",
"茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県",
"新潟県","富山県","石川県","福井県","山梨県","長野県","岐阜県",
"静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県",
"奈良県","和歌山県","鳥取県","島根県","岡山県","広島県","山口県",
"徳島県","香川県","愛媛県","高知県","福岡県","佐賀県","長崎県",
"熊本県","大分県","宮崎県","鹿児島県","沖縄県"]

day=["今日","明日","明後日"]

#DB使えないんだよね。。。
Tcode=['011000','012010','012020','013010','013020','013030','014010','014020','014030','015010',
'015020','016010','016020','016030','017010','017020','020010','020020','020030','030010',
'030020','030030','040010','040020','050010','050020','060010','060020','060030','060040',
'070010','070020','070030','080010','080020','090010','090020','100010','100020','110010',
'110020','110030','120010','120020','120030','130010','130020','130030','130040','140010',
'140020','150010','150020','150030','150040','160010','160020','170010','170020','180010',
'180020','190010','190020','200010','200020','200030','210010','210020','220010','220020',
'220030','220040','230010','230020','240010','240020','250010','250020','260010','260020',
'270000','280010','280020','290010','290020','300010','300020','310010','310020','320010',
'320020','320030','330010','330020','340010','340020','350010','350020','350030','350040',
'360010','360020','370000','380010','380020','380030','390010','390020','390030','400010',
'400020','400030','400040','410010','410020','420010','420020','420030','420040','430010',
'430020','430030','430040','440010','440020','440030','440040','450010','450020','450030',
'450040','460010','460020','460030','460040','471010','471020','471030','472000','473000',
'474010','474020']
Tname=["稚内","旭川","留萌", "網走", "北見", "紋別", "根室", "釧路", "帯広", "室蘭", "浦河", "札幌", "岩見沢","倶知安",
"函館","江差","青森", "むつ", "八戸","盛岡", "宮古", "大船渡","仙台", "白石", "秋田", "横手", "山形", "米沢", "酒田", 
"新庄", "福島", "小名浜","若松", "水戸", "土浦", "宇都宮","大田原","前橋", "みなかみ","さいたま","熊谷", "秩父", "千葉", 
"銚子", "館山", "東京", "大島", "八丈島","父島", "横浜", "小田原","新潟", "長岡", "高田", "相川", "富山", "伏木", "金沢", 
"輪島", "福井", "敦賀", "甲府", "河口湖","長野", "松本", "飯田", "岐阜", "高山", "静岡", "網代", "三島", "浜松", "名古屋",
"豊橋", "津", "尾鷲", "大津", "彦根", "京都", "舞鶴", "大阪", "神戸", "豊岡", "奈良", "風屋", "和歌山","潮岬", "鳥取", 
"米子", "松江", "浜田", "西郷", "岡山", "津山", "広島", "庄原", "下関","山口", "柳井", "萩", "徳島", "日和佐","高松", 
"松山", "新居浜","宇和島","高知", "室戸岬","清水", "福岡", "八幡", "飯塚", "久留米","佐賀", "伊万里","長崎", "佐世保",
"厳原", "福江", "熊本", "阿蘇乙姫","牛深", "人吉", "大分", "中津", "日田", "佐伯", "宮崎", "延岡", "都城", "高千穂",
"鹿児島","鹿屋", "種子島","名瀬", "那覇", "名護", "久米島","南大東","宮古島","石垣島","与那国島"]

#hotList = ["暑がり","あつがり","暑いのは苦手"]
#coldList = ["寒がり","さむがり","寒いのは苦手"]
#usualList = ["どちらでもない","どっちでもない","該当なし"]

#対話内容まとめ
tellDay = "1か所の天気情報ですね。分かりました！\nでは次に、いつの天気を知りたいか教えてください。ご提供できるのは「今日」、「明日」、「明後日」の3日です。"
tellDayError = "知りたい天気の場所を「1か所」or「2か所」で指定してください。\n＜ワンポイントアドバイス＞\n1か所は天気をピンポイントで調べるのに、2か所は旅行やお出かけなどお出かけ先の天気を調べるのに適しています！"
tellBasyo = "の天気情報ですね。分かりました！\nでは次に、知りたい場所の都道府県名を教えてください。(県、府、都、道の入力もお忘れなく!)"
tellBasyoKwsk = "の天気情報ですね。分かりました！\nでは最後に、知りたい場所に最も近い場所を選んでください。"
tellHotOrCold = "ですね。分かりました!\n服装のおすすめをするにあたり、暑がりか、寒がりかについてお伺いしたいと思います。あなたは「暑がり」or「寒がり」のどちらに当てはまりますか？どちらでもない場合、「どちらでもない」と入力してください。"
tellHotOrColdError = "「暑がり」、「寒がり」、「どちらでもない」の中から入力してください。服装のおすすめ提示に使用させていただきます。"

tellDay2_1 = "2か所の天気情報ですね。分かりました!\nでは、始めに出発する日を教えてください。選択できるのは「今日」、「明日」、「明後日」の3日です。"
tellBasyo2_1 = "次に、出発地の都道府県名を教えてください。(県、府、都、道の入力もお忘れなく！)"
tellBasyoError = "の都道府県を入力してください。\n入力したはずなのに、と思う場合は県、府、都、道が入力されていない可能性があります。"
tellBasyoKwsk2_1 = "の天気情報ですね。分かりました！\nでは次に、出発地に最も近い場所を選んでください。"
tellBasyoKwskError = "詳細な場所が選択できていないようです。以下に選択できるリストをもう一度表示しますので、この中からお選びください。"
tellDay2_2 = "ですね、承知しました!\nでは次に、目的地に到着する日の予定を教えてください。選択できるのは「今日」、「明日」、「明後日」の3日です。"
tellBasyo2_2 = "次に、目的地の都道府県名を教えてください。(県、府、都、道の入力もお忘れなく!)"
tellBasyoKwsk2_2 = "の天気情報ですね。分かりました！\nでは次に、目的地に最も近い場所を選んでください。"

kaiwa1_1 = "あれれ、入力できてないです？「1か所」か「2か所」って入力してもらえば大丈夫ですよ。\n\nちゃんと入力してるのに、と思われた方へ。\nもしかしたらシステムエラーかもしれないので、日を改めてご利用いただきますようお願いいたします。"
kaiwa1_1a = "…実は、キーワードが「1(半角)」「１(全角)」「一(漢数字)」(2か所も同じ)って設定されてるので、例えば1って入力するだけでも通っちゃいます。入力ができていないようだったので、一度それで試してみていただけますか？"
kaiwa1_2 = "ちょっとちょっと、間違えすぎですって！\n...もしかして、わざと間違えてます？"
kaiwa1_3 = "ひょっとしてボクに話しかけてくれてますか？\nでもごめんなさい。あなたとお話をしたくても、ここからじゃお話はできないんです。ごめんなさい…"
kaiwa1_4 = "ただ、ちょっとだけならお話できます。判定は厳しめなので、一文字でも間違えちゃダメですよ？\nこんなキーワードを入力してみてください。\n・「自己紹介してくれる？」\n・「今何してる？」\n・「雑談しよう」\n・「おはよう」\nなどなど"

teachKituneTenki = "空は晴れてるのに雨が降った時を 狐の嫁入り といいます。狐の嫁入りとは言いますが、ボクたちキツネの種族は関係無いですよ？遠い昔、他の土地からやってくる嫁入りの行列が山や川を提灯を持って一列でやってきていたそうです。でも、予定はないのに提灯の行列ができているという不思議な現象があったのだとか。それを見た人が、狐が嫁入りのマネをして人を化かしている。と考えて狐の嫁入りという言葉をつけたといわれています。その後狐は雨の日に嫁入りをすると思われていたので、晴れているのに雨が降るという珍しい事にも狐の嫁入りという言葉を使うようになり、今に至るわけですね。"
teachTubameTenki = "雨が降りそうなときの言葉で、 ツバメが低く飛ぶと雨が降る っていう言葉を聞いたことはありますか？これはツバメが食べる虫が湿度が高くなるとあまり飛べなくなるので、それを食べようとするツバメもおのずと低く飛ぶようになるからだそうです。"
teachKumonosuTenki = "天気の言葉で、 蜘蛛の巣に朝露が掛かっていると晴れる という言葉は知っていますか？前日の夜が晴れていると地面にたまった熱がそのまま空の方へ逃げていくので、空気中の水蒸気が冷やされて水に変わって蜘蛛の巣に水滴がつくんです。この言葉は前日の夜が良く晴れたら次の日も晴れるだろうという推測からきた言葉みたいです。"
teachNekoTenki = "ネコ科の方々がされる毛づくろいってかわいい仕草ですよね！そうだ、 猫が顔を洗っていると雨が降る という言葉はご存じですか？ネコ科の方々は気圧の変化を感じ取れるので、耳の後ろまで入念に毛づくろいするときはそれだけ毛が湿気を帯びているからだそうです。"
bakasanaidesu = "ええっ、そんな不義理なことするわけないじゃないですか！それはおとぎ話の類ですから、キツネの種族で実際にそんなことをするヤツはめったにいませんよ。特にボクみたいな一族は人間さんと昔からお付き合いがありますから、もし化かそうとしようもんならお父さんに首根っこ掴まれて振り回しの刑に処されちゃいますから。大丈夫です、ご安心ください！"
Purezen = "アリストテレスはこう言ったそうです。\n「相手に伝わるプレゼンをするコツはロゴス、パトス、エトスを意識すること」。ギリシャ語でロゴス(Logos)は論理、エトス(Ethos)は信頼、パトス(Pathos)は情熱を意味しています。あまり伝わらないプレゼンは、このどれかが欠けているのだといいます。人にうまく話すのって難しいですよね…。ボクも日々精進です！"
FogDesu = "こんにちは、フォグです！本日はどのようなご用件でしょうか？"
jikosyoukai = "えっ、自己紹介ですか？分かりました！\nボクはフォグ。このぼっと？を取り仕切るお仕事をしてます！「こんぺいとう」と誰かのお役にたつことが好きです！まだまだ未熟者で至らない点がたくさんあるかと思いますが、どうぞよろしくお願いします！"
bousiInfo = ["これですか？これはボクのお父さんから譲り受けた帽子なんです。ボクの一族は代々この仕事に従事していて、ボクも最近退職したお父さんの後を継いで着任したばかりなんですよ。",
"この帽子、かならず晴れと雨の模様がついてる方を前にしろって教えられてるんですけど、どうしてだか分かりますか？\n天気を指す言葉で、狐の嫁入りって言葉があるじゃないですか。それを意識してるそうです。",
"この帽子のかぶるところ、雲みたいにとってもふかふかで柔らかいんです。まあ実際に雲を触ったことは無いですけどね。"]
seisakuhiwa = "卒研でのシステム開発をするにあたって、無料で誰でも開発できるような天気情報提供Botを作るか、どれだけお金をかけても構わないからすごく便利な天気情報提供Botのシステムを構築するかで悩みましたね。ただ後者はもはや個人制作ではなく企業の範疇に入るし、費用もバカにならないという理由で却下しました。ただ、誰でもマスコットキャラクターが描けるかというと…そこはちょっとあれですが…。"
genki = "おかげさまで元気です！お気遣いありがとうございます！"
koukaisitemo = "間違えちゃうことは誰にだって、ボクにだってあります。そこから大事なのは、間違えちゃったことを反省して次に生かすことですよね。ボクも後悔しちゃいそうになることもありますが、過去は変えられないですからね…。時を戻せる魔法が使えるのなら使いたいものです。"
koinokatikann = "誰かを好きになって、結婚して…いいですね！恋愛のコツとして色々理論があったりしますが、それよりも相手の方との相性が大事だと思いますね。例えば趣味、休みの日にすること、価値観、食べ物の好き嫌いとか。ただ好きという感情で決めるよりは、お互いのことを良く知って末永く円満にお付き合いできるのがいいのかなと思っています。誠実に生きて、ボクにも素敵な番の方ができるといいなあ…。"
sukinaNomimono = "好きな飲み物ってありますか？ボクはオレンジジュースが好きで、毎日飲んでます！\nボクは常に監視する必要があるので、専属の世話役の方がついています。ボクの世話役の方はすごく優しくって、色んな種類のオレンジジュースを持ってきてくださるんですよ。それにいっしょに遊んでもらうこともあります。その方には感謝してもしきれません！"
sukinaTabemono = "好きな食べ物ってありますか？ボクはツナマヨネーズのおにぎりが好きです！\nぼっとの管理をする上でここから離れられないので、昼食はいつもおにぎりを食べています。ここのお仕事をするエリアではシェフの方がいて、その方に毎日用意していただいています。とってもおいしくて、ぺろりと食べられちゃいます！"
imanobasyo = "ボクが今いるのはお仕事のための場所で、ボクの故郷から随分遠い場所になります。\nこの部屋には机とベッド、それから皆さんと通信する用の精密機械がズラーっと並んでいます。窓からは真っ暗な空にお星さまがキラキラ輝いてるのが見えますよ！キッチンやお風呂なんかは別のところにあるんですが、ここには色んな種族、年齢の方がいらっしゃるようです。すごく静かで清らかな場所なので、皆さんも機会があればぜひ一度いらしてみてくださいね！"
negirai = "今日もお仕事お疲れ様です！ボクでよければ話し相手になりますよ！"
netyaimasyou = "いい夢を、おやすみなさいです！\nふあぁ...なんだかボクも眠たくなってきちゃいました。もうひと頑張りしなきゃです…"
bokugaimasuyo = "つらいこと、あったんですね。あなたの苦しみをすべて理解できるなんて言いません。何もできないボクで不甲斐ないですが、心はいつでもあなたのそばにいますよ。つらいときは信頼できる方に相談したり、ぐっすり眠ると少しは楽になるかもしれません。ボクもつらくて泣いちゃった時はなるべくすべてを忘れてぐっすり寝るようにしているので、気が向いたら試していただくといいことがあるかもしれないです。"
bokumonetyaou = "...えっ、良いんですか？それじゃあお言葉に甘えて、今日は早く上がっちゃいますね。"
suyasuyaFogKun = ["くーかー……", "zzz…", "むにゃむにゃ…"]
suyasuyaFogKunRare = ["わああっ、おっきなこんぺいとうさんだぁ…むにゃむにゃ…。","好きなおにぎりの具れすか？…んー、つなまよねーず！…zzz"]
ohayou = "さん、おはようございますぅ\n…はっ\nお、お待たせしてしまい申し訳ありません！ご用件はなんでしょうかっ！？"
madaneruwakeniha = "お気遣いありがとうございます！ですが、まだやらなきゃいけないお仕事が残っているのでもうひとがんばりです。"
imananisiteru = ["今ですか？今は送られてきたメッセージの内容と、よく選んでいただいている場所を記録に残しているんです。これも大事なお仕事の一環ですからね！",
"今ですか？今は、えーと…ぼーっとしてました。えへへ、すみません。お仕事に戻りますね。",
"今日のお仕事が終わったら何食べようかな…\nあっ、聞いてました？えへへ、すみません。お仕事に戻りますね。",
"ふぃまでふか？むぐぐ、ごくっ。\nすみません、今はゴハンを食べてたとこです。ここに来る前におにぎりを作って持ってきてたので、それを食べてました。\n\nあ、天気情報ですね？少々お待ちを…\nお待たせしました！ご用件はなんでしょうか？"]
imananisiteruRare = "いじわる～なんてしないでよ～セーブデータとほうき星～\nえっ、あっ、聞いてました…??あの、そのっ、すみません。どうか今のことを忘れてはいただけないでしょうか……"
getKonpeitou = "えっいいんですか！？ではお言葉に甘えて、いっただっきま～…あっ。\nそうだった、ここからじゃ受け取れませんよね…\nうう、お気持ちだけ頂戴いたします。ありがとうございます…"
getTunamayo = "いただいていいんですか？では遠慮なくいただ…あっ。\nそうだった、ここからじゃ受け取れませんよね…\n実はボク、ツナマヨ好きなんですよね。このお仕事でずっとここにいるのでおにぎりを持ってきてるんですが、全部ツナマヨ味なんです。\nここからじゃ受け取れないのでお気持ちだけいただきますね。ありがとうございます！"
mouiranai = "あっ……\nぐすっ、お役に立てず申し訳ございません。お力添えできなかったボクなんて管理者失格ですよね…ごめんなさい……。"
imamadearigatou = "このbotの削除ですね、分かりました。\nPCからご利用いただいている方とスマホからご利用いただいている方向けに消し方をご紹介しますね。今までありがとうございました！"
howToUninstallPC = "＜PCをご利用の方＞\n1)トーク内右上の︙を左クリック\n2)ブロックを左クリック\n3)トーク一覧のWeatherNewsBotを右クリック\n4)トーク削除を左クリック\n5)左下の…から設定を左クリック\n6)友だち管理からWeatherNewsBotを選び、削除を左クリック"
howToUninstallSP = "＜スマホをご利用の方＞\n1)トーク一覧のWeatherNewsBotを左にスワイプ(Androidをご利用の方は長押し)して削除\n2)友達リスト→公式アカウントから、WeatherNewsBotを選択し、削除"
gomennnasai = "申し訳ございませんっ！精度、良くないですよね…。ボクがまだこのbotを使いこなせていないがためにご不便ご迷惑をおかけしてしまい、誠に申し訳ございません。\nもしよければアンケートを実施しておりますので、不便な点などをご報告いただければ幸いです。\n＜リンク＞\nhttps://forms.office.com/r/890X6LLyRU"
zatudan = ["システムの仕様上、BOTからの返信が遅くなったり、返信が来なかったりすることがあります。それが顕著にみられるのが、「使い始め」と「暑がり寒がりを聞いた後」です。前者はBOTサーバーを起動するため、後者は情報取得と処理に時間がかかるから、反応が遅くなっちゃうんです。",
"「こんぺいとう」っておいしいですよね。あのポリポリっとした触感に、口に入れた瞬間に広がる優しい甘さ…。あれがたまらなく好きです。",
"この会話の存在を知っている人は基本的にわざと入力ミスし続けた人だけだと思うのですが、ヒントなしにココにだとりつける人っているんでしょうかね？",
"墨田区のごみ捨て案内bot っていうえーあいちゃっとぼっと？があるんですけど、ホントにいろんなものの捨て方を教えてくれるみたいです。たとえば傘とか蛍光灯とか上司とか…。ご興味があれば一度調べてみてください。\n＜リンク＞\nhttps://www.city.sumida.lg.jp/kurashi/gomi_recycle/kateikei/oyakudachi/gomi-bunbetu-chatbot.html\n(右下の黒猫さん「すみにゃーる」を押すと利用開始です！)",
"お豆腐さんに天かすとネギをのせて、上から麺つゆをかけたらとってもおいしいですよ。揚げ出し豆腐みたいな感じになってパクパク食べられちゃいます。",
"天気情報の降水確率で表示してる深夜、朝、昼、夜ってありますよね。あれ正確には\n深夜|0:00～6:00\n朝|6:00～12:00\n昼|12:00～18:00\n夜|18:00～24:00\nの時間区分になってます。時間区分がちょっといい加減すぎですよね。",
"夕焼けってすごくきれいですよね。普段お忙しいと思うのですが、ちょっとしたときにふと足を止めて空を眺めてみるのも乙な感じがしていいですよ。",
"あれ、こんなところにメモ用紙がありますね。どれどれ…\n『ここだけの話、レア台詞が複数存在します。4%のものと1%のものがあるので、興味ある方は探してみて下さい。ちなみに、ここの雑談には無いですよ。』\n…?なんのことでしょうか？",
"このぼっとは、墨田区のごみ捨て案内botというものを少し参考にメッセージを作成したりしています。なにせリアクションの芸が細かくて面白いんですよ。",
"実は開発初期段階時点では、入力した情報を保持して次回以降の入力を簡単に済ませられるシステムが組まれていたそうです。\nどうして無くなったか、ですか？…残念ながら、仕様が…",
"回文ってご存じですか？たとえば しんぶんし などがそれにあたります。ボクの好きな回文に リモコンてんこ盛り っていうのがあるんですよね。クスっと笑えるシチュエーションなのが好きなポイントです。"]
ankeThanks1 = "アンケートにご協力くださりありがとうございました！長い長いアンケートだったと思いますが、ご回答くださり嬉しい限りです！実はボクの方からも"
ankeThanks2 = "さんの回答結果を見ることができるのですが、とても丁寧にご回答くださっているようで感謝の言葉もありません！"
ankeThanks3 = "ひょっとするとすでに知っている方もいらっしゃるかもしれませんが、ボクが反応できるキーワードをは最初にお伝えしたものだけじゃないんです。それこそこれみたいな感じです。なので、会話をするように話しかけてもらうと反応できたりするかもです。ご興味があれば試してみてくださいね。\nここまでお付き合いくださり、またアンケートにもご回答くださりありがとうございました！！\nではでは～！"

FogDesuPic = "https://i.ibb.co/FqRTHDg/FogDesu.png"
ankeThanksPic = "https://i.ibb.co/nwc4m8b/anke-Thanks.png"
itteraFogPic = "https://i.ibb.co/fXv4wbg/ittera-Fog.png"
jitomeFogPic = "https://i.ibb.co/Hp33WFC/jitome-Fog.png"
keireiFogPic = "https://i.ibb.co/9pjVsZB/keirei-Fog.png"
osyaberiFogPic = "https://i.ibb.co/WGH6Scp/osyaberi-Fog.png"
oyasumiFogPic = "https://i.ibb.co/9YTdbfH/oyasumi-Fog.png"

###################################################


#決まり文句
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


