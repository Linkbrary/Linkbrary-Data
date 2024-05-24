from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import subprocess
import json
import directory_gpt
import asyncio

app = FastAPI()

def run_spider_process(spider_name: str, link: str):
    process = subprocess.run(
        ['scrapy', 'crawl', spider_name, '-a', f'url={link}'],
        capture_output=True,
        text=True
    )
    if process.returncode != 0:
        raise Exception("Scrapy 스파이더 실행 중 오류 발생" + process.stderr)
    return process.stdout

@app.get("/crawl/{link:path}")
async def run_spider(link: str, background_tasks: BackgroundTasks):
    try:
        if "news.naver.com" in link:
            spider_name = "naverNews"
        elif "v.daum.net" in link:
            spider_name = "daumNews"
        elif "tistory.com" in link:
            spider_name = "tistory"
        elif "blog.naver.com" in link:
            spider_name = "naverBlog"
        elif "velog.io" in link:
            spider_name = "velog"
        else:
            raise ValueError("지원하지 않는 URL입니다.")

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, run_spider_process, spider_name, link)
        data = json.loads(data)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class DirectoryRequest(BaseModel):
    directory: str
    content: str

@app.post("/directory")
async def process_content(request: DirectoryRequest):
    try:
        gpt_response = directory_gpt.process_directory(request.directory, request.content)
        
        response_data = {
            "directory": gpt_response
        }
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)