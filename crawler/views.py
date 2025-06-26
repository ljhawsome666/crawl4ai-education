import os
import re
import requests
import zipfile
from datetime import datetime
from django.conf import settings
from django.utils.text import slugify
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
from crawl4ai import AsyncWebCrawler
from crawler.models import CrawlResultShowcase
from asgiref.sync import sync_to_async
from urllib.parse import urljoin


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
        elif first := element.find("tr"):
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


async def run_crawler(url: str, raw_keyword: str):
    keywords = [kw.strip().lower() for kw in raw_keyword.replace('，', ',').split(',') if kw.strip()]
    if not keywords:
        return {'results': [], 'filename': '', 'download_url': ''}

    crawler = AsyncWebCrawler()
    results = await crawler.arun(url=url, max_pages=10)

    filtered_results = []
    output_dir = os.path.join(settings.BASE_DIR, "output_files")
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    safe_keyword = slugify(raw_keyword)
    os.makedirs(output_dir, exist_ok=True)

    # 图片保存目录
    image_dir = os.path.join(output_dir, f"images_{safe_keyword}_{timestamp}")
    os.makedirs(image_dir, exist_ok=True)

    md_filename = f"crawl_result_{safe_keyword}_{timestamp}.md"
    md_filepath = os.path.join(output_dir, md_filename)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ),
        "Accept": "image/*,*/*;q=0.8",
        "Referer": url
    }

    with open(md_filepath, "w", encoding="utf-8") as f:
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

            # ✅ 下载页面中所有图片
            img_tags = soup.find_all("img")
            for idx, img in enumerate(img_tags):
                img_url = img.get("src")
                if not img_url:
                    continue
                if img_url.startswith("//"):
                    img_url = "https:" + img_url
                elif img_url.startswith("/"):
                    img_url = urljoin(page.url, img_url)
                elif not img_url.startswith("http"):
                    continue

                try:
                    resp = requests.get(img_url, headers=headers, timeout=8)
                    resp.raise_for_status()
                    ext = os.path.splitext(img_url)[-1].split("?")[0][:5]
                    ext = ext if ext.startswith(".") else ".jpg"
                    safe_img_name = re.sub(r"[^a-zA-Z0-9_.-]", "_", os.path.basename(img_url))
                    if not safe_img_name.endswith(ext):
                        safe_img_name += ext
                    img_filename = f"{idx}_{safe_img_name}"
                    img_path = os.path.join(image_dir, img_filename)
                    with open(img_path, "wb") as img_file:
                        img_file.write(resp.content)
                except Exception as e:
                    print(f"[图片下载失败] {img_url}: {e}")

            if matched_sections:
                markdown = '\n'.join(matched_sections)
                title = str(page.metadata.get("title", "") or "")

                await sync_to_async(CrawlResultShowcase.objects.create)(
                    url=page.url,
                    keyword=raw_keyword,
                    content_preview=markdown[:500]
                )

                f.write(f"# {title or '无标题'}\n")
                f.write(f"链接: {page.url}\n\n")
                f.write(markdown or '')
                f.write("\n\n---\n\n")

                filtered_results.append({
                    "url": page.url,
                    "title": title,
                    "markdown": markdown[:10000]
                })

    # ✅ 打包 markdown 文件和图片为 zip
    zip_filename = f"crawl_result_{safe_keyword}_{timestamp}.zip"
    zip_filepath = os.path.join(output_dir, zip_filename)
    with zipfile.ZipFile(zip_filepath, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(md_filepath, arcname=md_filename)
        for root, dirs, files in os.walk(image_dir):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, output_dir)
                zipf.write(full_path, arcname=arcname)

    return {
        'results': filtered_results,
        'filename': zip_filename,
        'download_url': f"/api/download/{zip_filename}"
    }
