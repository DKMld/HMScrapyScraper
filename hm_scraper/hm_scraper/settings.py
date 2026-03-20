import os


BOT_NAME = "hm_scraper"

SPIDER_MODULES = ["hm_scraper.spiders"]
NEWSPIDER_MODULE = "hm_scraper.spiders"

ROBOTSTXT_OBEY = False
FEED_EXPORT_ENCODING = "utf-8"
FEEDS = {
    "output.json": {
        "format": "json",
        "overwrite": True,
        "indent": 2,
    }
}

USER_AGENT = None

DOWNLOAD_HANDLERS = {
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": os.getenv("PLAYWRIGHT_HEADLESS", "0").lower() in {"1", "true", "yes"},
}
PLAYWRIGHT_CONTEXTS = {
    "default": {
        "locale": "bg-BG",
        "timezone_id": "Europe/Sofia",
    }
}
PLAYWRIGHT_PROCESS_REQUEST_HEADERS = None

DOWNLOAD_DELAY = 2
