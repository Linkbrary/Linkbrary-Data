from pathlib import Path
import re
import json
import scrapy
from gpt_process import process_new_data
from doc2vec import embed_text

class VelogSpider(scrapy.Spider):
    name = "velog"
    handle_httpstatus_list = [404]

    def __init__(self, url=None, do_summary=None, *args, **kwargs):
        super(VelogSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url] if url else []
        self.do_summary = True if do_summary == 'true' else False

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        elements = response.xpath('//h1 | //h2 | //h3 | //p')
        contents = []

        for element in elements:
            tag = element.root.tag
            text = ''.join(element.xpath('.//text()').getall())
            contents.append(f"<{tag}>{text}</{tag}>")
        
        title = response.css('title::text').get()
        image = response.css("meta[property='og:image']::attr(content)").get()
        new_contents = []
    
        for text in contents:
            text = text.strip()
            text = re.sub(r'\[.*?\]', '', text)
            if text:
                new_contents.append(text)

        content_all = ' '.join([content for content in new_contents if content])
        clean = re.compile('<.*?>')
        content_all = re.sub(clean,'',content_all)

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
                "embed": embed
            }
        else:
            data = {
                "embed": embed
            }
        print(json.dumps(data))
        