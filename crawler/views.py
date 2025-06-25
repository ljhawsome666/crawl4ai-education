import json
import os
from datetime import datetime
from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils.text import slugify
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
from .models import CrawlResultShowcase
from asgiref.sync import sync_to_async


# HTML 转 Markdown 的递归函数
def html_to_markdown(element):
    if isinstance(element, NavigableString):
        return element.strip()
    if not isinstance(element, Tag):
        return ""

    if element.name == "span" and "math" in element.get("class", []):
        content = element.get_text(strip=True)
        return f"\n$$\n{content}\n$$\n"

    if element.name == "script" and element.get("type") in ["math/tex", "math/tex; mode=display"]:
        content = element.string or ""
        return f"\n$$\n{content.strip()}\n$$\n"

    if element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
        level = int(element.name[1])
        prefix = "#" * level
        content = ''.join(html_to_markdown(child) for child in element.children)
        return f"\n{prefix} {content.strip()}\n\n"

    if element.name == "p":
        content = ''.join(html_to_markdown(child) for child in element.children)
        return f"\n{content.strip()}\n\n"

    if element.name == "ul":
        items = [f"- {html_to_markdown(li).strip()}" for li in element.find_all("li", recursive=False)]
        return "\n".join(items) + "\n\n"

    if element.name == "ol":
        items = [f"{idx}. {html_to_markdown(li).strip()}" for idx, li in enumerate(element.find_all("li", recursive=False), 1)]
        return "\n".join(items) + "\n\n"

    if element.name == "table":
        rows = []
        headers = []
        thead = element.find("thead")
        if thead:
            headers = [th.get_text(strip=True) for th in thead.find_all("th")]
        else:
            first_row = element.find("tr")
            if first_row:
                headers = [th.get_text(strip=True) for th in first_row.find_all(["th", "td"])]
        if headers:
            rows.append("| " + " | ".join(headers) + " |")
            rows.append("| " + " | ".join(["---"] * len(headers)) + " |")

        trs = element.find("tbody").find_all("tr") if element.find("tbody") else element.find_all("tr")[1:]
        for tr in trs:
            cols = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
            rows.append("| " + " | ".join(cols) + " |")
        return "\n".join(rows) + "\n\n"

    if element.name == "blockquote":
        content = ''.join(html_to_markdown(child) for child in element.children).strip()
        lines = content.splitlines()
        return "\n" + "\n".join("> " + line for line in lines) + "\n\n"

    return ''.join(html_to_markdown(child) for child in element.children)



@csrf_exempt
async def crawl_and_filter(request):
    if request.method != 'POST':
        return JsonResponse({'error': '仅支持POST请求'}, status=405)

    try:
        body = json.loads(request.body)
        url = body.get('url')
        raw_keyword = body.get('keyword', '')
        if not url or not raw_keyword:
            return JsonResponse({'error': 'URL和关键词不能为空'}, status=400)

        keywords = [kw.strip().lower() for kw in raw_keyword.replace('，', ',').split(',') if kw.strip()]
        if not keywords:
            return JsonResponse({'error': '无有效关键词'}, status=400)

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
                    md = html_to_markdown(para)
                    matched_sections.append(md)

            if matched_sections:
                markdown = '\n'.join(matched_sections)
                title = page.metadata.get("title", "")
                if not isinstance(title, str):
                    title = str(title)

                # ✅ 解决 500 报错：使用 sync_to_async 保存
                await sync_to_async(CrawlResultShowcase.objects.create)(
                    url=page.url,
                    keyword=raw_keyword,
                    content_preview=markdown[:500],
                    is_approved=False,
                )

                filtered_results.append({
                    "url": page.url,
                    "title": title,
                    "markdown": markdown[:10000]
                })

        # 保存为 markdown 文件
        if filtered_results:
            output_dir = os.path.join(settings.BASE_DIR, "output_files")
            os.makedirs(output_dir, exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"crawl_result_{slugify(raw_keyword)}_{timestamp}.md"
            filepath = os.path.join(output_dir, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                for item in filtered_results:
                    title = item.get("title") or "无标题"
                    url_link = item.get("url") or "#"
                    markdown = item.get("markdown", "")
                    if not isinstance(markdown, str):
                        markdown = str(markdown)

                    f.write(f"# {title}\n")
                    f.write(f"链接: {url_link}\n\n")
                    f.write(markdown)
                    f.write("\n\n---\n\n")

            return JsonResponse({
                'results': filtered_results,
                'filename': filename,
                'download_url': f"/api/download/{filename}"
            })

        else:
            return JsonResponse({'results': [], 'filename': '', 'download_url': ''})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


# ✅ 新增：下载 Markdown 文件接口
def download_file(request, filename):
    output_dir = os.path.join(settings.BASE_DIR, "output_files")
    file_path = os.path.join(output_dir, filename)

    if not os.path.exists(file_path):
        raise Http404("文件不存在")

    response = FileResponse(open(file_path, 'rb'), content_type='text/markdown; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response

def list_showcases(request):
    data = CrawlResultShowcase.objects.filter(is_approved=True).order_by('-created_at')
    result = [{
        'url': item.url,
        'keyword': item.keyword,
        'content_preview': item.content_preview,
    } for item in data]
    return JsonResponse(result, safe=False)