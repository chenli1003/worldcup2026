#!/usr/bin/env python3
"""2026 World Cup live data fetcher - runs in GitHub Actions, fetches from Wikipedia API."""

import json, os, re, sys
from datetime import datetime, timedelta, timezone

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests")
    sys.exit(1)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
WIKI_PAGE = '2026_FIFA_World_Cup'
USER_AGENT = 'WorldCup2026/1.0 (bot)'
WIKI_API = 'https://en.wikipedia.org/w/api.php'

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

CITY_CN = {
    'Mexico City': '墨西哥城', 'Guadalajara': '瓜达拉哈拉', 'Monterrey': '蒙特雷',
    'Los Angeles': '洛杉矶', 'San Francisco': '旧金山', 'Seattle': '西雅图',
    'Dallas': '达拉斯', 'Houston': '休斯敦', 'Atlanta': '亚特兰大',
    'Philadelphia': '费城', 'Miami': '迈阿密', 'Boston': '波士顿',
    'New York/New Jersey': '纽约/新泽西', 'Kansas City': '堪萨斯城',
    'Vancouver': '温哥华', 'Toronto': '多伦多',
}

def fetch_wikitext(section=0):
    params = {'action': 'parse', 'page': WIKI_PAGE, 'prop': 'wikitext', 'format': 'json', 'section': section}
    r = requests.get(WIKI_API, params=params, headers={'User-Agent': USER_AGENT}, timeout=30)
    r.raise_for_status()
    return r.json().get('parse', {}).get('wikitext', {}).get('*', '')

def fetch_html():
    url = f'https://en.wikipedia.org/api/rest_v1/page/html/{WIKI_PAGE}'
    r = requests.get(url, headers={'User-Agent': USER_AGENT}, timeout=30)
    r.raise_for_status()
    return r.text

def normalize_team(name):
    name = re.sub(r"'''?", '', name)
    name = re.sub(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', r'\1', name)
    name = re.sub(r'\{\{flagicon\|[^}]+\}\}', '', name)
    name = re.sub(r'\{\{fb\|([^}]+)\}\}', r'\1', name)
    name = re.sub(r'\{\{[^}]+\}\}', '', name)
    name = re.sub(r'<[^>]+>', '', name)
    name = re.sub(r'[\(\[].*?[\)\]]', '', name)
    return name.strip()

def parse_matches_tables(html):
    matches = []
    match_id_counter = 0
    tables = re.findall(r'<table[^>]*>(.*?)</table>', html, re.DOTALL | re.IGNORECASE)
    for table in tables:
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table, re.DOTALL | re.IGNORECASE)
        for row in rows:
            cells = re.findall(r'<(?:td|th)[^>]*>(.*?)</(?:td|th)>', row, re.DOTALL | re.IGNORECASE)
            if not cells:
                continue
            cells_clean = [re.sub(r'<[^>]+>', ' ', c).strip() for c in cells]
            cells_clean = [re.sub(r'\s+', ' ', c).strip() for c in cells_clean]
            cells_clean = [re.sub(r'\[note \d+\]', '', c).strip() for c in cells_clean]
            score_match_found = None
            for ci, cell in enumerate(cells_clean):
                sm = re.match(r'^(\d+)\s*[–—-]\s*(\d+)$', cell)
                if sm:
                    score_match_found = (ci, int(sm.group(1)), int(sm.group(2)))
                    break
            if score_match_found is None:
                for ci, cell in enumerate(cells_clean):
                    sm = re.match(r'^(\d+)\s*–\s*(\d+)\s*(?:\(.*?\))?$', cell)
                    if sm:
                        score_match_found = (ci, int(sm.group(1)), int(sm.group(2)))
                        break
            if score_match_found is None:
                continue
            ci, home_score, away_score = score_match_found
            home_team = cells_clean[ci - 1] if ci > 0 else ''
            away_team = cells_clean[ci + 1] if ci < len(cells_clean) - 1 else ''
            home_team = normalize_team(home_team)
            away_team = normalize_team(away_team)
            if not home_team or not away_team or home_team == away_team:
                continue
            if len(home_team) < 2 or len(away_team) < 2 or len(home_team) > 50 or len(away_team) > 50:
                continue
            match_id_counter += 1
            matches.append({
                'id': f'2026-{match_id_counter:03d}',
                'matchNo': match_id_counter,
                'homeTeam': home_team,
                'awayTeam': away_team,
                'homeScore': home_score,
                'awayScore': away_score,
                'homeRef': home_team,
                'awayRef': away_team,
                'stageNormalized': 'group_a',
                'date': '',
                'kickoffUtc': '',
                'city': '',
                'stadium': '',
            })
    return matches

def parse_standings(wikitext):
    groups = {}
    group_pattern = r"===\s*Group ([A-L])\s*===\s*\n(.*?)(?=\n===|$)"
    for gm in re.finditer(group_pattern, wikitext, re.DOTALL):
        gname = f"Group {gm.group(1)}"
        gtext = gm.group(2)
        table_match = re.search(r'\{\|.*?\n(.*?)\|\}', gtext, re.DOTALL)
        if not table_match:
            continue
        table = table_match.group(1)
        teams = []
        rows = table.split('\n|-\n')
        for row in rows:
            if '!' in row:
                continue
            cells = []
            for cell in re.finditer(r'(?:^\|\s*|\|\|\s*|\n\|\s*)(.*?)(?=\n\||\n!|\n\|-|\Z)', row, re.DOTALL):
                val = re.sub(r"'''?", '', cell.group(1)).strip()
                val = re.sub(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', r'\1', val)
                val = re.sub(r'\{\{flagicon\|[^}]+\}\}', '', val).strip()
                cells.append(val)
            if len(cells) < 3:
                continue
            try:
                pos = int(cells[0]) if cells[0].isdigit() else 0
            except:
                continue
            team = cells[1] if len(cells) > 1 else ''
            if not team or pos == 0:
                continue
            played = int(cells[2]) if len(cells) > 2 and cells[2].isdigit() else 0
            won = int(cells[3]) if len(cells) > 3 and cells[3].isdigit() else 0
            drawn = int(cells[4]) if len(cells) > 4 and cells[4].isdigit() else 0
            lost = int(cells[5]) if len(cells) > 5 and cells[5].isdigit() else 0
            gf = int(cells[6]) if len(cells) > 6 and cells[6].strip('+').lstrip('0') != '' and cells[6].strip('+').replace('-','').isdigit() else 0
            ga = int(cells[7]) if len(cells) > 7 and cells[7].strip('+').lstrip('0') != '' and cells[7].strip('+').replace('-','').isdigit() else 0
            try: pts = int(cells[8]) if len(cells) > 8 else 0
            except: pts = won * 3 + drawn
            teams.append({
                'team': team, 'teamCN': TEAM_CN.get(team, team),
                'position': pos, 'played': played, 'won': won,
                'drawn': drawn, 'lost': lost, 'goalsFor': gf,
                'goalsAgainst': ga, 'goalDifference': gf - ga,
                'points': pts, 'advanced': pos <= 2
            })
        if teams:
            groups[gname] = sorted(teams, key=lambda t: t['position'])
    return groups

def load_fallback():
    for fname in ['matches-raw.json', 'standings.json', 'bracket.json']:
        if not os.path.exists(os.path.join(DATA_DIR, fname)):
            return None, None, None
    with open(os.path.join(DATA_DIR, 'matches-raw.json'), 'r', encoding='utf-8') as f:
        matches = json.load(f)
    with open(os.path.join(DATA_DIR, 'standings.json'), 'r', encoding='utf-8') as f:
        standings = json.load(f)
    with open(os.path.join(DATA_DIR, 'bracket.json'), 'r', encoding='utf-8') as f:
        bracket = json.load(f)
    return matches, standings, bracket

def build_output(matches_list, standings_data, bracket_data):
    played = [m for m in matches_list if m.get('homeScore') is not None]
    upcoming = [m for m in matches_list if m.get('homeScore') is None]
    def gbd(mlist):
        r = {}
        for m in mlist:
            r.setdefault(m.get('date', 'unknown'), []).append(m)
        return r
    groups_out = {}
    for gname, teams in standings_data.items():
        groups_out[gname] = []
        for t in teams:
            tn = t.get('team', '')
            groups_out[gname].append({
                'team': tn, 'teamCN': TEAM_CN.get(tn, tn),
                'position': t.get('position', 0), 'played': t.get('played', 0),
                'won': t.get('won', 0), 'drawn': t.get('drawn', 0),
                'lost': t.get('lost', 0), 'pts': t.get('points', 0),
                'gf': t.get('goalsFor', 0), 'ga': t.get('goalsAgainst', 0),
                'gd': t.get('goalDifference', 0), 'advanced': t.get('advanced', False),
            })
    today_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    team_matches = {}
    for m in matches_list:
        for key in ['homeTeam', 'awayTeam']:
            team = m.get(key, '')
            if team not in team_matches:
                team_matches[team] = []
            team_matches[team].append({
                'id': m.get('id', ''), 'date': m.get('date', ''),
                'stage': m.get('stageNormalized', m.get('stage', '')),
                'home': m.get('homeTeam', ''), 'away': m.get('awayTeam', ''),
                'homeCN': TEAM_CN.get(m.get('homeTeam', ''), m.get('homeTeam', '')),
                'awayCN': TEAM_CN.get(m.get('awayTeam', ''), m.get('awayTeam', '')),
                'homeScore': m.get('homeScore'), 'awayScore': m.get('awayScore'),
                'city': m.get('city', ''), 'stadium': m.get('stadium', ''),
                'kickoffBJ': m.get('kickoffBJ', ''),
            })
    return {
        'generatedAt': datetime.now(timezone.utc).isoformat(),
        'totalMatches': len(matches_list), 'playedCount': len(played),
        'upcomingCount': len(upcoming),
        'todayPlayed': [m for m in played if m.get('date') == today_str],
        'todayUpcoming': [m for m in upcoming if m.get('date') == today_str],
        'playedByDate': gbd(played), 'upcomingByDate': gbd(upcoming),
        'groups': groups_out, 'bracket': bracket_data,
        'teamMatches': team_matches, 'allMatches': matches_list,
    }

def main():
    print("=== 2026 World Cup Data Fetcher ===")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    matches, standings, bracket = None, None, None
    try:
        print("\nFetching from Wikipedia...")
        html = fetch_html()
        print(f"  HTML: {len(html)} bytes")
        wikitext = fetch_wikitext()
        print(f"  Wikitext: {len(wikitext)} bytes")
        parsed = parse_matches_tables(html)
        if parsed:
            matches = parsed
            print(f"  Parsed {len(matches)} matches")
        groups = parse_standings(wikitext)
        if groups:
            standings = {'year': 2026, 'groups': groups}
            print(f"  Parsed {len(groups)} groups")
    except Exception as e:
        print(f"  Wikipedia fetch error: {e}")
    if matches is None:
        print("\nFalling back to local data...")
        matches, standings, bracket = load_fallback()
        if matches:
            print(f"  Loaded {len(matches)} from local files")
        else:
            print("FATAL: No data available")
            sys.exit(1)
    if standings is None:
        standings = {'year': 2026, 'groups': {}}
    if bracket is None:
        bracket = {}
    output = build_output(matches, standings.get('groups', {}), bracket)
    out_path = os.path.join(DATA_DIR, 'worldcup-live.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nDone: {out_path}")
    print(f"  Total: {output['totalMatches']} | Played: {output['playedCount']} | Upcoming: {output['upcomingCount']}")

if __name__ == '__main__':
    main()
