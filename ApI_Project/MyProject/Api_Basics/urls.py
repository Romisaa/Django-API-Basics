from django.db import router
from django.urls import path, include
from .views import article_list, article_detail,ArticleViewSet, ArticleAPIView, ArticleDtails, GenericAPIView
from rest_framework.routers import DefaultRouter



# To Use viewsets we must use router to define the routing or URL to the view we create
router = DefaultRouter()
router.register('article', ArticleViewSet, basename='article')




urlpatterns = [
    path('viewset/', include(router.urls)),
    path('viewset/<int:pk>', include(router.urls)),
    # path('article/', article_list),
    path('article/', ArticleAPIView.as_view()),
    # path('detail/<int:pk>/', article_detail),
    path('detail/<int:id>/', ArticleDtails.as_view()),
    path('generic/article/<int:id>/', GenericAPIView.as_view()),
]