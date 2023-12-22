import requests
from datetime import datetime, timedelta
import json

date_range = [datetime.now()-timedelta(hours=20),datetime.now()]

class Player:
    def __init__(self, id):
        self.id = id
        self.user_info = self.get_user_info()
        self.recent_matches = self.get_recent_matches()
        self.report = {
            'nickname':self.user_info['profile']['personaname'],
            'matches':[]
            }
        self.qingsuan()
    
    def get_user_info(self):
        try:
            url = f"https://api.opendota.com/api/players/{self.id}"
            res = requests.get(url)
            return res.json()
        except Exception as e:
            print(e)
            return {}
    
    def get_recent_matches(self):
        def _get_date(match):
            return datetime.fromtimestamp(match.get('start_time',0))
        
        try:
            url = f"https://api.opendota.com/api/players/{self.id}/recentMatches"
            res = requests.get(url)
            res = res.json()
            res = [i for i in res if _get_date(i)>date_range[0] and _get_date(i)<date_range[1]]
            return res
        except Exception as e:
            print(e)
            return []

    def qingsuan(self):
        for m in self.recent_matches:
            r = {'hero':m['hero_id'],'achievements':[]}
            if m['deaths']>=15:
                r['achievements'].append('【僵】')
            if m['hero_damage']/(m['gold_per_min']*m['duration']/60)<=0.5:
                r['achievements'].append('【瘤】')
            if m['hero_damage']/(m['gold_per_min']*m['duration']/60)>=3:
                r['achievements'].append('【劳】')
            if m['kills']/m['deaths']>=15:
                r['achievements'].append('【天之上】')
            if m['kills']>=25:
                r['achievements'].append('【宰】')
            if m['tower_damage']>11000:
                r['achievements'].append('【拆】')
            if m['kills']+m['assists']<=3 :
                r['achievements'].append('【划】')

            if r['achievements']:
                self.report['matches'].append(r)
    

players = [
    Player(134788522)
]

report = {"date":datetime.now().strftime('%Y-%m-%d'),"detail":[]}
for p in players:
    report['detail'].append(p.report)

with open('data/report.json','w') as f:
    json.dump(report,f,ensure_ascii=False,indent=2)


