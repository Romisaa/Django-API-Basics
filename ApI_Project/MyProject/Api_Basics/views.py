from cgitb import lookup
import imp
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import Article
from .serializer import ArticleSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404


# Class ViewSet Based, It doesn't use get or post method but use retrive or update methods
"""We used generic viewset, but we will modify the class to use Modelviewset"""

class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()



    """Comment this code beacuse we will use generic viewset"""
    # def list(self, request):  #To List data
    #     articles = Article.objects.all()
    #     serializer = ArticleSerializer(articles, many=True)
    #     return Response(serializer.data)

    # def create(self, request):  #instead of using post
    #     serializer = ArticleSerializer(data=request.data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def retrieve(self, request, pk=None):   #instead of Update
    #     queryset = Article.objects.all()
    #     article = get_object_or_404(queryset, pk=pk)
    #     serializer = ArticleSerializer(article)
    #     return Response(serializer.data)

    # def update(self, request, pk=None): #instead of PUT
    #     article = Article.objects.all()
    #     serializer = ArticleSerializer(article, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        
 

        






# Class Generic and Mixin
class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, 
mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    
    # first thing to do is to identify serializer class
    serializer_class = ArticleSerializer
    
    # Second define queryset
    queryset = Article.objects.all()

    lookup_field = 'id'  #require for put function
    
    # authentication_classes = [SessionAuthentication, BasicAuthentication]  #Calling authentication class, it will search for session auth if not found will search for Basic one

    authentication_classes = [TokenAuthentication]
    
    permission_classes = [IsAuthenticated]


    # def your functions to make mixin list your request
    def get(self, request, id=None):    #this for listing or get the data
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):   #this is for creating new data
        return self.create(request)   

    def put(self, request, id=None):    #for updating  
        return self.update(request, id) 

    def delete(self, request):
        return self.destroy(request)



# Class Based View API
class ArticleAPIView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDtails(APIView):
    def get_object(self,id):
        try:
            return Article.objects.get(id=id)

        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        article = self.get_object(id=id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)




    def put(self, request,id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,id):
        article = self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# Function Based View API

@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)  # many=true because i have many articles to serialzer
        return Response(serializer.data)

    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)

    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ArticleSerializer(article ,data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



