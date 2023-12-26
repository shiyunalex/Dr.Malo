import requests
from datetime import datetime, timedelta
import json

hero_dict = json.load(open('data/hero_names.json','r'))

class Player:
    def __init__(self, id):
        self.id = id
        self.user_info = self.get_user_info()
        self.recent_matches = self.get_recent_matches()
        self.report = {
            'nickname':self.user_info['profile']['personaname'],
            'matches':[]
            }
        self.get_achievements()
    
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
            date_range = [datetime.now()-timedelta(hours=20),datetime.now()]
            url = f"https://api.opendota.com/api/players/{self.id}/recentMatches"
            res = requests.get(url)
            res = res.json()
            res = [i for i in res if _get_date(i)>date_range[0] and _get_date(i)<date_range[1]]
            return res
        except Exception as e:
            print(e)
            return []

    def get_achievements(self):
        for m in self.recent_matches:
            r = {'hero':hero_dict.get(str(m['hero_id']),m['hero_id']),'achievements':[]}
            if m['deaths']>15:
                r['achievements'].append(f"阵亡{m['deaths']}次，求求你别送了")
            if m['duration']>3900 and ((127>=m['player_slot']>=0 and not m['radiant_win']) or (255>=m['player_slot']>=128 and m['radiant_win'])):
                r['achievements'].append(f"鏖战{round(m['duration']/60)}分钟，究极长痛嘻嘻")
            if m['kills']+m['assists']<=3 :
                r['achievements'].append(f"{m['kills']}杀{m['assists']}助攻，别划了呀哥们")
            if r['achievements']:
                self.report['matches'].append(r)
    

def qingsuan():
    players = [
        Player(134788522)
    ]

    report = {"date":datetime.now().strftime('%Y-%m-%d'),"detail":[]}
    for p in players:
        report['detail'].append(p.report)

    with open('data/report.json','w') as f:
        json.dump(report,f,ensure_ascii=False,indent=2)

if __name__ == '__main__':
    qingsuan()