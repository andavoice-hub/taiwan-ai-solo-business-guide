"""驗證精華版的內容門檻與 Markdown／離線網頁同步。"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parent
markdown = (ROOT / "指南.md").read_text(encoding="utf-8")
page = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
marker = '<script id="data" type="application/json">'
assert marker in page, "網頁缺嵌入資料"
items = json.loads(page.split(marker, 1)[1].split("</script>", 1)[0])
required = {"id", "category", "conclusion", "audience", "cost", "revenue",
            "evidence", "steps", "risk", "sources", "checked", "reverse"}
assert len(items) == 30, "精華版應為每類 3 條、共 30 條"
assert markdown.count("\n### ") == len(items)
assert [item["id"] for item in items] == list(range(1, len(items) + 1))
assert all(required <= item.keys() and all(item[key] for key in required - {"reverse"}) for item in items)
assert len({item["category"] for item in items}) == 10
assert all(n == 3 for n in Counter(item["category"] for item in items).values())
assert all(n >= 2 for n in Counter(item["category"] for item in items if item["reverse"]).values())
assert all(item["evidence"] in {"官方", "法規", "研究", "多方報導", "個人經驗", "推論"} for item in items)


def canonical(url: str) -> str:
    part = urlsplit(url)
    assert part.scheme == "https" and part.netloc and not part.fragment, url
    # 同頁的追蹤參數不應偽裝成另一個來源。
    query = "&".join(q for q in part.query.split("&") if q and not q.startswith(("utm_", "trk=", "authuser=")))
    return urlunsplit((part.scheme, part.netloc.lower(), part.path.rstrip("/"), query, ""))


urls = []
for item in items:
    assert len(item["sources"]) >= 2, item["id"]
    own = []
    for source in item["sources"]:
        assert source["name"] and source["url"]
        url = canonical(source["url"])
        own.append(url)
        urls.append(url)
        assert source["url"] in markdown, f"Markdown 缺來源：{url}"
    assert len(own) == len(set(own)), f"第 {item['id']} 條同頁重複計數"

source_counts = Counter(urls)
assert len(source_counts) >= 70, f"只有 {len(source_counts)} 個不同來源，至少需 70"
assert max(source_counts.values()) <= 3, "某來源被超過 3 條共用"
inference_rate = sum(i["evidence"] == "推論" for i in items) / len(items)
vague_rate = sum(i["revenue"] == "依個人而異" for i in items) / len(items)
assert inference_rate <= .30, f"推論比例 {inference_rate:.1%} 超過 30%"
assert vague_rate <= .50, f"『依個人而異』比例 {vague_rate:.1%} 超過 50%"

duplicate_rates = {}
for field in ("cost", "risk", "revenue", "steps"):
    duplicate_rates[field] = 1 - len({i[field].strip() for i in items}) / len(items)
    assert duplicate_rates[field] <= .20, f"{field} 欄位重複率過高：{duplicate_rates[field]:.1%}"
    for category in {i["category"] for i in items}:
        values = [i[field].strip() for i in items if i["category"] == category]
        assert len(values) == len(set(values)), f"{category} 的 {field} 重複"

assert "<script src=" not in page and '<link rel="stylesheet"' not in page
print(f"PASS：{len(items)} 條／10 類；{len(source_counts)} 個不同來源；"
      f"推論 {inference_rate:.1%}；依個人而異 {vague_rate:.1%}；"
      f"欄位重複率 {duplicate_rates}；離線網頁嵌入資料")
