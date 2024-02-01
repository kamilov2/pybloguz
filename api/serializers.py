from rest_framework import serializers
from blog.models import Post, Tag, Category
from django.contrib.auth.models import User 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')  

    
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class HomePageSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    category = CategorySerializer()
    author = UserSerializer()
    image = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()  

    class Meta:
        model = Post
        fields = '__all__'

    def get_body(self, obj):
        if obj.body:
            return obj.body.to_delta()
        return None

    def get_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url) if obj.image else None

class PostDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    author = UserSerializer()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None