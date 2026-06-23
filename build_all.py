import json, os
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
OUT_FILE = os.path.join(DATA_DIR, 'worldcup-live.json')

TEAM_CN = {
    'Algeria': '阿尔及利亚', 'Argentina': '阿根廷', 'Australia': '澳大利亚',
    'Austria': '奥地利', 'Belgium': '比利时', 'Bosnia and Herzegovina': '波黑',
    'Brazil': '巴西', 'Cabo Verde': '佛得角', 'Canada': '加拿大',
    'Colombia': '哥伦比亚', 'Congo DR': '民主刚果', 'Croatia': '克罗地亚',
    'Curaçao': '库拉索', 'Czechia': '捷克', "Côte d'Ivoire": '科特迪瓦',
    'Ecuador': '厄瓜多尔', 'Egypt': '埃及', 'England': '英格兰',
    'France': '法国', 'Germany': '德国', 'Ghana': '加纳', 'Haiti': '海地',
    'IR Iran': '伊朗', 'Iraq': '伊拉克', 'Japan': '日本', 'Jordan': '约旦',
    'Korea Republic': '韩国', 'Mexico': '墨西哥', 'Morocco': '摩洛哥',
    'Netherlands': '荷兰', 'New Zealand': '新西兰', 'Norway': '挪威',
    'Panama': '巴拿马', 'Paraguay': '巴拉圭', 'Portugal': '葡萄牙',
    'Qatar': '卡塔尔', 'Saudi Arabia': '沙特阿拉伯', 'Scotland': '苏格兰',
    'Senegal': '塞内加尔', 'South Africa': '南非', 'Spain': '西班牙',
    'Sweden': '瑞典', 'Switzerland': '瑞士', 'Tunisia': '突尼斯',
    'Türkiye': '土耳其', 'USA': '美国', 'Uruguay': '乌拉圭',
    'Uzbekistan': '乌兹别克斯坦'
}

def cn(en): return TEAM_CN.get(en, en)

# City & Stadium Chinese names
CITY_CN = {
    'Mexico City': '墨西哥城', 'Guadalajara': '瓜达拉哈拉', 'Monterrey': '蒙特雷',
    'Los Angeles': '洛杉矶', 'San Francisco': '旧金山', 'Seattle': '西雅图',
    'Dallas': '达拉斯', 'Houston': '休斯敦', 'Atlanta': '亚特兰大',
    'Philadelphia': '费城', 'Miami': '迈阿密', 'Boston': '波士顿',
    'New York/New Jersey': '纽约/新泽西', 'Kansas City': '堪萨斯城',
    'Vancouver': '温哥华', 'Toronto': '多伦多',
}
STADIUM_CN = {
    'Estadio Azteca': '阿兹特克体育场', 'Estadio Akron': '阿克伦体育场',
    'Estadio BBVA': 'BBVA 体育场', 'SoFi Stadium': 'SoFi 体育场',
    'Levi\'s Stadium': '李维斯体育場', 'Lumen Field': '流明球场',
    'AT&T Stadium': 'AT&T 体育场', 'NRG Stadium': 'NRG 体育场',
    'Mercedes-Benz Stadium': '梅赛德斯-奔驰竞技场', 'Lincoln Financial Field': '林肯金融球场',
    'Hard Rock Stadium': '硬石球场', 'Gillette Stadium': '吉列体育场',
    'MetLife Stadium': '大都会人寿球场', 'Arrowhead Stadium': '箭头体育场',
    'BC Place': 'BC广场', 'BMO Field': 'BMO 球场',
}

with open(os.path.join(DATA_DIR, 'matches-raw.json'), 'r', encoding='utf-8') as f:
    all_matches = json.load(f)
with open(os.path.join(DATA_DIR, 'standings.json'), 'r', encoding='utf-8') as f:
    standings_data = json.load(f)
with open(os.path.join(DATA_DIR, 'bracket.json'), 'r', encoding='utf-8') as f:
    bracket_data = json.load(f)

def calc_beijing(kickoff_utc):
    if not kickoff_utc or len(kickoff_utc) < 16: return ''
    try:
        dt = datetime.fromisoformat(kickoff_utc.replace('Z', '+00:00'))
        dt_bj = dt + timedelta(hours=8)
        return dt_bj.strftime('%m月%d日 %H:%M')
    except: return ''

def simplify_match(m):
    mid = m.get('id') or m.get('matchNo') or str(m.get('date','')) + str(m.get('homeTeam','')) + str(m.get('awayTeam',''))
    home = m.get('homeTeam', '')
    away = m.get('awayTeam', '')
    return {
        'id': mid,
        'date': m.get('date', ''),
        'stage': m.get('stageNormalized', m.get('stage', '')),
        'home': home, 'away': away,
        'homeCN': cn(home), 'awayCN': cn(away),
        'homeScore': m.get('homeScore'), 'awayScore': m.get('awayScore'),
        'city': CITY_CN.get(m.get('city', ''), m.get('city', '')),
        'stadium': STADIUM_CN.get(m.get('stadium', ''), m.get('stadium', '')),
        'kickoffBJ': calc_beijing(m.get('kickoffUtc', '')),
        'status': m.get('status', ''),
    }

played = [simplify_match(m) for m in all_matches if m.get('homeScore') is not None]
upcoming = [simplify_match(m) for m in all_matches if m.get('homeScore') is None]

def group_by_date(matches):
    result = {}
    for m in matches:
        d = m['date']
        if d not in result: result[d] = []
        result[d].append(m)
    return result

# Build groups — use CORRECT field names from standings source
groups = {}
for group_name, teams in standings_data.get('groups', {}).items():
    groups[group_name] = []
    for t in teams:
        team_en = t.get('team', '')
        gf = t.get('goalsFor', 0)
        ga = t.get('goalsAgainst', 0)
        groups[group_name].append({
            'team': team_en, 'teamCN': cn(team_en),
            'position': t.get('position', 0),
            'played': t.get('played', 0),
            'won': t.get('won', 0), 'drawn': t.get('drawn', 0), 'lost': t.get('lost', 0),
            'pts': t.get('points', 0),
            'gf': gf, 'ga': ga,
            'gd': gf - ga,
            'advanced': t.get('advanced', False),
        })

# Build bracket with Chinese names + Beijing time + Chinese venue
bracket_out = {}
for stage, games in bracket_data.get('stages', {}).items():
    bracket_out[stage] = []
    for g in games:
        bracket_out[stage].append({
            'matchNo': g.get('matchNo', ''),
            'date': g.get('date', ''),
            'home': g.get('home', ''),
            'away': g.get('away', ''),
            'homeCN': cn(g.get('home', '')),
            'awayCN': cn(g.get('away', '')),
            'homeScore': g.get('homeScore'),
            'awayScore': g.get('awayScore'),
            'city': CITY_CN.get(g.get('city', ''), g.get('city', '')),
            'stadium': STADIUM_CN.get(g.get('stadium', ''), g.get('stadium', '')),
            'kickoffBJ': calc_beijing(g.get('kickoffUtc', '')),
            'winner': g.get('winner', ''),
        })

# Team match history
team_matches = {}
all_simple = played + upcoming
for m in all_simple:
    for team in [m['home'], m['away']]:
        if team not in team_matches: team_matches[team] = []
        if not any(x.get('id') == m['id'] for x in team_matches[team]):
            team_matches[team].append({
                'id': m.get('id'), 'date': m['date'], 'stage': m['stage'],
                'home': m['home'], 'away': m['away'],
                'homeCN': m['homeCN'], 'awayCN': m['awayCN'],
                'homeScore': m.get('homeScore'), 'awayScore': m.get('awayScore'),
                'city': m['city'], 'stadium': m['stadium'],
                'kickoffBJ': m.get('kickoffBJ', ''),
            })

for team in team_matches:
    team_matches[team].sort(key=lambda x: x['date'])

today_str = datetime.now().strftime('%Y-%m-%d')
output = {
    'generatedAt': datetime.now().isoformat(),
    'totalMatches': len(all_matches), 'playedCount': len(played), 'upcomingCount': len(upcoming),
    'todayPlayed': [m for m in played if m['date'] == today_str],
    'todayUpcoming': [m for m in upcoming if m['date'] == today_str],
    'playedByDate': group_by_date(played), 'upcomingByDate': group_by_date(upcoming),
    'groups': groups, 'bracket': bracket_out,
    'teamMatches': team_matches, 'allMatches': all_simple,
}

with open(OUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print('Data built successfully!')
print(f'  Total: {output["totalMatches"]} Played: {output["playedCount"]} Upcoming: {output["upcomingCount"]}')
