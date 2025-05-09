import openai
from openai import OpenAI
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DocumentEmbedding, RequestChatGPT
from .serializers import DocumentEmbeddingSerializer , RequestChatGPTSerializer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from rest_framework.exceptions import ParseError
from rest_framework import status
import numpy as np
import os
import requests
from dotenv import load_dotenv
from datetime import datetime

os.environ["TOKENIZERS_PARALLELISM"] = "false"

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def _save_infrastructure_data(request):
    try:
        response = requests.get('http://localhost:8000/infra/data/')

        response.raise_for_status()
        documents = response.json().get('documents', [])

        if not documents or documents == ["No data available."]:
            return Response({"error": "가져올 데이터가 없습니다."}, status=404)

        # 기존 데이터 삭제 (필요에 따라 삭제하지 않을 수도 있음)
        DocumentEmbedding.objects.all().delete()

        saved_docs = []

        # 첫 번째 문서를 query로 사용 (필요에 따라 수정)
        query = documents[0] if documents else ""

        for text in documents:
            vector = model.encode(text).tolist()  # 모델을 사용하여 문서 벡터화

            # name 필드 사용
            doc = DocumentEmbedding(name=text, embedding=vector)
            doc.save()
            saved_docs.append(doc)

        serializer = DocumentEmbeddingSerializer(saved_docs, many=True)
        return Response({"message": f"{len(documents)}개의 데이터 저장 성공", "data": serializer.data})
    except Exception as e:
        return Response({"error": f"데이터 저장 중 오류 발생: {str(e)}"}, status=500)


class SaveInfrastructureDataAPIView(APIView):
    """ /infrastructure/data/의 데이터를 DocumentEmbedding에 저장 """
    
    def get(self, request):
        return _save_infrastructure_data(request)

class ChatWithRagAPIView(APIView):
    """유사한 문서를 기반으로 ChatGPT에게 질문하여 응답 생성 (POST), 쿼리 처리 (GET)"""

    def _validate_query(self, query):
        """쿼리 유효성 검증"""
        if not query:
            return Response({"error": "질문을 입력하세요."}, status=400)
        return None

    def post(self, request):
        try:
            # 요청 본문을 직접 처리해서 query 추출
            query = request.body.decode('utf-8').strip()

            if not query:
                return Response({"error": "질문을 입력하세요."}, status=400)

            # 이후 기존 코드
            save_response = _save_infrastructure_data(request)
            if save_response.status_code != 200:
                return Response({"error": "문서 저장 실패. RAG 요청을 실행할 수 없습니다.", "details": save_response.data}, status=500)

            error_response = self._validate_query(query)
            if error_response:
                return error_response

            # 쿼리 벡터화
            query_vector = model.encode(query).reshape(1, -1)

            # 저장된 문서 가져오기
            all_embeddings = DocumentEmbedding.objects.all()
            if not all_embeddings.exists():
                return Response({"error": "저장된 문서가 없습니다."}, status=404)

            # 벡터 변환
            doc_vectors = np.array([np.array(doc.embedding) for doc in all_embeddings])

            # 유사도 계산
            similarities = cosine_similarity(doc_vectors, query_vector).flatten()
            best_idx = np.argmax(similarities)
            best_doc = all_embeddings[int(best_idx)]
            best_score = similarities[best_idx]

            # RAG 프롬프트 생성
            rag_prompt = f""" 
            초기 설정:

            문맥:
            {best_doc.name}

            질문:
            {query}

            위 문맥을 바탕으로 질문에 대한 답변을 정확하게 작성하세요.
            """

            # ChatGPT 호출
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 유능한 AI 비서입니다."},
                    {"role": "user", "content": rag_prompt}
                ],
            )

            chatgpt_response_text = response.choices[0].message.content

            RequestChatGPT.objects.create(
                query=query,
                response=chatgpt_response_text,
                similarity=best_score,
                created_at=datetime.now(),
            )

            return Response({
                "query": query,
                "response": best_doc.name,
                "chatgpt_response": chatgpt_response_text,
                "similarity": float(best_score)
            })

        except openai.OpenAIError as e:
            return Response({"error": f"OpenAI API 오류: {str(e)}"}, status=500)
        except Exception as e:
            return Response({"error": f"서버 오류: {str(e)}"}, status=500)

    def get(self, request):
        """GET 요청 처리: 쿼리를 받아 간단한 응답 반환"""
        try:
            query = request.query_params.get("query")
            error_response = self._validate_query(query)
            if error_response:
                return error_response

            return Response({
                "query": query,
                "response": "GET 요청에 대한 응답입니다."
            })

        except Exception as e:
            return Response({"error": f"서버 오류: {str(e)}"}, status=500)


class RequestChatGPTListAPIView(APIView):
    """
    저장된 ChatGPT 요청 결과 리스트 조회 (최근 순)
    """
    def get(self, request):
        try:
            requests_qs = RequestChatGPT.objects.all().order_by('-created_at')
            serializer = RequestChatGPTSerializer(requests_qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)