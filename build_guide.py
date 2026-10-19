"""從單一原始資料產生精華版 Markdown 與可離線搜尋的單頁網站。"""
from __future__ import annotations

import json
from pathlib import Path

from guide_data import DATE, E, S


ROOT = Path(__file__).resolve().parent
items = []
for row in E:
    category, conclusion, audience, cost, revenue, evidence, steps, risk, keys, reverse = row
    items.append({
        "id": len(items) + 1,
        "category": category,
        "conclusion": conclusion,
        "audience": audience,
        "cost": cost,
        "revenue": revenue,
        "evidence": evidence,
        "steps": steps,
        "risk": risk,
        "sources": [{"name": S[key][0], "url": S[key][1]} for key in keys],
        "checked": DATE,
        "reverse": reverse,
    })

lines = [
    "# 台灣 AI 一人公司變現指南：30 條精華版", "",
    "每類 3 條，先做一條有來源、可量測的事。這是 100 條計畫的 30 條精華版；不保證收入。",
    "工具價格、平台規則與法規查證日期：2026-10-18；實施前重新核對。『成本』若寫自有設備或工時，是執行估算，非官方報價；『可衡量結果』是追蹤方法，不是承諾。", "",
    "證據等級：**官方**＝官方功能、價格或政策；**法規**＝現行法規與主管機關說明；**推論**＝根據來源提出的測試做法，商業效果未驗證。來源各自支持條目中的具體主張，不能把平台功能誤當成獲利證據。", "",
]
category = None
for item in items:
    if item["category"] != category:
        category = item["category"]
        lines += [f"## {category}", ""]
    sources = "、".join(f"[{s['name']}]({s['url']})" for s in item["sources"])
    lines += [
        f"### {item['id']:03d}｜{item['conclusion']}", "",
        f"- 一句結論：{item['conclusion']}",
        f"- 適合誰：{item['audience']}",
        f"- 成本（金額與時間）：{item['cost']}",
        f"- 可衡量結果／可能收益：{item['revenue']}",
        f"- 照做步驟：{item['steps']}",
        f"- 證據等級：{item['evidence']}" + ("；反常識" if item["reverse"] else ""),
        f"- 來源連結：{sources}（查證日期：{item['checked']}）",
        f"- 風險與紅線：{item['risk']}", "",
    ]
lines += [
    "---", "",
    "內容採 [CC BY-NC 4.0](LICENSE)；非商用轉載請標示安達與授權。需要陪跑與工具，可看 [官方 LINE](https://s.andax.me/s/fwT5bv) 或 [anda.biz](https://anda.biz)。", "",
]
(ROOT / "指南.md").write_text("\n".join(lines), encoding="utf-8")

payload = json.dumps(items, ensure_ascii=False).replace("<", "\\u003c")
page = '''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>台灣 AI 一人公司變現指南｜30 條精華版</title>
<style>:root{font-family:system-ui,"Microsoft JhengHei",sans-serif;color:#1c2830;background:#f7f5ef}*{box-sizing:border-box}body{margin:0}header{padding:32px 18px;background:#123948;color:#fff}header>div,main,footer{max-width:1000px;margin:auto}h1{font-size:clamp(1.7rem,5vw,3rem);margin:.2em 0}p{line-height:1.7}main{padding:20px 16px}input,select{font:inherit;padding:12px;border:1px solid #9aabae;border-radius:8px;max-width:100%;background:white}input{width:min(100%,450px)}.controls{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}article{background:#fff;border:1px solid #d9e0dc;border-radius:12px;padding:18px;margin:14px 0;box-shadow:0 2px 8px #1239480b}article h2{font-size:1.2rem;margin:0 0 12px}dl{display:grid;grid-template-columns:8.5em 1fr;gap:8px}dt{font-weight:bold;color:#365c67}dd{margin:0;line-height:1.6;overflow-wrap:anywhere}dd a{display:inline-block;margin-right:.55em}a{color:#087181}footer{padding:22px 16px;background:#e6eeec}small{opacity:.9}@media(max-width:560px){dl{grid-template-columns:1fr;gap:2px}dt{margin-top:9px}.controls>*{width:100%}}</style></head><body>
<header><div><small>安達｜2026-10-18 查證｜100 條計畫的 30 條精華版</small><h1>台灣 AI 一人公司變現指南</h1><p>每類 3 條：工具與價格、照做步驟、可衡量結果及原始來源。不保證收入。</p></div></header><main><p>先選一條適合自己的事。價格、平台規則及法規可能變動，動手前請重查來源。「推論」代表官方來源支持背景事實，商業效果仍未驗證。自有設備與工時是規劃估算。</p><div class="controls"><input id="search" type="search" placeholder="搜尋，例如：Batch、課程、稅籍" aria-label="搜尋條目"><select id="category" aria-label="篩選分類"><option value="">所有分類</option></select></div><p id="count" role="status"></p><div id="list"></div></main><footer>需要陪跑與工具：<a href="https://s.andax.me/s/fwT5bv">官方 LINE</a>｜<a href="https://anda.biz">anda.biz</a>。<p>內容採 <a href="https://creativecommons.org/licenses/by-nc/4.0/">CC BY-NC 4.0</a>；非商用轉載請標示安達與授權。</p></footer>
<script id="data" type="application/json">''' + payload + '''</script><script>const data=JSON.parse(document.getElementById('data').textContent);const list=document.getElementById('list'),count=document.getElementById('count'),search=document.getElementById('search'),category=document.getElementById('category');for(const name of [...new Set(data.map(x=>x.category))]){const o=document.createElement('option');o.value=name;o.textContent=name;category.append(o)}function render(){const q=search.value.trim().toLowerCase(),c=category.value;const found=data.filter(x=>(!c||x.category===c)&&(!q||JSON.stringify(x).toLowerCase().includes(q)));count.textContent=`顯示 ${found.length} / ${data.length} 條`;list.replaceChildren();for(const x of found){const article=document.createElement('article');const title=document.createElement('h2');title.textContent=`${String(x.id).padStart(3,'0')}｜${x.conclusion}`;article.append(title);const dl=document.createElement('dl');for(const [label,key] of [['適合誰','audience'],['成本（金額與時間）','cost'],['可衡量結果／可能收益','revenue'],['照做步驟','steps'],['證據等級','evidence'],['來源連結','sources'],['風險與紅線','risk']]){const dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=label;if(key==='sources'){for(const s of x.sources){const a=document.createElement('a');a.href=s.url;a.textContent=s.name;a.rel='noopener noreferrer';a.target='_blank';dd.append(a)}const time=document.createElement('small');time.textContent=`查證日期：${x.checked}`;dd.append(time)}else dd.textContent=x[key]+(key==='evidence'&&x.reverse?'；反常識':'');dl.append(dt,dd)}article.append(dl);list.append(article)}}search.addEventListener('input',render);category.addEventListener('change',render);render();</script></body></html>'''
(ROOT / "site").mkdir(exist_ok=True)
(ROOT / "site" / "index.html").write_text(page, encoding="utf-8")
print(f"已產生 {len(items)} 條精華指南與離線單頁")
