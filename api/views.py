import openai
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DocumentEmbedding
from .serializers import DocumentEmbeddingSerializer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
import requests

# 모델 로드
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# class SaveEmbeddingAPIView(APIView):
#     """사용자가 입력한 텍스트를 벡터화하여 DB에 저장"""
#     def post(self, request):
#         text = request.data.get("text")
#         if not text:
#             return Response({"error": "텍스트를 입력하세요."}, status=400)
#         try:
#             vector = model.encode(text).tolist()
#             doc = DocumentEmbedding(text=text, embedding=vector)
#             doc.save()  # SQLite DB에 저장
#             serializer = DocumentEmbeddingSerializer(doc)
#             return Response({"message": "저장 성공", "data": serializer.data})
#         except Exception as e:
#             return Response({"error": f"벡터 저장 중 오류 발생: {str(e)}"}, status=500)

class SaveInfrastructureDataAPIView(APIView):
    """ /infrastructure/data/의 데이터를 DocumentEmbedding에 저장 """
    
    def get(self, request):
        return self._save_infrastructure_data(request)

    def _save_infrastructure_data(self, request):
        try:
            response = requests.get('http://localhost:8000/infrastructure/data/')
            
            print(response.json())  # 디버깅 출력
           
            response.raise_for_status()
            documents = response.json().get('documents', [])
            
            if not documents or documents == ["No data available."]:
                return Response({"error": "가져올 데이터가 없습니다."}, status=404)

            DocumentEmbedding.objects.all().delete()

            saved_docs = []

            for text in documents:
                vector = model.encode(text).tolist()
                doc = DocumentEmbedding(text=text, embedding=vector)
                doc.save()
                saved_docs.append(doc)
    

            serializer = DocumentEmbeddingSerializer(saved_docs, many=True)
            return Response({"message": f"{len(documents)}개의 데이터 저장 성공", "data": serializer.data})
        except Exception as e:
            return Response({"error": f"데이터 저장 중 오류 발생: {str(e)}"}, status=500)


class ChatWithRagAPIView(APIView):
    """유사한 문서를 기반으로 ChatGPT에게 질문하여 응답 생성"""
    def post(self, request):
        query = request.data.get("query")
        if not query:
            return Response({"error": "질문을 입력하세요."}, status=400)
        try:
            query_vector = np.array(model.encode(query)).reshape(1, -1)
            all_docs = DocumentEmbedding.objects.all()
            if not all_docs.exists():
                return Response({"error": "저장된 문서가 없습니다."}, status=404)

            doc_vectors = np.array([doc.embedding for doc in all_docs])
            similarities = cosine_similarity(doc_vectors, query_vector).flatten()
            best_idx = np.argmax(similarities)
            best_doc = all_docs[best_idx]
            best_score = similarities[best_idx]

           
            rag_prompt = f"""
            문맥:
            {best_doc.text}

            질문:
            {query}

            위 문맥을 바탕으로 질문에 대한 답변을 간결하고 정확하게 작성하세요.
            """
            chat_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "당신은 유능한 AI 비서입니다."},
                    {"role": "user", "content": rag_prompt}
                ],
                temperature=0.7
            )
            
            return Response({
                "query": query,
                "context": best_doc.text,
                "chatgpt_response": chat_response["choices"][0]["message"]["content"],
                "similarity": float(best_score)
            })
        
        except Exception as e:
            return Response({"error": f"ChatGPT API 호출 중 오류 발생: {str(e)}"}, status=500) 