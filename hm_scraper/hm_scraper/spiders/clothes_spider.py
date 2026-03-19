import re

import scrapy
from scrapy_playwright.page import PageMethod


class HmApiSpider(scrapy.Spider):
    name = "hm_api"
    allowed_domains = ["www2.hm.com"]
    start_urls = [
        "https://www2.hm.com/bg_bg/productpage.1274171042.html",
    ]

    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept-Language": "bg-BG,bg;q=0.9,en-US;q=0.8,en;q=0.7",
                },
                meta={
                    "playwright": True,
                    "playwright_context": "default",
                    "playwright_page_goto_kwargs": {"wait_until": "domcontentloaded"},
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "div.fd9cd8 a[title]", timeout=45000),
                    ],
                },
            )

    def parse(self, response):
        colors = self._clean_list(
            response.xpath("//div[contains(@class, 'fd9cd8')]//a/@title").getall()
        )
        current_color = self._clean_text(
            response.xpath("//div[contains(@class, 'fd9cd8')]//a[@aria-checked='true']/@title").get()
        )
        name = self._clean_text(response.xpath('//*[@data-testid="product-name"]/text()').get())
        price = self._clean_text(response.xpath('//*[@data-testid="white-price"]/text()').get())
        reviews_count = self._extract_int(
            response.xpath('//*[contains(@aria-label, "Коментари")]/text()').get()
        )
        reviews_score = self._extract_float(
            response.xpath("//*[contains(@data-testid, 'reviews-summary-button')]/@title").get()
        )

        yield {
            "available_colors": colors,
            "name": name,
            "price": price,
            "current_color": current_color,
            "reviews_count": reviews_count,
            "reviews_score": reviews_score,
        }


# Помощни функции за изчистване на данните.

    def _clean_text(self, value):
        if not value:
            return None

        return " ".join(value.replace("\xa0", " ").split())

    def _clean_list(self, values):
        cleaned_values = []

        for value in values:
            cleaned_value = self._clean_text(value)
            if cleaned_value:
                cleaned_values.append(cleaned_value)

        return cleaned_values

    def _extract_int(self, value):
        cleaned_value = self._clean_text(value)
        if not cleaned_value:
            return None

        match = re.search(r"\d+", cleaned_value)
        if not match:
            return None

        return int(match.group())

    def _extract_float(self, value):
        cleaned_value = self._clean_text(value)
        if not cleaned_value:
            return None

        match = re.search(r"\d+(?:[.,]\d+)?", cleaned_value)
        if not match:
            return None

        return float(match.group().replace(",", "."))
