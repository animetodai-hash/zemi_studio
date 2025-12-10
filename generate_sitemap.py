#!/usr/bin/env python3
import os
from datetime import datetime, timezone

# ===== 設定 =====
BASE_URL = "https://animetodai-hash.github.io/zemi_studio"
ROOT_DIR = "."  # リポジトリのルートから走査

# sitemap に含めたくないファイル（必要なら増やしてOK）
EXCLUDE_FILES = {
    "googleae6ad0c4a1c1fd80.html",
    "googled76a05602482aa7e.html",
}

def html_path_to_url(path: str) -> str:
    # path: ./animezemi/index.html みたいな相対パス
    rel = os.path.relpath(path, ROOT_DIR).replace(os.sep, "/")

    # 先頭の ./ を削る
    if rel.startswith("./"):
        rel = rel[2:]

    # ルートの index.html → /
    if rel == "index.html":
        return BASE_URL + "/"

    # ディレクトリ配下の index.html → /dir/
    if rel.endswith("/index.html"):
        url_path = "/" + rel[:-len("index.html")]
        return BASE_URL + url_path

    # それ以外のHTML → /path/file.html
    return BASE_URL + "/" + rel

def collect_urls():
    urls = []

    for root, dirs, files in os.walk(ROOT_DIR):
        # .git や .github などは無視
        if ".git" in root or ".github" in root:
            continue

        for f in files:
            if not f.endswith(".html"):
                continue
            if f in EXCLUDE_FILES:
                continue

            full_path = os.path.join(root, f)
            url = html_path_to_url(full_path)
            urls.append(url)

    # ルートトップを優先的に前に（あれば）
    urls = sorted(set(urls))
    return urls

def generate_sitemap(urls):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    url_entries = []
    for u in urls:
        # index.html 系だけ priority 上げる
        priority = "1.0" if u.rstrip("/").endswith("/zemi_studio") or u.endswith("/zemi_studio/") else "0.8"
        entry = f"""  <url>
    <loc>{u}</loc>
    <lastmod>{now}</lastmod>
    <priority>{priority}</priority>
  </url>"""
        url_entries.append(entry)

    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{os.linesep.join(url_entries)}
</urlset>
"""
    return content

def main():
    urls = collect_urls()
    sitemap = generate_sitemap(urls)
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"Generated sitemap.xml with {len(urls)} URLs")

if __name__ == "__main__":
    main()
