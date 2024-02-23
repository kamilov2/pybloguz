import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Max
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from blog.models import Post, Category, Tag
from .serializers import HomePageSerializer, PostDetailSerializer, TagSerializer, CategorySerializer
from drf_yasg.utils import swagger_auto_schema




class CategoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()

    def get_serializer_context(self):
        return {'category': self.request}
    
class TagListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.all()

    def get_serializer_context(self):
        return {'tag': self.request}


class FirstCategoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()[:5]

    def get_serializer_context(self):
        return {'category': self.request}
    
class LastCategoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()[5:]

    def get_serializer_context(self):
        return {'category': self.request}
    



class HomePageAPIView(generics.ListAPIView):
    """
    Домашняя страница API предоставляет список публикаций на главной странице.
    
    **Permissions:**
    - `IsAuthenticated`: Доступ к данному эндпоинту разрешен для всех.

    **Authentication:**
    - `JWTAuthentication`: Требуется JWT-аутентификация для доступа к этому эндпоинту.

    **Query Params:**
    - `page` (optional, int): Номер страницы для пагинации.

    **Responses:**
    - `200 OK`: Успешный ответ. Возвращает список публикаций на главной странице.
    """
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    serializer_class = HomePageSerializer
    
    @swagger_auto_schema(
        operation_summary="Сводка эндпоинта",
        operation_description="Подробное описание того, что делает этот эндпоинт",
        responses={200: "Успешный ответ"},
    )
    def get_queryset(self):
        """
        Возвращает список опубликованных и лучших публикаций, отсортированных по убыванию идентификатора.
        """
        return Post.objects.filter(is_published=True, is_top=True).order_by('-id').prefetch_related(
            'tags', 'comments').select_related('category', 'author')

    def list(self, request):
        """
        Список опубликованных и лучших публикаций на главной странице.

        Принимает параметр 'page' для пагинации результатов.

        Возвращает список публикаций на главной странице, пагинированный в соответствии с параметром 'page'.
        """
        page = self.request.query_params.get('page', 1)
        queryset = self.get_queryset()
     

        serializer = self.serializer_class(queryset, many=True, context={'request': request})

        paginated_data = self.paginate_queryset(serializer.data)

        paginator = Paginator(queryset, self.paginator.page_size)
        total_pages = paginator.num_pages

        response_data = {         
            'posts': paginated_data,
            'current_page': int(page),
            'total_pages': total_pages
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

        response_data = {
            'post': serializer.data,
            'related_posts': related_serializer.data,
            'top_posts': top_posts_serializer.data
        }


        return Response(response_data, status=status.HTTP_200_OK)

class FilterListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    serializer_class = HomePageSerializer

    def get_queryset(self):
        category_id, tag_id = (
            self.request.query_params.get('category_id', None),
            self.request.query_params.get('tag_id', None)
        )

        try:
            if category_id:
                queryset = Post.objects.filter(is_published=True, category=category_id).select_related('category', 'author').prefetch_related('tags').order_by('-id')
                category = Category.objects.filter(id=category_id).first()
                return queryset, category.title if category else None, queryset.count()
            elif tag_id:
                queryset = Post.objects.filter(is_published=True, tags=tag_id).select_related('category', 'author').prefetch_related('tags').order_by('-id')
                tag = Tag.objects.filter(id=tag_id).first()
                return queryset, tag.title if tag else None, queryset.count()
        except Exception as e:
            print(f"Error in get_queryset: {e}")

        return Post.objects.none(), None, 0

    def list(self, request):
        try:
            queryset, title, post_count = self.get_queryset()
            tags = Tag.objects.all()
            categories = Category.objects.all()

            if queryset is not None and len(queryset) > 0:
                serializer = self.get_serializer(queryset, many=True, context={'request': request})

                paginated_data = self.paginator.paginate_queryset(serializer.data, self.request)
                response_data = {
                    'next_page': self.paginator.get_next_link(),
                    'previous_page': self.paginator.get_previous_link(),
                    # 'tags': TagSerializer(tags, many=True).data,
                    # 'categories': CategorySerializer(categories, many=True).data,
                    'posts': paginated_data,
                    'title': title,
                    'post_count': post_count,
                    'page_count': self.paginator.page.paginator.num_pages,
                    'current_page': self.paginator.page.number,
                }

       
                return Response(response_data)
            else:
                response_data = {
                    'message': 'Hozircha maqolalar mavjud emas!',
                    'title': title,
                    'post_count': post_count,
                    'page_count': 0,
                    'current_page': 1
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error in list: {e}")
            return Response({'message': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        

class FilterTopListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    serializer_class = HomePageSerializer

    def get_queryset(self):

        this_week = datetime.datetime.utcnow().isocalendar()[1]
        this_month = datetime.datetime.utcnow().month

        top_filters = {
            'reactions': Post.objects.filter(is_published=True).order_by("-reaction_count").prefetch_related(
                'tags', 'comments').select_related('category', 'author'),
            'new': Post.objects.filter(is_published=True).order_by('-id').prefetch_related('tags').select_related(
                'category'),
            'fire': Post.objects.annotate(Max('reaction_count')).filter(is_published=True).prefetch_related('tags').select_related(
                'category'),
            'top': Post.objects.filter(is_published=True, is_top=True).order_by('-id').prefetch_related('tags').select_related(
                'category'),
            'week': Post.objects.filter(is_published=True, published_date__week=this_week).order_by('-id').prefetch_related(
                'tags').select_related('category'),
            'month': Post.objects.filter(is_published=True, published_date__month=this_month).order_by('-id').prefetch_related(
                'tags').select_related('category'),
            'everytime': Post.objects.filter(is_published=True, is_top=True).order_by('-views').prefetch_related('tags').select_related(
                'category'),
        }

        top_filter = self.request.query_params.get('filter', None)

        return top_filters.get(top_filter, Post.objects.none())

       
    def list(self, request):
        try:
            queryset = self.get_queryset()
            tags = Tag.objects.all()
            categories = Category.objects.all()
            
            if not queryset.exists():
                response_data = {
                    'message': 'Hozircha maqolalar mavjud emas!',
                    'page_count': 0,
                    'current_page': 1
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)

            paginated_queryset = self.paginate_queryset(queryset)
            serializer = self.get_serializer(paginated_queryset, many=True, context={'request': request})

            response_data = {
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
                'tags': TagSerializer(tags, many=True).data,
                'categories': CategorySerializer(categories, many=True).data,
                'posts': serializer.data,
                'page_count': self.paginator.page.paginator.num_pages,
                'current_page': self.paginator.page.number,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error in list: {e}")
            return Response({'message': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@staff_member_required
def site_uml(request):
    figma_url = "https://www.figma.com/file/k2aH8QNpHu4iQ4jfcV3zoq/Pyblog?type=whiteboard&node-id=0%3A1&t=71s6njWXZHExk7t7-1"
    return HttpResponseRedirect(figma_url)
