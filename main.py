from fastapi import FastAPI, HTTPException
import subprocess
import json

app = FastAPI()


@app.get("/crawl/{link:path}")
async def run_spider(link: str):
    try:
        if "news.naver.com" in link:
            spider_name = "naverNews"
        elif "v.daum.net" in link:
            spider_name = "daumNews"
        elif "tistory.com" in link:
            spider_name = "tistory"
        elif "blog.naver.com" in link:
            spider_name = "naverBlog"
        else:
            raise ValueError("지원하지 않는 URL입니다.")

        # Scrapy 스파이더 실행
        process = subprocess.run(
            ['scrapy', 'crawl', spider_name, '-a', f'url={link}'],
            capture_output=True,
            text=True
        )

        if process.returncode != 0:
            raise Exception("Scrapy 스파이더 실행 중 오류 발생" + process.stderr)
        data = json.loads(process.stdout)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)