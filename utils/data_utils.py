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
            rate = m['hero_damage']/(m['gold_per_min']*m['duration']/60)
            if rate<0.5:
                r['achievements'].append(f"输出经济比{round(rate,2)}，野区采灵芝。")
            elif rate>2:
                r['achievements'].append(f"输出经济比{round(rate,2)}，责任神！")
            if m['kills']>=15 :
                r['achievements'].append(f"{m['kills']}杀,哇 搞这么厉害呀！")
            elif m['kills']>=20 :
                r['achievements'].append(f"{m['kills']}杀,无敌了呀！")
            elif m['kills']>=25 :
                r['achievements'].append(f"{m['kills']}杀, 您就是yatoro god？")
            if m['tower_damage']>10000:
                r['achievements'].append(f"塔伤{m['tower_damage']}，拆迁办来咯！")
            if r['achievements']:
                self.report['matches'].append(r)
    

def qingsuan():
    players = [
        Player(134788522),
        Player(167008289),#fg
        Player(243467357),#loge
        Player(162973981),#tiannuwang
        Player(131849486),#kanwang
        Player(132370368),#dachui
        Player(175159852),#lanmaowang
        Player(136605760),#xinshou
        Player(173362823),#jinxiangjiao
        Player(273755420),#afun
        Player(325332696),#end
        Player(140386448),#lizong
    ]

    report = {"date":datetime.now().strftime('%Y-%m-%d'),"detail":[]}
    for p in players:
        report['detail'].append(p.report)

    with open('data/report.json','w') as f:
        json.dump(report,f,ensure_ascii=False,indent=2)

if __name__ == '__main__':
    qingsuan()