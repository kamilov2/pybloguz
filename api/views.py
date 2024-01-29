import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.utils import timezone
from blog.models import Post, Category, Tag
from .serializers import HomePageSerializer, PostDetailSerializer, TagSerializer, CategorySerializer


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5  
    page_size_query_param = 'page_size'
    max_page_size = 1000


class HomePageAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    serializer_class = HomePageSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return Post.objects.filter(is_published=True, is_top=True).order_by('-id').prefetch_related(
            'tags', 'comments').select_related('category', 'author')

    def list(self, request):
        queryset = self.get_queryset()
        tags = Tag.objects.all()  
        categories = Category.objects.all()  

        serializer = self.get_serializer(queryset, many=True)
        tags_serializer = TagSerializer(tags, many=True)  
        categories_serializer = CategorySerializer(categories, many=True)  

        paginated_data = self.paginate_queryset(serializer.data)
        response_data = {
            'posts': paginated_data,
            'tags': tags_serializer.data,
            'categories': categories_serializer.data
        }

        return self.get_paginated_response(response_data)

class PostDetailAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def get(self, request, format=None):
        post_id = request.query_params.get('id')

        try:
            post_id = int(post_id)
        except ValueError:
            return Response({'error': 'Invalid id parameter'}, status=status.HTTP_400_BAD_REQUEST)

        post = get_object_or_404(
            Post.objects.select_related('category', 'author')
                        .prefetch_related('tags'),
            pk=post_id, is_published=True
        )

        serializer = PostDetailSerializer(post, context={'request': request})
        this_week = datetime.datetime.utcnow().isocalendar()[1]

        top_post_ids = Post.objects.filter(is_published=True, published_date__week=this_week).order_by('-id').select_related(
                'category', 'author').prefetch_related(
            'tags')
        top_posts_serializer = PostDetailSerializer(top_post_ids, many=True, context={'request': request})

        related_post_ids = Post.objects.filter(
            category=post.category, 
            is_published=True,
        ).select_related('category', 'author').prefetch_related('tags').order_by('-id').exclude(pk=post_id)[:3]
        

        related_serializer = PostDetailSerializer(related_post_ids, many=True, context={'request': request})

        serialized_data = serializer.data
        serialized_data['related_posts'] = related_serializer.data
        serialized_data['top_posts'] = top_posts_serializer.data

        return Response(serialized_data, status=status.HTTP_200_OK)


