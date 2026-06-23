/**
 * 2026世界杯数据生成脚本
 * 由 WorkBuddy 调用 MCP 工具获取数据后，将此脚本产生的 JSON 写入 data/worldcup-live.json
 * 网页前端通过 fetch 此 JSON 文件实现动态数据展示
 *
 * 使用方法：
 *   node generate-data.js <standings.json> <bracket.json> <matches.json>
 */

const fs = require('fs');
const path = require('path');

// 从命令行参数读取三个JSON文件
const args = process.argv.slice(2);
if (args.length < 3) {
  console.error('用法: node generate-data.js <standings.json> <bracket.json> <matches.json>');
  process.exit(1);
}

const [standingsFile, bracketFile, matchesFile] = args;

let standings, bracket, matches;
try {
  standings = JSON.parse(fs.readFileSync(standingsFile, 'utf8'));
  bracket = JSON.parse(fs.readFileSync(bracketFile, 'utf8'));
  matches = JSON.parse(fs.readFileSync(matchesFile, 'utf8'));
} catch (e) {
  console.error('读取JSON文件失败:', e.message);
  process.exit(1);
}

// 处理积分榜数据
const groups = {};
for (const [groupName, teams] of Object.entries(standings.groups)) {
  groups[groupName] = teams.map(t => ({
    team: t.team,
    played: t.played,
    won: t.won,
    drawn: t.drawn,
    lost: t.lost,
    gf: t.goalsFor,
    ga: t.goalsAgainst,
    gd: t.goalDifference,
    pts: t.points,
    advanced: t.advanced,
    position: t.position,
  }));
}

// 处理所有比赛数据
const allMatches = matches.data || matches; // 兼容两种格式
const playedMatches = allMatches.filter(m => m.homeScore !== null && m.homeScore !== undefined);
const upcomingMatches = allMatches.filter(m => m.homeScore === null || m.homeScore === undefined);

// 按日期分组即将进行的比赛
const upcomingByDate = {};
for (const m of upcomingMatches) {
  const date = m.date;
  if (!upcomingByDate[date]) upcomingByDate[date] = [];
  upcomingByDate[date].push({
    date: m.date,
    stage: m.stage,
    home: m.homeTeam,
    away: m.awayTeam,
    homeScore: m.homeScore,
    awayScore: m.awayScore,
    city: m.city,
    stadium: m.stadium || '',
    kickoff: m.kickoff || m.kickoffUtc || '',
  });
}

// 已完赛按日期分组
const playedByDate = {};
for (const m of playedMatches) {
  const date = m.date;
  if (!playedByDate[date]) playedByDate[date] = [];
  playedByDate[date].push({
    date: m.date,
    stage: m.stage,
    home: m.homeTeam,
    away: m.awayTeam,
    homeScore: m.homeScore,
    awayScore: m.awayScore,
    city: m.city,
    stadium: m.stadium || '',
  });
}

// 处理淘汰赛对阵
const bracketData = { round_of_32: [], round_of_16: [], quarter_final: [], semi_final: [], third_place: [], final: [] };
for (const [stage, games] of Object.entries(bracket.stages)) {
  const key = stage;
  bracketData[key] = games.map(g => ({
    matchNo: g.matchNo,
    stage: g.stage,
    home: g.home,
    away: g.away,
    homeScore: g.homeScore,
    awayScore: g.awayScore,
    city: g.city,
    stadium: g.stadium,
    kickoff: g.kickoffUtc,
    winner: g.winner,
    homeRef: g.homeRef,
    awayRef: g.awayRef,
  }));
}

// 组装最终数据
const output = {
  generatedAt: new Date().toISOString(),
  year: 2026,
  totalMatches: allMatches.length,
  playedCount: playedMatches.length,
  upcomingCount: upcomingMatches.length,
  groups,
  playedByDate,
  upcomingByDate,
  bracket: bracketData,
  // 今日比赛
  today: playedByDate['2026-06-20'] || [],
  todayUpcoming: upcomingByDate['2026-06-20'] || [],
};

// 写入文件
const outPath = path.join(__dirname, 'data', 'worldcup-live.json');
fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, JSON.stringify(output, null, 2), 'utf8');
console.log(`✅ 数据已写入: ${outPath}`);
console.log(`   已完赛: ${playedMatches.length} 场`);
console.log(`   待比赛: ${upcomingMatches.length} 场`);
