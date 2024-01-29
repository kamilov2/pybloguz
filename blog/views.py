import datetime
from typing import Any, Dict

from django.db.models.query import QuerySet
from django.db.models import Q, Max
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import View, TemplateView
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator

from .models import Post, Category
from .utils import set_reaction

# Create your views here.
PAGE_ITEMS_COUNT = 10

class HomePageView(ListView):
    model = Post
    paginate_by = PAGE_ITEMS_COUNT
    template_name = 'index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = Post.objects.filter(is_published=True, is_top=True).order_by('-id').prefetch_related(
            'tags','comments').select_related(
                'category')
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context




class MainPostsView(View):
    template_name = 'index.html'

    def get(self,request,*args, **kwargs):
        this_week = datetime.datetime.utcnow().isocalendar()[1]
        this_month = datetime.datetime.utcnow().month
        
        if kwargs.get("by_what") == 'reactions':

            posts = Post.objects.filter(is_published=True).order_by("-reaction_count").prefetch_related(
            'tags','comments').select_related(
                'category','author')
            pagination = Paginator(posts,PAGE_ITEMS_COUNT)
            page_number = request.GET.get("page")
            page_obj = pagination.get_page(page_number)
            data = {
                'page_obj':page_obj,
                "filter_title":"Obuna bo'lingan maqolalar"
            }
            return render(request, self.template_name,context=data)
        elif kwargs.get("by_what") == 'new':
            posts = Post.objects.filter(is_published=True).order_by('-id').prefetch_related(
            'tags').select_related(
                'category')
            pagination = Paginator(posts,PAGE_ITEMS_COUNT)
            page_number = request.GET.get("page")
            page_obj = pagination.get_page(page_number)
            data = {
                'page_obj':page_obj,
                "filter_title":"Yangi maqolalar"
            }
            return render(request, self.template_name,context=data)
        elif kwargs.get("by_what") == 'fire':
            posts = Post.objects.annotate(Max('reaction_count')).filter(is_published=True).prefetch_related(
            'tags',).select_related(
                'category')
            pagination = Paginator(posts,PAGE_ITEMS_COUNT)
            page_number = request.GET.get("page")
            page_obj = pagination.get_page(page_number)
            data = {
                'page_obj':page_obj,
                "filter_title":"Eng sara maqolalar !"
            }
            return render(request, self.template_name,context=data)
        elif kwargs.get("by_what") == 'top':
            posts = Post.objects.filter(is_published=True, is_top=True).order_by('-id').prefetch_related(
            'tags').select_related(
                'category')
            pagination = Paginator(posts,PAGE_ITEMS_COUNT)
            page_number = request.GET.get("page")
            page_obj = pagination.get_page(page_number)
            data = {
                'page_obj':page_obj,
                "filter_title":"TOP maqolalar !"
            }
            return render(request, self.template_name,context=data)
        elif kwargs.get("by_what") == 'week':
            posts = Post.objects.filter(is_published=True, published_date__week=this_week).order_by('-id').prefetch_related(
            'tags').select_related(
                'category')
            pagination = Paginator(posts,PAGE_ITEMS_COUNT)
            page_number = request.GET.get("page")
            page_obj = pagination.get_page(page_number)
            data = {
                'page_obj':page_obj,
                "filter_title":"Haftaning TOP maqolalari !"
            }
            return render(request, self.template_name,context=data)
        elif kwargs.get("by_what") == 'month':
            print(this_month)
            posts = Post.objects.filter(is_published=True, published_date__month=this_month).order_by('-id').prefetch_related(
            'tags').select_related(
                'category')
            pagination = Paginator(posts,PAGE_ITEMS_COUNT)
            page_number = request.GET.get("page")
            page_obj = pagination.get_page(page_number)
            data = {
                'page_obj':page_obj,
                "filter_title":"Oyning TOP maqolalari !"
            }
            return render(request, self.template_name,context=data)
        elif kwargs.get("by_what") == 'everytime':
            posts = Post.objects.filter(is_published=True,is_top=True).order_by('-views').prefetch_related(
            'tags').select_related(
                'category')
            print(posts)
            # for i in posts:
            #     print(i)
            pagination = Paginator(posts,PAGE_ITEMS_COUNT)
            page_number = request.GET.get("page")
            page_obj = pagination.get_page(page_number)
            data = {
                'page_obj':page_obj,
                "filter_title":"Doim TOP bo'lgan maqolalar !"
            }
            return render(request, self.template_name,context=data)
        return render(request, self.template_name,context=data)

    
    

class CategoryListView(ListView):
    model = Post
    paginate_by = PAGE_ITEMS_COUNT
    template_name = 'tag_cat_detail.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = Post.objects.filter(category__slug=self.kwargs.get("slug")).prefetch_related(
            'tags').select_related(
                'category')
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["obj_name"] = self.kwargs.get('slug')
        context["category_pk"] =  Category.objects.get(slug=self.kwargs.get("slug")).id
        return context   
    
class TagListView(ListView):
    model = Post
    paginate_by = PAGE_ITEMS_COUNT
    template_name = 'tag_cat_detail.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = Post.objects.filter(tag__slug=self.kwargs.get("slug")).prefetch_related(
            'tags','comments').select_related('category')
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["obj_name"] = self.kwargs.get('slug')
        return context   
    
    
    def get_queryset(self, *args, **kwargs):
        qs = Post.objects.filter(category__title__icontains=self.kwargs.get('slug'))
        return qs

def get_view_list(obj,request):
    request.session.modified = True   
    post_id = obj.id 
    try:
        viewed_posts = request.session["view_list"]
    except:
        viewed_posts = request.session["view_list"] = []
    
    
    if post_id not in viewed_posts:
        viewed_posts.extend([post_id])
        obj.views += 1
        obj.save()
        print(viewed_posts)
    else:       
        pass

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["most_read"] = Post.objects.filter(is_published=True).order_by('-views').order_by("?")[:3]
        context["related_posts"] = Post.objects.filter(
            category=self.object.category, 
            is_published=True,
        ).prefetch_related('tags').select_related('category').order_by('-id').exclude(pk=self.object.pk)[:3]
        get_view_list(self.object,self.request)
        return context


# def set_comment(request, post_id):
#     if request.user.is_authenticated:        
#         if request.method == "POST":
#             post = Post.objects.get(pk=post_id)
#             Comment.objects.create(
#                 text=request.POST.get('text'),
#                 user=request.user,
#                 full_name=request.POST.get("full_name"),
#                 post=post
#             )
#             post.comments_count += 1
#             post.save()
#             messages.add_message(request, messages.SUCCESS, "Qabul qildik !")
#             return redirect('blog:post_detail', slug=post.slug)
#     else:
#         messages.add_message(request, messages.ERROR, "Faqat ro'yhatdan o'tgan foydalanuvchilar fikr bildira oladi !")
#         return redirect('blog:post_detail', slug=post.slug)
        



def post_reaction_view(request):
    post_id = request.GET.get("post_id")
    react = request.GET.get("react")
    post_obj = Post.objects.get(id=post_id)
    wtf = set_reaction(request,post_obj,react)
    data = {
        'status':200,
        "wtf":wtf
    }
    return JsonResponse(data)

# def to_saved_posts_view(request):  
#     post = Post.objects.get(id=int(request.GET.get("post_id")))
#     if request.user.is_authenticated:
        
#         if request.user not in post.saved.all():
#             post.saved.add(request.user)
#             data = {
#                 'status':200,
#                 'wtf':"Maqola saqlanganlarga qo'shildi !"
#             }
#         else:
#             post.saved.remove(request.user)
#             data = {
#                 'status':400,
#                 'wtf':"Maqola saqlanganlardan olindi !"
#             } 
#     else:
#         data = {
#             'status':404,
#             'wtf':"Reaksiya bildirish uchun ro'yhatdan o'ting yoki kiring !"
#         }       

#     return JsonResponse(data)


def inline_search(request):
    q = request.GET.get("query")
    if len(q) > 3:
        posts = Post.objects.filter(is_published=True).filter(
            Q(title__icontains=q)
         )
        return JsonResponse({'data':list(posts.values())})
        
    else:
        pass
    
    return JsonResponse({'status':200})


class ContactView(TemplateView):
    template_name = 'contact.html'
    
def myhandler404(request,exception=None):
    return render(request,template_name="404.html")
    
    
    
    
    
    
    
    
    
    
