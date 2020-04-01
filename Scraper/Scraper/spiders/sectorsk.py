# -*- coding: utf-8 -*-
import scrapy
from ..items import ScraperItem
from datetime import datetime
from scrapy.exceptions import CloseSpider


class SectorskSpider(scrapy.Spider):
    name = 'sectorsk'
    allowed_domains = ['sector.sk']
    start_urls = ['https://www.sector.sk/novinky']
    base_url = 'https://www.sector.sk/'
    page_number = 0
    handle_httpstatus_list = [404]
    err_count = 0

    def parse(self, response):
        if response.status == 404:
            SectorskSpider.err_count +=1
            if SectorskSpider.err_count >= 5:
                raise CloseSpider('Too many 404 errors - spider closed.')
            return None
        else:
            SectorskSpider.err_count = 0

        all_article_urls = response.css('.lstbxmain')

        for item in all_article_urls:
            title = item.css('.overorang::text').extract_first().strip()
            comments_count_str = item.css('.rghdsc::text').extract_first()

            if comments_count_str is not None:
                comments_count = int(comments_count_str)
            else:
                comments_count = 0

            info_text = item.css('.newspridane::text').extract_first()
            description_data = item.css('.newslh::text').extract_first()

            if description_data is not None:
                description = description_data[:55].rsplit(' ', 1)[0] + '...' if len(description_data) > 55 \
                    else description_data + '...'

            if comments_count is None:
                comments_count = item.css('.lstfnic::text').extract_first()

            article_relative_url = item.css('.overorang::attr(href)').extract_first()
            article_url = self.base_url + str(article_relative_url) + ''

            yield scrapy.Request(article_url, callback=self.parse_article, meta={
                'article_title': title,
                'comments_count': comments_count,
                'info_text': info_text,
                'description': description
            })

    def parse_article(self, response):
        if response.status == 404:
            SectorskSpider.err_count +=1
            if SectorskSpider.err_count >= 5:
                raise CloseSpider('Too many 404 errors - spider closed.')
            return None
        else:
            SectorskSpider.err_count = 0

        items = ScraperItem()
        title = response.meta.get('article_title')
        author = response.xpath('//span[@class="mencolo"]/a/text()').extract_first()
        comments_count = response.meta.get('comments_count')
        info_text = response.meta.get('info_text')
        article_url = response.request.url
        description = response.meta.get('description')

        tags = response.css('.pltbs::text').extract()
        if len(tags) <= 1:
            tags += response.css('.pltbs a::text').extract()

        parag_data = response.xpath('//div[@class="newstextcolo newstextstyle"]/p/text()').extract_first()

        if parag_data is None:
            parag_data = response.xpath('//div[@class="newstextcolo clntxt"]/div/p/text()').extract_first()
            if parag_data is None:
                parag_data = " "

        parag = parag_data[:55].rsplit(' ', 1)[0] + '...' if len(parag_data) > 55 else parag_data + '...'

        paragraphs = [description, parag]

        if author is None:
            author = response.xpath('//span[@class="hry"]/a/text()').extract_first()

        now = datetime.now()
        dt_string = now.strftime("%d.%m.%Y")

        date = info_text.split()[1]

        if date == "dnes":
            date = dt_string

        if len(info_text) > 20:
            category = info_text.split()[3]
        else:
            category = "bez kategorie"

        items['article_title'] = title
        items['article_author'] = author
        items['article_url'] = article_url
        items['comments_count'] = comments_count
        items['published'] = date
        items['category'] = category
        items['paragraphs'] = paragraphs
        items['tags'] = tags

        yield items

        next_page = 'https://www.sector.sk/novinky?page=' + str(SectorskSpider.page_number) + ''
        pages_g = getattr(self,'pages')
        pages = int(pages_g)

        if SectorskSpider.page_number <= pages:
            SectorskSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
