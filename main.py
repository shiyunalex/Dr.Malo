from utils import *
import asyncio
from datetime import datetime
import argparse
import itchat

parser = argparse.ArgumentParser()
parser.add_argument("-e")
args = parser.parse_args()

if args.e=='online':
    itchat.login(enableCmdQR=2)
    room = itchat.get_chatrooms()[0]
    room_id = room.UserName

class malo:
    def __init__(self):
        self.test = 0
        self.status = {
            "weekend": 0,
            "worktime": 0,
        }

    def send(self, msg):
        if args.e=='online':
            itchat.send(msg, toUserName=room_id)
        else:
            print(msg)
    
    async def update_status(self):
        while True:
            if is_weekend():
                self.status["weekend"] = 1
            else:
                self.status["weekend"] = 0
            if is_worktime():
                self.status["worktime"] = 1
            else:
                self.status["worktime"] = 0
            await asyncio.sleep(1)
    
    async def task_1(self):
        while True:
            if not self.status["weekend"]\
                and self.status["worktime"]\
                and get_hour() in [11,15]:
                self.send(f"【温馨提醒】现在是 {datetime.now().strftime('%H:%M')}, 站起来动动，提肛&喝水啦~~ !".format(datetime.now()))
                await asyncio.sleep(3601)
            else:
                await asyncio.sleep(5)
    
    async def task_2(self):
        while True:
            if get_hour() == 9:
                self.send("现在是早上9点,Dr.Malo上班啦~")
                await asyncio.sleep(3601)
            else:
                await asyncio.sleep(5)
    
    async def task_3(self):
        while True:
            if get_hour() == 18:
                self.send("现在是下午6点,Dr.Malo下班啦~")
                await asyncio.sleep(3601)
            else:
                await asyncio.sleep(5)
    
    async def task_4(self):
        while True:
            if get_hour() == 20:
                self.send("【温馨提醒】晚上8点,各位靓仔还不快上线dota~")
                await asyncio.sleep(3601)
            else:
                await asyncio.sleep(5)
    
    async def task_5(self):
        while True:
            if get_hour() == 0:
                self.send("【温馨提醒】各位靓仔晚安~ \nPS:赢一天了没？")
                await asyncio.sleep(3601)
            else:
                await asyncio.sleep(5)
    
    async def task_qingsuan(self):
        while True:
            if get_hour() == 10:
                report = qingsuan()
                self.send("【青蒜！】")
                await asyncio.sleep(3601)
            else:
                await asyncio.sleep(5)
    


    async def main(self):
        await asyncio.gather(
            self.update_status(),
            self.task_1(),
            self.task_2(),
            self.task_3(),
            self.task_4(),
            self.task_5(),
        )
    

    

if __name__ == '__main__':
    try:
        m = malo()
        asyncio.run(m.main())
    except Exception as e:
        if args.e=='online':
            itchat.logout()