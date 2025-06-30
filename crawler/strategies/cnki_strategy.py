from crawl4ai.content_scraping_strategy import WebScrapingStrategy
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from bs4 import BeautifulSoup
import re
from dataclasses import dataclass

@dataclass
class LinkCandidate:
    url: str
    anchor: str = ""
    score: float = 0.0
    depth: int = 0

class CNKIScrapingStrategy(WebScrapingStrategy):
    def __init__(self, llm_extractor: LLMExtractionStrategy):
        super().__init__()
        self.extraction_strategy = llm_extractor

    def should_visit(self, url: str, html: str | None = None) -> bool:
        if re.search(r"\.(exe|pdf|docx?|zip|rar|tar|gz|xls[x]?)($|\?)", url, re.IGNORECASE):
            return False

        forbidden_keywords = [
            "login", "logout", "passport", "account", "register",
            "center", "recommend", "favorite", "message", "user", "personal",
            "help", "weixin", "wechat", "baidu", "sogou", "qikan", "d.cnki.net"
        ]
        if any(k in url.lower() for k in forbidden_keywords):
            return False

        if re.search(r"(KXReader|kreader|Article|Detail|fulltext|paperinfo)[\w\-]*\.aspx", url, re.IGNORECASE):
            return True

        if html:
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text().lower()

            if soup.select_one(".wxTitle, .title, h1") and "请登录" not in text:
                return True
            if "知网个人中心" in text or "请登录" in text:
                return False

        return False

    def transform_url_if_needed(self, url: str, html: str | None = None) -> str:
        if html and "kns.cnki.net/kcms2/article/abstract" in url:
            soup = BeautifulSoup(html, "html.parser")
            iframe = soup.find("iframe")
            if iframe and iframe.get("src") and "xml.html" in iframe.get("src"):
                return "https://kns.cnki.net" + iframe["src"]
        return url

    def extract_links(self, page) -> list[LinkCandidate]:
        soup = BeautifulSoup(page.raw_html or "", "html.parser")
        candidates = []

        for a in soup.find_all("a", href=True):
            href = a['href']
            if href.startswith("javascript:") or href.startswith("#"):
                continue
            if not href.startswith("http"):
                href = re.sub(r"^/+", "", href)
                href = "https://kns.cnki.net/" + href
            candidates.append(LinkCandidate(url=href, anchor=a.get_text(strip=True)))

        for iframe in soup.find_all("iframe"):
            src = iframe.get("src")
            if src and "xml.html" in src:
                if not src.startswith("http"):
                    src = "https://kns.cnki.net" + src
                candidates.append(LinkCandidate(url=src, anchor="iframe"))

        return candidates
