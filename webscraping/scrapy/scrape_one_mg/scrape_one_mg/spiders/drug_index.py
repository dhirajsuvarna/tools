import scrapy
from ..items import DrugSummaryItem, DrugInfoItem
import time
import urllib


class DrugIndexSpider(scrapy.Spider):
    name = "index"
    allowed_domains = ["www.1mg.com"]
    start_urls = ["https://www.1mg.com/drugs-all-medicines?page=1&label=g"]

    # def start_requests(self):
    #     yield scrapy.Request(self.start_urls[0], meta={"playwright": True})

    def parse(self, response):
        for alphabet in range(ord("g"), ord("g") + 1):
            link = (
                f"https://www.1mg.com/drugs-all-medicines?page=1&label={chr(alphabet)}"
            )
            print(f"Scraping Alphabet link: {link}")
            yield response.follow(link, callback=self.parse_pagination)

    def parse_pagination(self, response):
        out = urllib.parse.urlsplit(response.request.url)
        alphabet = urllib.parse.parse_qs(out.query)["label"][0]

        last_page = response.css("ul.list-pagination li")[-2]
        last_page_number = int(last_page.css("a::text").get())
        print(f"Total number of pages: {last_page_number}")
        # time.sleep(10)
        last_page_number = 2
        for page_number in range(1, last_page_number + 1):
            link = f"https://www.1mg.com/drugs-all-medicines?page={page_number}&label={alphabet}"
            print(f"Scraping summary link: {link}")
            yield response.follow(link, callback=self.parse_page)

    def parse_page(self, response):
        # with open("drug_index.html", "w", encoding="utf-8") as outFile:
        #     outFile.write(response.text)

        products = response.css("div.style__product-card___1gbex")
        for product in products:
            drug_summary = self.get_drug_summary(product)
            yield drug_summary
            drug_link = f"https://www.1mg.com{drug_summary['page_link']}"
            print(f"Scraping detail link: {drug_link}")
            yield response.follow(drug_link, callback=self.parse_drug)

    def parse_drug(self, response):
        drug_item = DrugInfoItem()
        # with open("sample.html", "w", encoding="utf-8") as oFile:
        #     oFile.write(response.text)

        # get the drug headers
        name_of_drug = response.css("div#drug_header h1::text").get()
        drug_item["name"] = name_of_drug

        drug_headers = response.css("div#drug_header div.DrugHeader__meta___B3BcU")
        for drug_header in drug_headers:
            title = drug_header.css("div.DrugHeader__meta-title___22zXC::text").get()
            if title.lower() == "marketer":
                value = drug_header.css(
                    "div.DrugHeader__meta-value___vqYM0 a::text"
                ).get()
                drug_item["marketer"] = value
            elif title.lower() == "salt composition":
                value = drug_header.css(
                    "div.DrugHeader__meta-value___vqYM0 a::text"
                ).get()
                drug_item["salt_composition"] = value
            else:
                value = drug_header.css(
                    "div.DrugHeader__meta-value___vqYM0::text"
                ).get()
                drug_item["storage"] = value

        product_introduction = response.css(
            "div#overview div.DrugOverview__content___22ZBX::text"
        ).get()

        drug_item["product_introduction"] = product_introduction

        # time.sleep(30)
        yield drug_item

    def get_drug_summary(self, product):
        drug_summary = DrugSummaryItem()
        drug_summary["page_link"] = product.css("a::attr(href)").get()
        name_and_price = (
            product.css(
                "div.style__font-bold___1k9Dl.style__font-14px___YZZrf.style__flex-row___2AKyf.style__space-between___2mbvn.style__padding-bottom-5px___2NrDR"
            )
            .css("div::text")
            .getall()
        )

        drug_summary["name"] = name_and_price[0]
        drug_summary["price"] = name_and_price[-1]

        drug_summary["prescription_rqd_txt"] = product.css(
            "div.style__rx___3pKXG.style__font-12px___2ru_e>span::text"
        ).get()

        pkg_and_mfg = product.css(
            "div.style__flex-column___1zNVy.style__font-12px___2ru_e>div::text"
        ).getall()
        drug_summary["packaging_info"] = pkg_and_mfg[0]
        drug_summary["manufacturer"] = pkg_and_mfg[-1]

        drug_summary["content"] = product.css(
            "div.style__product-content___5PFBW::text"
        ).get()

        return drug_summary

    """
        # all alphabets
        chips = response.css("div.style__chips___2T95q>a")
        chips.css("a::attr(href)").getall()  # all links

        print(f"Number of drugs: {len(all_drugs)}")
    """
