from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from news.models import News
from news.serializers import NewsSerializer
from django.utils import timezone
import random
import string


class NewsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class NewsAPIView(APIView):
    permission_classes = []
    authentication_classes = []
    pagination_class = NewsPagination  # Adicione esta linha

    def get(self, request, pk=None) -> Response:
        paginator = self.pagination_class()  # Instancie o paginador
        if pk:
            news = News.objects.get(pk=pk)
            serializer = NewsSerializer(news, many=False)
            return Response(serializer.data)
        else:
            news = News.objects.all()
            result_page = paginator.paginate_queryset(news, request)
            serializer = NewsSerializer(result_page , many=True)

            return paginator.get_paginated_response(serializer.data)
            

    def post(self, request) -> Response:
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            news_article = News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = NewsSerializer(news_article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            news_article = News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        news_article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TemporaryLinkCreateView(APIView):
    def post(self, request):
        print(request.data)
        news_id = request.data.get('id')
        news = News.objects.get(pk=news_id)

        # Gera um token aleatório de 12 caracteres
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

        # Adiciona o token e a data de expiração ao objeto News
        news.temporary_link_token = token
        news.temporary_link_expiration = timezone.now() + timezone.timedelta(hours=1)
        news.save()

        return Response({'link': f'/api/link/{token}/'})

class TemporaryLinkView(APIView):
    def get(self, request, token):
        try:
            news = News.objects.get(temporary_link_token=token, temporary_link_expiration__gte=timezone.now())
            serializer = NewsSerializer(news)
            return Response(serializer.data)
        except News.DoesNotExist:
            return Response({'error': 'Link expirado ou inválido.'}, status=400)