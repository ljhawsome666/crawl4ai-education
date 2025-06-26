# crawler/views.py —— 功能模块（不再作为 Django 视图使用）

import os
from datetime import datetime
from django.conf import settings
from django.utils.text import slugify
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
from crawl4ai import AsyncWebCrawler
from crawler.models import CrawlResultShowcase
from asgiref.sync import sync_to_async


def html_to_markdown(element):
    if isinstance(element, NavigableString):
        return element.strip()
    if not isinstance(element, Tag):
        return ""
    if element.name == "span" and "math" in element.get("class", []):
        return f"\n$$\n{element.get_text(strip=True)}\n$$\n"
    if element.name == "script" and element.get("type") in ["math/tex", "math/tex; mode=display"]:
        return f"\n$$\n{(element.string or '').strip()}\n$$\n"
    if element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
        level = int(element.name[1])
        return f"\n{'#' * level} {''.join(html_to_markdown(c) for c in element.children).strip()}\n\n"
    if element.name == "p":
        return f"\n{''.join(html_to_markdown(c) for c in element.children).strip()}\n\n"
    if element.name == "ul":
        return "\n".join(f"- {html_to_markdown(li).strip()}" for li in element.find_all("li", recursive=False)) + "\n\n"
    if element.name == "ol":
        return "\n".join(f"{i+1}. {html_to_markdown(li).strip()}" for i, li in enumerate(element.find_all("li", recursive=False))) + "\n\n"
    if element.name == "table":
        rows, headers = [], []
        thead = element.find("thead")
        if thead:
            headers = [th.get_text(strip=True) for th in thead.find_all("th")]
        elif (first := element.find("tr")):
            headers = [th.get_text(strip=True) for th in first.find_all(["th", "td"])]
        if headers:
            rows.append("| " + " | ".join(headers) + " |")
            rows.append("| " + " | ".join(["---"] * len(headers)) + " |")
        trs = element.find("tbody").find_all("tr") if element.find("tbody") else element.find_all("tr")[1:]
        for tr in trs:
            cols = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
            rows.append("| " + " | ".join(cols) + " |")
        return "\n".join(rows) + "\n\n"
    if element.name == "blockquote":
        content = ''.join(html_to_markdown(c) for c in element.children).strip()
        return "\n" + "\n".join("> " + line for line in content.splitlines()) + "\n\n"
    return ''.join(html_to_markdown(c) for c in element.children)


# ✅ 主功能：异步爬虫逻辑，供 dashboard 直接调用
async def run_crawler(url: str, raw_keyword: str):
    keywords = [kw.strip().lower() for kw in raw_keyword.replace('，', ',').split(',') if kw.strip()]
    if not keywords:
        return {'results': [], 'filename': '', 'download_url': ''}

    crawler = AsyncWebCrawler()
    results = await crawler.arun(url=url, max_pages=10)

    filtered_results = []

    for page in results:
        html = page.cleaned_html or ""
        if not html or not any(kw in html.lower() for kw in keywords):
            continue

        soup = BeautifulSoup(html, "html.parser")
        paragraphs = soup.find_all(['p', 'li', 'blockquote'])

        matched_sections = []
        for para in paragraphs:
            text = para.get_text(strip=True)
            if any(kw in text.lower() for kw in keywords):
                matched_sections.append(html_to_markdown(para))

        if matched_sections:
            markdown = '\n'.join(matched_sections)
            title = str(page.metadata.get("title", "") or "")

            await sync_to_async(CrawlResultShowcase.objects.create)(
                url=page.url,
                keyword=raw_keyword,
                content_preview=markdown[:500]
            )

            filtered_results.append({
                "url": page.url,
                "title": title,
                "markdown": markdown[:10000]
            })

    filename = ''
    if filtered_results:
        output_dir = os.path.join(settings.BASE_DIR, "output_files")
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"crawl_result_{slugify(raw_keyword)}_{timestamp}.md"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            for item in filtered_results:
                f.write(f"# {item['title'] or '无标题'}\n")
                f.write(f"链接: {item['url']}\n\n")
                f.write(item['markdown'] or '')
                f.write("\n\n---\n\n")

    return {
        'results': filtered_results,
        'filename': filename,
        'download_url': f"/api/download/{filename}" if filename else ''
    }
