from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """Example for model Serializer"""

    class Meta:
        model = Article
        # fields = ['id', 'title', 'author']
        # If I want to get all the fields without writing it all ---> fields = '__all__'
        fields = '__all__'

    """This was an example for serializer usages but
    instead it's better to user model Serializer to keep the code more better"""
    # title = serializers.CharField(max_length=100)
    # author = serializers.CharField(max_length=100)
    # email = serializers.EmailField(max_length=100)
    # date = serializers.DateTimeField()
    #
    # # Define functions create and update
    # def create(self, validated_data):
    #     return Article.objects.create(validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.author = validated_data.get('author', instance.author)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.date = validated_data.get('date', instance.date)
    #     instance.save()
    #     return instance
