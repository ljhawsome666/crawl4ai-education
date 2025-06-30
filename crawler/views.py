import os
import requests
import zipfile
from datetime import datetime
from django.conf import settings
from django.utils.text import slugify
from bs4 import BeautifulSoup, NavigableString, Tag

from crawler.models import CrawlResultShowcase
from asgiref.sync import sync_to_async

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import (
    BFSDeepCrawlStrategy,
    DFSDeepCrawlStrategy,
    BestFirstCrawlingStrategy
)

from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer
from crawl4ai.async_configs import BrowserConfig
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy


# ---------- Markdown 转换函数 ----------
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

# ---------- 图片与关键词相关性判断 ----------
def is_image_relevant(img: Tag, keywords: list) -> bool:
    def text_contains_kw(text):
        return text and any(kw in text.lower() for kw in keywords)

    if text_contains_kw(img.get("alt")):
        return True

    figcaption = img.find_parent("figure")
    if figcaption:
        caption_text = figcaption.find("figcaption")
        if caption_text and text_contains_kw(caption_text.get_text(strip=True)):
            return True

    parent_text = img.find_parent()
    if parent_text and text_contains_kw(parent_text.get_text(strip=True)):
        return True

    if text_contains_kw(img.get("src", "")):
        return True

    return False


# ---------- 主函数（整合版） ----------
async def run_crawler(
    url: str,
    raw_keyword: str,
    max_depth: int = 1,
    include_external: bool = False,
    strategy: str = 'bfs'
):
    keywords = [kw.strip().lower() for kw in raw_keyword.replace('，', ',').split(',') if kw.strip()]
    if not keywords:
        return {'results': [], 'filename': '', 'download_url': ''}

    # ✅ 根据策略选择 deep_crawl_strategy
    strategy = strategy.lower()
    if strategy == 'dfs':
        deep_strategy = DFSDeepCrawlStrategy(
            max_depth=max_depth,
            include_external=include_external,
            max_pages=30
        )
    elif strategy == 'bestfirst':
        scorer = KeywordRelevanceScorer(
            keywords=keywords,
            weight=0.7
        )
        deep_strategy = BestFirstCrawlingStrategy(
            max_depth=max_depth,
            include_external=include_external,
            url_scorer=scorer,
            max_pages=30
        )
    else:  # 默认使用 bfs
        deep_strategy = BFSDeepCrawlStrategy(
            max_depth=max_depth,
            include_external=include_external,
            max_pages=30
        )


    browser_cfg = BrowserConfig(
        browser_type="chromium",
        headless=True,
        user_agent_mode="random",
        text_mode=True,  # ✅ 让系统返回 HTML + 文本抽取后的 cleaned_html
        verbose=True
    )

    crawler = AsyncWebCrawler(config=browser_cfg)

    config = CrawlerRunConfig(
        deep_crawl_strategy=deep_strategy,
        scraping_strategy=LXMLWebScrapingStrategy(),  # 或者你的其他策略
        verbose=True,
        stream=False,
    )

    results = await crawler.arun(url=url, config=config)

    filtered_results = []
    output_dir = os.path.join(settings.BASE_DIR, "output_files")
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    safe_keyword = slugify(raw_keyword)
    os.makedirs(output_dir, exist_ok=True)

    temp_dir = os.path.join(output_dir, f"temp_{safe_keyword}_{timestamp}")
    os.makedirs(temp_dir, exist_ok=True)

    image_dir = os.path.join(temp_dir, "images")
    os.makedirs(image_dir, exist_ok=True)

    md_filename = "result.md"
    md_filepath = os.path.join(temp_dir, md_filename)

    with open(md_filepath, "w", encoding="utf-8") as f:
        for page in results:
            html = page.cleaned_html or ""
            print(f"[DEBUG] 页面URL: {page.url}")
            print(f"[DEBUG] 页面标题: {page.metadata.get('title')}")
            print(f"[DEBUG] 页面HTML长度: {len(html)}")
            print(f"[DEBUG] 页面命中关键词？{any(kw in html.lower() for kw in keywords)}")
            if not html or not any(kw in html.lower() for kw in keywords):
                continue

            soup = BeautifulSoup(html, "html.parser")
            paragraphs = soup.find_all(['p', 'li', 'blockquote'])

            matched_sections = []
            image_markdown_lines = []

            for para in paragraphs:
                text = para.get_text(strip=True)
                if any(kw in text.lower() for kw in keywords):
                    matched_sections.append(html_to_markdown(para))

            # 图片处理
            img_tags = soup.find_all("img")
            for idx, img in enumerate(img_tags):
                img_url = img.get("src")
                if not img_url or not img_url.startswith("http"):
                    continue
                if not is_image_relevant(img, keywords):
                    continue

                try:
                    headers = {
                        "User-Agent": "Mozilla/5.0",
                        "Accept": "image/*,*/*;q=0.8",
                        "Referer": url
                    }
                    response = requests.get(img_url, headers=headers, timeout=10)
                    response.raise_for_status()
                    img_data = response.content

                    img_ext = os.path.splitext(img_url)[-1].split("?")[0][:5]
                    img_ext = img_ext if img_ext.startswith('.') else '.jpg'
                    img_filename = f"{safe_keyword}_{timestamp}_{idx}{img_ext}"
                    img_path = os.path.join(image_dir, img_filename)

                    with open(img_path, "wb") as img_file:
                        img_file.write(img_data)

                    alt_text = img.get("alt", "图片")
                    image_markdown_lines.append(f"![{alt_text}](images/{img_filename})")

                except Exception as e:
                    print(f"[图片下载失败] {img_url}: {e}")

            if matched_sections or image_markdown_lines:
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
                if image_markdown_lines:
                    f.write("\n\n## 相关图片\n\n")
                    f.write('\n\n'.join(image_markdown_lines))
                f.write("\n\n---\n\n")

                filtered_results.append({
                    "url": page.url,
                    "title": title,
                    "markdown": markdown[:10000]
                })

    # 打包为 zip
    zip_filename = f"crawl_result_{safe_keyword}_{timestamp}.zip"
    zip_filepath = os.path.join(output_dir, zip_filename)
    with zipfile.ZipFile(zip_filepath, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, temp_dir)
                zipf.write(full_path, arcname=arcname)

    # 删除中间临时目录
    try:
        import shutil
        shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"[清理失败] {temp_dir}: {e}")

    return {
        'results': filtered_results,
        'filename': zip_filename,
        'download_url': f"/api/download/{zip_filename}"
    }

