from django.urls import path
from news.views import NewsAPIView,TemporaryLinkView,TemporaryLinkCreateView

urlpatterns = [
    path("news/", NewsAPIView.as_view(), name="news-api"),
    path("news/<int:pk>/", NewsAPIView.as_view(), name="news-api-detail"),
    path('link/<str:token>/', TemporaryLinkView.as_view(), name='temporary_link_view'),
    path('link/', TemporaryLinkCreateView.as_view(), name='temporary_link_create'),
]
