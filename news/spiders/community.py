from pathlib import Path
import re
import json
import scrapy
from gpt_process import process_new_data
from doc2vec import embed_text

class CommunitySpider(scrapy.Spider):
    name = "community"
    handle_httpstatus_list = [404]

    def __init__(self, url=None, do_summary=None, *args, **kwargs):
        super(CommunitySpider, self).__init__(*args, **kwargs)
        self.start_urls = [url] if url else []
        self.do_summary = True if do_summary == 'true' else False

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        contents = ''
        title = response.css('title::text').get()

        if "clien.net" in response.url:
            content = response.css('div.post_content ::text').getall()
            contents = ''.join(content)
            contents = re.sub(r'[\n\t\xa0]+', ' ', contents).strip()
        elif "dcinside.com" in response.url:
            content = response.xpath('//div[@class="write_div"]/div//text()').getall()
            contents = ''.join(content)
        elif "fmkorea.com" in response.url:
            content = response.xpath('//div[contains(@class, "xe_content")]/text()').getall()
            contents = ''.join(content)
        elif "ruliweb.com" in response.url:
            content = response.xpath('//div[@class="view_content autolink"]//text()').getall()
            contents = ''.join(content)
        elif "inven.co.kr" in response.url:
            content = response.xpath('//div[@class="articleContent"]//text()').getall()
            contents = ''.join(content)
            if "INVEN" in contents:
                contents = contents.split("INVEN")[0].strip ()
        elif "pann.nate.com" in response.url:
            content = response.xpath('//div[@id="contentArea"]//text()').getall()
            contents = ''.join(content)
        elif "theqoo.net" in response.url:
            content = response.xpath('//div[contains(@class, "rhymix_content xe_content")]//text()').getall()
            contents = ''.join(content)
        else:
            content = response.css('p::text').getall()
            contents = ''.join(content)
        


        image = response.css("meta[property='og:image']::attr(content)").get()
        new_contents = []
    
        for text in contents:
            text = text.strip()
            text = re.sub(r'\[.*?\]', '', text)
            if text:
                new_contents.append(text)

        content_all = ' '.join([content for content in new_contents if content])

        print(title)
        print(content_all)
        print(image)

        """if self.do_summary:
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
        print(json.dumps(data))"""