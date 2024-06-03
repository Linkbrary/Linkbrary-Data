import torch
from torch.nn import CosineSimilarity
from transformers import BertModel, BertTokenizer
from torch.nn.functional import normalize
import openai

"""# Load tokenizer and model
tokenizer = BertTokenizer.from_pretrained('monologg/kobert')
model = BertModel.from_pretrained('monologg/kobert')
model.eval()  # Set the model to evaluation mode"""

openai.api_key=""


def embed_text(texts):
       text_all = ' '.join([text for text in texts if text])
       model = "text-embedding-3-large"
       response = openai.Embedding.create(input = [text_all], model = model)
       embeded_text = response['data'][0]['embedding']
       return embeded_text

       """text_all = ' '.join([text for text in texts if text])
       tokens = tokenizer(text_all, return_tensors="pt", max_length=512, truncation=True, padding="max_length")

       with torch.no_grad():
              outputs = model(**tokens)

       cls_embedding = outputs.last_hidden_state[:, 0, :]
       normalized_embeddings = normalize(cls_embedding, p=2, dim=1)  # L2 정규화 적용

       return normalized_embeddings"""


"""def embed_test(text):
       print(text)
       tokens = tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
       with torch.no_grad():
              outputs = model(**tokens)

       cls_embedding = outputs.last_hidden_state[:, 0, :]

       print(cls_embedding)

       return cls_embedding
       

def test_embeding(embeddings, tests):
       test_all = ' '.join([test for test in tests if test])
       testText2 = "복합쇼핑몰 건립, 백화점 확장 이전 등 대규모 도심 개발이 이뤄지는 광주 광천동, 임동 일대 도시철도 신설 추진이 본격화했다." \
                   "용역 등을 통해 사업 계획이 구체화하면 광주시와 정부의 공식 협의도 이뤄질 것으로 보인다.12일 광주시에 따르면 시는 이른바" \
                   " 광천선 신설안을 담은 도시철도망 구축 계획 용역을 진행하고 있다.5년 주기로 수립하는 10개년 계획이다.특히 서구 광천동, " \
                   "북구 임동 일대 교통 대안으로 떠오른 도시철도 청사진이 주목받고 있다.광주시는 용역 결과를 토대로 오는 7월께 국토교통부에" \
                   " 계획안을 제출할 방침이다.노선은 상무역, 시청, 기아 오토랜드, 터미널, 전방·일신방직 부지, KIA 챔피언스 필드 인근, 광주역" \
                   " 등을 잇는 7.8㎞ 구간이 거론된다.광주시는 6천억원가량 사업비가 필요할 것으로 추산하고 교통 수요가 많은 '황금 라인'인 만큼" \
                   " 비용 대비 편익(B/C) 등 경제성을 충족할 수 있을 것으로 분석했다.이 일대는 교통·유통·여가 시설이 몰려있어 이미 극심한 " \
                   "혼잡이 빚어지는 데다가 대규모 개발사업들도 예정돼 교통 대책 마련이 시급한 곳이다.현재 운영 중인 도시철도 1호선, 건설 " \
                   "중인 2호선에서도 배제돼 타당성도 갖췄다고 광주시는 주장했다.광천동에서는 광주신세계가 금호고속으로부터 유스퀘어문화관," \
                   " 종합버스터미널 부지를 사들여 기존 백화점보다 3배 이상 큰 '광주 신세계 아트 앤 컬처파크' 건립을 추진하고 있으며 수천 " \
                   "가구 규모 재개발 사업도 진행 중이다.임동에서는 프로야구가 열리는 날마다 차량 정체가 반복되고 '더현대 광주'와 4천여 가" \
                   "구 공동주택 등이 들어설 옛 전방·일신방직 공장 부지 개발도 추진된다.각종 개발사업 완공 시기와 시차를 줄이고자 시 내부에" \
                   "서는 2030년 도시철도 개통을 목표로 설정한 것으로 전해졌다.광주시는 사업비 60%가량을 국비로 지원받고 방직공장 부지 용도" \
                   " 변경을 대가로 민간 사업자로부터 받기로 한 공공기여금, 신세계백화점 확장 과정에서 발생할 수 있는 공공기여금 등으로 나머지" \
                   " 예산을 마련할 계획이다.윤석열 대통령이 재개 방침을 밝힌 민생토론회가 광주에서 열리게 되면 핵심 의제 중 하나로 논의될 " \
                   "것으로 보인다.윤 대통령이 대선 후보 시절부터 지역 공약으로 복합쇼핑몰을 제시한 만큼 예비 타당성 조사, 사업비 마련 등 " \
                   "과정에서 지원을 광주시는 기대하고 있다."
       testText3 = "프로축구 K리그1 전북현대는 온라인 게임에서 활동할 선수를 뽑는 'eK리그 서포터즈컵' 선발전을 오는 24∼25일 전주월드컵경" \
                   "기장에서 개최한다고 12일 밝혔다.14세 이상의 축구 팬이면 오는 15일까지 구단 인스타그램으로 참가 신청하면 된다.선발전은 " \
                   "1 대 1 토너먼트 방식으로 32강전부터 치른다. 여기에서 선발된 선수 2명(1ㆍ2위)과 예비선수 1명(3위)은 한국프로축구연맹과 " \
                   "넥슨이 6∼7월 주최하는 'eK리그 서포터즈컵 2024' 본선 참가 자격을 갖는다.구단 관계자는 \"전북현대 팬과 응원단, 순수"\
                   "아마추어가 참가해 필드가 아닌 온라인 게임에서 활동할 전북현대 대표선수를 뽑는 대회\"라며 많은 참가를 요청했다."

       embedding1 = embed_text(test_all)
       embedding2 = embed_text(testText2)
       embedding3 = embed_text(testText3)

       cos = CosineSimilarity(dim=1)
       similarity1 = cos(embeddings, embedding1)
       similarity2 = cos(embeddings, embedding2)
       similarity3 = cos(embeddings, embedding3)

       print(f"1의 유사도: {similarity1.item()}")
       print(f"2의 유사도: {similarity2.item()}")
       print(f"3의 유사도: {similarity3.item()}")

def test_title(text):
       testText1 = "신공항 광역급행철도, 정부 예타 대상 선정"
       testText2 = "대구~경북 광역철도 등 6개 예타 대상사업 선정"
       testText3 = "의대 6곳 아직 개강 못 해…대학들 '학년제 전환'엔 미온적"

       embedding1 = embed_text(testText1)
       embedding2 = embed_text(testText2)
       embedding3 = embed_text(testText3)

       cos = CosineSimilarity(dim=1)
       similarity1 = cos(text, embedding1)
       similarity2 = cos(text, embedding2)
       similarity3 = cos(text, embedding3)

       print(f"1의 유사도: {similarity1.item()}")
       print(f"2의 유사도: {similarity2.item()}")
       print(f"3의 유사도: {similarity3.item()}")
"""
