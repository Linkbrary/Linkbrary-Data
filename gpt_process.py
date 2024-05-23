import openai
from openai import OpenAIError
import warnings
from transformers import GPT2Tokenizer
import os
import tiktoken

warnings.simplefilter(action='ignore', category=FutureWarning)

openai.api_key = ''
tokenizer = tiktoken.get_encoding("cl100k_base")
tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
MAX_TOKEN_LENGTH = 3800

question = '''
당신의 임무는 주어진 글을 분석하여 정해진 형식으로 출력하는 것입니다.  
입력된 글을 분석하여, 한 줄당 20글자 이하로, 총 3줄을 출력해야합니다. 
요약 내용은 "~하다"와 같이 단정적인 문장으로 작성해야 합니다.
정해진 형식은 다음과 같습니다.

1. (첫번째 요약 내용)
2. (두번째 요약 내용)
3. (세번째 요약 내용)

이 때, 3줄을 반드시 채워야 합니다. 반드시 한줄당 20글자 이하여야 합니다.
요약 내용이 20글자를 초과하면, 20글자보다 적은 형태로 바꿔서 출력해야 합니다. 이 때, 바꾼 형태는 반드시 문법적으로 완전한 문장이어야 합니다.
요약 이후, 요약된 내용이 전부 한글 문법적으로 올바른 문장인지 확인하세요. 명사로 끝나거나, "다, 한다"등의 형태로 끝나야 합니다.
완전한 문장이 아니라면 다시 작성하세요.

글은 다음과 같습니다 :

'''


def process_new_data(contents):
    content_all = ''
    content_all = ' '.join([content for content in contents if content])

    results = []
    text_data = question + content_all
    tokens = tokenizer.encode(text_data)

    if len(tokens) > MAX_TOKEN_LENGTH:
        tokens = tokens[:MAX_TOKEN_LENGTH - 1]  # 마지막 토큰을 위한 자리를 남김
        text_data = tokenizer.decode(tokens)

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-0125',
        max_tokens=300,
        messages=[{"role": "user", "content": text_data}]
    )    

    chat_response = response.choices[0].message.content

    results.append({
        'output': chat_response
    })

    return chat_response
