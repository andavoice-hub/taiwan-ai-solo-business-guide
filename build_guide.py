"""從單一原始資料產生精華版 Markdown 與可離線搜尋的單頁網站。"""
from __future__ import annotations

import json
from pathlib import Path

from guide_data import DATE, E, S


ROOT = Path(__file__).resolve().parent
SECTION = {
    "AI 工具怎麼選與花費": ("先控制工具費用，再看工作能不能省時間。", "找一筆最近的工具帳單，寫下每件工作的費用。"),
    "短影音與漫劇": ("影片有人看，還要看內容是否原創、符合平台規則。", "挑一支影片，核對素材授權與上傳標示。"),
    "賣課與直播成交": ("先教會觀眾一件事，再記錄有多少人真正詢問。", "寫下你能用一支短片教會觀眾的事。"),
    "電商與帶貨": ("商品照和說明要真實，也要確認你有權使用。", "挑一張商品照，查清來源和使用授權。"),
    "自動化與代理": ("讓流程幫你做事，也要防止漏單和重複執行。", "找一筆訂單，確認流程紀錄能追到結果。"),
    "接案與代營運": ("開工前寫清交付內容、權利和資料使用範圍。", "拿一份報價單，補上要交付的檔案清單。"),
    "原始碼公開引流": ("公開作品能讓人認識你，授權和詢問數都要看。", "打開一個公開作品，檢查授權說明。"),
    "台灣法規紅線": ("賣東西和收資料前，先把重要條件說清楚。", "用手機看一次你的結帳頁或表單。"),
    "常見詐騙與坑": ("要你先付錢或急著匯款時，先自己查證。", "存下 165 網站，遇到可疑交易先查。"),
    "衡量與迭代": ("觀看和點擊只是線索，詢問與成交要另外記。", "記下本週實際收到的詢問數。"),
}
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
    "# 台灣 AI（人工智慧）一人公司變現指南：30 條精華版", "",
    "先挑一件你做得到的事。這裡有 10 類、共 30 條做法；不保證收入。",
    "價格、平台規則與法規查證於 2026-10-18，動手前請重新核對。自有設備與工時是估算；記錄數字是為了看結果，不是收入承諾。", "",
    "**官方**是官方資料；**法規**是法律或主管機關資料；**推論**是根據來源提出的做法，效果還沒驗證。", "",
]
category = None
for item in items:
    if item["category"] != category:
        if category:
            lines += [f"**你現在可以做的一件事：**{SECTION[category][1]}", ""]
        category = item["category"]
        lines += [f"## {category}", "", f"**一句話懂：**{SECTION[category][0]}", ""]
    sources = "、".join(f"[{s['name']}]({s['url']})" for s in item["sources"])
    lines += [
        f"### {item['id']:03d}｜{item['conclusion']}", "",
        f"- 適合誰：{item['audience']}",
        f"- 成本（金額與時間）：{item['cost']}",
        f"- 看什麼結果：{item['revenue']}",
        f"- 照做步驟：{item['steps']}",
        f"- 資料性質：{item['evidence']}",
        f"- 來源連結：{sources}（查證日期：{item['checked']}）",
        f"- 留意：{item['risk']}", "",
    ]
lines += [f"**你現在可以做的一件事：**{SECTION[category][1]}", ""]
lines += [
    "---", "",
    "內容採 [CC BY-NC 4.0](LICENSE)；非商用轉載請標示安達與授權。需要陪跑與工具，可看 [官方 LINE](https://s.andax.me/s/fwT5bv) 或 [anda.biz](https://anda.biz)。", "",
]
(ROOT / "指南.md").write_text("\n".join(lines), encoding="utf-8")

payload = json.dumps(items, ensure_ascii=False).replace("<", "\\u003c")
section_payload = json.dumps(SECTION, ensure_ascii=False).replace("<", "\\u003c")
page = '''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>台灣 AI（人工智慧）一人公司變現指南｜30 條精華版</title>
<style>:root{font-family:system-ui,"Microsoft JhengHei",sans-serif;color:#1c2830;background:#f7f5ef}*{box-sizing:border-box}body{margin:0}header{padding:32px 18px;background:#123948;color:#fff}header>div,main,footer{max-width:1000px;margin:auto}h1{font-size:clamp(1.7rem,5vw,3rem);margin:.2em 0}p{line-height:1.7}main{padding:20px 16px}input,select{font:inherit;padding:12px;border:1px solid #9aabae;border-radius:8px;max-width:100%;background:white}input{width:min(100%,450px)}.controls{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}article{background:#fff;border:1px solid #d9e0dc;border-radius:12px;padding:18px;margin:14px 0;box-shadow:0 2px 8px #1239480b}article h2{font-size:1.2rem;margin:0 0 12px}dl{display:grid;grid-template-columns:8.5em 1fr;gap:8px}dt{font-weight:bold;color:#365c67}dd{margin:0;line-height:1.6;overflow-wrap:anywhere}dd a{display:inline-block;margin-right:.55em}a{color:#087181}footer{padding:22px 16px;background:#e6eeec}small{opacity:.9}@media(max-width:560px){dl{grid-template-columns:1fr;gap:2px}dt{margin-top:9px}.controls>*{width:100%}}</style></head><body>
<header><div><small>安達｜2026-10-18 查證｜30 條做法</small><h1>台灣 AI（人工智慧）一人公司變現指南</h1><p>先挑一件做得到的事。不保證收入。</p></div></header><main><p>每條都有成本、做法、要看的結果和來源。價格、規則與法規會變，動手前請重查。「推論」表示做法的效果尚未驗證。</p><div class="controls"><input id="search" type="search" placeholder="搜尋，例如：課程、稅籍" aria-label="搜尋條目"><select id="category" aria-label="篩選分類"><option value="">所有分類</option></select></div><p id="count" role="status"></p><div id="list"></div></main><footer>需要陪跑與工具：<a href="https://s.andax.me/s/fwT5bv">官方 LINE</a>｜<a href="https://anda.biz">anda.biz</a>。<p>內容採 <a href="https://creativecommons.org/licenses/by-nc/4.0/">CC BY-NC 4.0</a>（可非商用分享，須標示來源）。</p></footer>
<script id="sections" type="application/json">''' + section_payload + '''</script><script id="data" type="application/json">''' + payload + '''</script><script>const sections=JSON.parse(document.getElementById('sections').textContent),data=JSON.parse(document.getElementById('data').textContent);const list=document.getElementById('list'),count=document.getElementById('count'),search=document.getElementById('search'),category=document.getElementById('category');for(const name of [...new Set(data.map(x=>x.category))]){const o=document.createElement('option');o.value=name;o.textContent=name;category.append(o)}function render(){const q=search.value.trim().toLowerCase(),c=category.value;const found=data.filter(x=>(!c||x.category===c)&&(!q||JSON.stringify(x).toLowerCase().includes(q)));count.textContent=`顯示 ${found.length} / ${data.length} 條`;list.replaceChildren();let current='';for(const x of found){if(x.category!==current){if(current){const action=document.createElement('p');action.textContent=`你現在可以做的一件事：${sections[current][1]}`;list.append(action)}current=x.category;const h=document.createElement('h2'),intro=document.createElement('p');h.textContent=current;intro.textContent=`一句話懂：${sections[current][0]}`;list.append(h,intro)}const article=document.createElement('article');const title=document.createElement('h2');title.textContent=`${String(x.id).padStart(3,'0')}｜${x.conclusion}`;article.append(title);const dl=document.createElement('dl');for(const [label,key] of [['適合誰','audience'],['成本（金額與時間）','cost'],['看什麼結果','revenue'],['照做步驟','steps'],['資料性質','evidence'],['來源連結','sources'],['留意','risk']]){const dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=label;if(key==='sources'){for(const s of x.sources){const a=document.createElement('a');a.href=s.url;a.textContent=s.name;a.rel='noopener noreferrer';a.target='_blank';dd.append(a)}const time=document.createElement('small');time.textContent=`查證日期：${x.checked}`;dd.append(time)}else dd.textContent=x[key];dl.append(dt,dd)}article.append(dl);list.append(article)}if(current){const action=document.createElement('p');action.textContent=`你現在可以做的一件事：${sections[current][1]}`;list.append(action)}}search.addEventListener('input',render);category.addEventListener('change',render);render();</script></body></html>'''
(ROOT / "site").mkdir(exist_ok=True)
(ROOT / "site" / "index.html").write_text(page, encoding="utf-8")
print(f"已產生 {len(items)} 條精華指南與離線單頁")
