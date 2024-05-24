from pathlib import Path
import re
import json
import scrapy
from gpt_process import process_new_data
from doc2vec import embed_text


class NaverBlogSpider(scrapy.Spider):
    name = "naverBlog"
    handle_httpstatus_list = [404]

    def __init__(self, url=None, do_summary=None, *args, **kwargs):
        super(NaverBlogSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url] if url else []
        self.do_summary = True if do_summary == 'true' else False

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # iframe src 추출
        iframe_src = response.xpath('//iframe[@id="mainFrame"]/@src').extract_first()
        full_url = response.urljoin(iframe_src)  # 상대 URL을 절대 URL로 변환
        yield scrapy.Request(full_url, callback=self.parse_iframe)

    def parse_iframe(self, response):
        # iframe 내부에서 필요한 데이터 추출
        new_contents = []
        title = response.xpath('//title/text()').get()
        image = response.xpath('//meta[@property="og:image"]/@content').get()
        contents = response.xpath('//div[@class="se_component_wrap"]//text()').extract()
        if not contents:
            contents = response.xpath('//div[@class="se-main-container"]//text()').extract()
        if not contents:
            contents = response.xpath('//div[@id="postViewArea"]//text()').extract()

        for text in contents:
            text = text.strip()
            text = re.sub(r'\[.*?\]', '', text)
            if text:
                new_contents.append(text)

        content_all = ' '.join([content for content in new_contents if content])
        
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
        

"""
    def parse(self, response):
        title = response.css('title::text').get()
        all_contents = []

        selectors = [
            'div.se_component_wrap ::text',
            'div.se-main-container ::text',
            'div#postViewArea ::text'
        ]

        for selector in selectors:
            contents = response.css(selector).getall()
            cleaned_content = [text.strip() for text in contents if text.strip()]

            if cleaned_content:
                all_contents.extend(cleaned_content)

        image = response.css("meta[property='og:image']::attr(content)").get()
        new_contents = []

        for text in contents:
            text = text.strip()
            text = re.sub(r'\[.*?\]', '', text)
            if text:
                new_contents.append(text)

        content_all = ' '.join([content for content in new_contents if content])
        summary = process_new_data(new_contents)
        embed = embed_text(new_contents)

        data = {
            "title": title,
            "content": content_all,
            "summary": summary,
            "thumbnail": image,
            "embed": embed.tolist()  # 768line
        }
        print(json.dumps(data))"""