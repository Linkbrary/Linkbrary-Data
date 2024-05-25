from pathlib import Path
import re
import json
import scrapy
from gpt_process import process_new_data
from doc2vec import embed_text


class NewsSpider(scrapy.Spider):
    name = "news"
    handle_httpstatus_list = [404]

    def __init__(self, url=None, do_summary=None, *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url] if url else []
        self.do_summary = True if do_summary == 'true' else False

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        contents = ''
        title = response.css('title::text').get()

        """if "chosun.com" in response.url:
            content = response.xpath('//div[@id="news_body_id"]//text()').getall()
            contents = ''.join(content)"""
        if "joongang.co.kr" in response.url:
            content = response.xpath('//div[@id="article_body"]//text()').getall()
            contents = ''.join(content)
            if "관련기사" in contents:
                contents = contents.split("관련기사")[0].strip ()
        elif "donga.com" in response.url:
            content = response.xpath('//section[@class="news_view"]//text()').getall()
            contents = ''.join(content)
            pattern = r'googletag.*?;'
            contents = re.sub(pattern, '', contents)
        #elif "hani.co.kr" in response.url:
            #content = response.css('p.text::text').getall()
            #contents = ''.join(content)
        elif "hankyung.com" in response.url:
            content = response.css('div#articletxt::text').getall()
            contents = ''.join(content)
        elif "mk.co.kr" in response.url:
            content = response.css('div.news_cnt_detail_wrap p::text').getall()
            contents = ''.join(content)
        elif "sedaily.com" in response.url:
            content = response.css('div.article::text').getall()
            contents = ''.join(content)
        elif "yna.co.kr" in response.url:
            content = response.css('.story-news.article p::text').getall()
            contents = ''.join(content)
            contents = re.sub(r'\b\S*\.kr\S*\b', '', contents)
            contents = re.sub(r'\s+', ' ', contents).strip()
        elif "news1.kr" in response.url:
            content = response.css('div#articles_detail::text').getall()
            contents = ''.join(content)
        elif "news.mt.co.kr" in response.url:
            content = response.xpath('//div[@id="textBody"]//text()').getall()
            contents = ''.join(content)
        elif "biz.heraldcorp.com" in response.url:
            content = response.xpath('//*[@id="articleText"]//text()').getall()
            contents = ''.join(content)
        elif "edaily.co.kr" in response.url:
            content = response.xpath('//*[@class="article_body"]//text()').getall()
            contents = ''.join(content)
        elif "seoul.co.kr/news" in response.url:
            content = response.xpath('//div[@class="viewContent body18 color700"]//text()').getall()
            contents = ''.join(content)
            pattern = r'googletag.*?;'
            contents = re.sub(pattern, '', contents)
        elif "hankookilbo.com" in response.url:
            content = response.xpath('//div[@class="col-main" and @itemprop="articleBody"]//p[@class="editor-p"]//text()').getall()
            contents = ''.join(content)
        elif "asiatoday.co.kr" in response.url:
            content = response.xpath('//div[@class="news_bm" and @id="font"]//text()').getall()
            contents = ''.join(content)
        elif "segye.com" in response.url:
            content = response.xpath('//div[@id="contents" and @class="article_read"]//text()').getall()
            contents = ''.join(content)
        else:
            content = response.css('p::text').getall()
            contents = ''.join(content)

        image = response.css("meta[property='og:image']::attr(content)").get()
        new_contents = []

        for text in contents.split():
            text = text.strip()
            text = re.sub(r'\[.*?\]', '', text)
            if text:
                new_contents.append(text)

        content_all = ' '.join(new_contents)
        
        if self.do_summary:
            summary = process_new_data(new_contents)
        else :
            summary = None
        
        embed = embed_text(new_contents)
        
        if self.do_summary:
            data = {
                "title": title,
                "content": content_all,
                "summary": summary,
                "thumbnail": image,
                "embed": embed.tolist()  # 768line
            }
        else:
            data = {
                "embed": embed.tolist()
            }
        print(json.dumps(data))