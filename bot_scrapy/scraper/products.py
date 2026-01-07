# scrapy runspider engine.py -o products.json --loglevel=CRITICAL

import re
import scrapy
from scrapy_playwright.page import PageMethod
import os
import requests
from dotenv import load_dotenv
import re
from urllib.parse import urlparse

def normalize_ml_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    path = re.sub(r"_Desde_\d+_", "", path)
    path = re.sub(r"_NoIndex_True.*", "", path)
    return f"https://lista.mercadolivre.com.br/{path}"


class Products(scrapy.Spider):
    load_dotenv()
    name = "products"
    output_file = "products.json"
    if os.path.exists(output_file):
        os.remove(output_file)

    # Número máximo de páginas a percorrer (padrão: 1)
    MAX_PAGES = 5
    PRODUCTS_PER_PAGE = 48  # Mercado Livre padrão
    MINIMUM_DISCOUNT_PERCENT = 20  # Percentual mínimo de desconto
    API_URL = os.getenv("API_URL")
    API_KEY = os.getenv("API_KEY")

    custom_settings = {
        "FEED_EXPORT_ENCODING": "utf-8",
        "LOG_LEVEL": "CRITICAL",
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": True,
        },
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    def start_requests(self):
        if not self.categories:
            self.logger.warning("Nenhuma categoria carregada. Verifique a API.")
            return

        for category in self.categories:
            if category.get("active", True):
                yield self.make_playwright_request(
                    category["link"], page_number=1, category_id=category["id"]
                )

    def make_playwright_request(self, url, page_number=1, category_id=None):
        return scrapy.Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            },
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod(
                        "wait_for_selector", "li.ui-search-layout__item", timeout=60000
                    ),
                    PageMethod(
                        "evaluate",
                        """
                        async () => {
                            const sleep = ms => new Promise(r => setTimeout(r, ms));
                            const step = window.innerHeight * 0.8;
                            let current = 0;
                            const total = document.body.scrollHeight;

                            while (current < total) {
                                window.scrollTo(0, current);
                                await sleep(700);
                                current += step;
                            }

                            window.scrollTo(0, document.body.scrollHeight);
                            await sleep(1000);
                        }
                        """,
                    ),
                ],
                "page_number": page_number,
                "category_id": category_id,  # <-- aqui!
            },
            callback=self.parse,
        )

    def parse(self, response):
        page_number = response.meta.get("page_number", 1)

        products = response.css("li.ui-search-layout__item")
        for product in products:
            # Extrai todos os dados do produto (mesmo que já está no seu código)
            name = product.css("a.poly-component__title::text").get()
            image = product.css("img.poly-component__picture::attr(src)").get()
            discount_percent = product.css(".poly-price__disc_label--pill::text").get()
            if discount_percent:
                discount_percent = discount_percent.strip().replace("% OFF", "")
                discount_percent = float(discount_percent)

            if self.MINIMUM_DISCOUNT_PERCENT:
                if not discount_percent or discount_percent < self.MINIMUM_DISCOUNT_PERCENT:
                    continue
                
            old_price_fraction = product.css(
                "s.andes-money-amount--previous span.andes-money-amount__fraction::text"
            ).get()
            old_price_cents = product.css(
                "s.andes-money-amount--previous span.andes-money-amount__cents::text"
            ).get()
            old_price = None
            if old_price_fraction:
                fraction = old_price_fraction.strip().replace(".", "")
                cents = old_price_cents.strip() if old_price_cents else "00"
                if fraction.isdigit() and cents.isdigit():
                    old_price = float(f"{fraction}.{cents}")

            price_fraction = product.css(
                "div.poly-price__current span.andes-money-amount__fraction::text"
            ).get()
            price_cents = product.css(
                "div.poly-price__current span.andes-money-amount__cents::text"
            ).get()
            price = None
            if price_fraction:
                fraction = price_fraction.strip().replace(".", "")
                cents = price_cents.strip() if price_cents else "00"
                if fraction.isdigit() and cents.isdigit():
                    price = float(f"{fraction}.{cents}")

            installements_text = product.css("span.poly-price__installments::text").get()
            installements = None
            if installements_text and "x" in installements_text:
                qty = installements_text.split("x")[0].strip()
                if qty.isdigit():
                    installements = int(qty)

            installements_fraction = product.css(
                "span.poly-price__installments span.andes-money-amount__fraction::text"
            ).get()
            installements_cents = product.css(
                "span.poly-price__installments span.andes-money-amount__cents::text"
            ).get()
            
            installements_value = None
            
            if installements_fraction:
                fraction = installements_fraction.strip().replace(".", "")
                cents = installements_cents.strip() if installements_cents else "00"
                if installements_fraction:
                    installements_value = float(f"{fraction}.{cents}")
                    
            interest_text = product.css("span.poly-price__installments *::text").getall()
            interest_free = "sem juros" in " ".join(interest_text).lower()
            link = product.css("h3 a.poly-component__title::attr(href)").get()
            external_id = None
            if link:
                match = re.search(r"(MLB-?\d+)", link)
                if match:
                    external_id = match.group(1)
                                

            category_id = response.meta.get("category_id")

            # Monta o payload para enviar via API
            payload = {
                "name": name,
                "image": image,
                "old_price": old_price,
                "price": price,
                "installements": installements,
                "installements_value": installements_value,
                "interest_free": interest_free,
                "link": link,
                "external_id": external_id,
                "discount_percent": discount_percent,
                "category": category_id,
            }
            
            headers = {
                "Authorization": f"Api-Key {self.API_KEY}",
                "Content-Type": "application/json",
            }

            # Envia para o Django
            try:
                response_api = requests.post(
                    self.API_URL + '/api/product/create/', headers=headers, json=payload, timeout=10
                )
                if response_api.status_code == 200:
                    self.logger.info(
                        f"Produto enviado: {name} - {response_api.json().get('status')}"
                    )
                else:
                    self.logger.error(f"Erro ao enviar produto {name}: {response_api.text}")
            except Exception as e:
                self.logger.error(f"Exceção ao enviar produto {name}: {str(e)}")

        # PAGINAÇÃO (mesmo que antes)
        if page_number < self.MAX_PAGES:
            per_page = len(products)
            if per_page == 0:
                return

            base_url = normalize_ml_url(response.url)

            next_page_offset = 1 + self.PRODUCTS_PER_PAGE * page_number

            next_page_url = (
                f"{base_url}_Desde_{next_page_offset}_NoIndex_True"
            )

            yield self.make_playwright_request(
                next_page_url,
                page_number=page_number + 1,
                category_id=category_id
            )
