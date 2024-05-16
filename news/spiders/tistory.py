from pathlib import Path
import re
import json
import scrapy
from gpt_process import process_new_data
from doc2vec import embed_text


class TistorySpider(scrapy.Spider):
    name = "tistory"
    handle_httpstatus_list = [404]

    def __init__(self, url=None, *args, **kwargs):
        super(TistorySpider, self).__init__(*args, **kwargs)
        self.start_urls = [url] if url else []

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.css('title::text').get()
        all_contents = []
        selectors = [
            'div.contents_style p::text',
            'div.entry-content ::text',
            'div.article_view ::text',
            'article ::text'
        ]

        for selector in selectors:
            contents = response.css(selector).getall()
            cleaned_content = [text.strip() for text in contents if text.strip()]

            if cleaned_content:
                all_contents.extend(cleaned_content)

        image = response.css("meta[property='og:image']::attr(content)").get()
        new_contents = []

        for text in all_contents:
            text = text.strip()
            text = re.sub(r'\[.*?\]', '', text)
            text = text.replace('\xa0', '')
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
        print(json.dumps(data))