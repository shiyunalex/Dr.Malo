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

class malo:
    def __init__(self):
        self.test = 0
        self.status = {
            "weekend": 0,
            "worktime": 0,
        }

    def send(self, msg):
        if args.e=='online':
            itchat.send(msg, toUserName="filehelper")
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
                self.send(f"现在是 {datetime.now().strftime('%H:%M')},Dr.Malo 提醒您按时提肛~".format(datetime.now()))
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


    async def main(self):
        await asyncio.gather(
            self.update_status(),
            self.task_1(),
            self.task_2(),
            self.task_3(),
        )

    

if __name__ == '__main__':
    try:
        m = malo()
        asyncio.run(m.main())
    except Exception as e:
        if args.e=='online':
            itchat.logout()