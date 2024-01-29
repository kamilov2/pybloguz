from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path("post/<slug>", views.PostDetailView.as_view(), name='post_detail'),
    
    path('filter/<str:by_what>', views.MainPostsView.as_view(), name='filter_by_something'),
    
    path("category/<slug>", views.CategoryListView.as_view(), name='category_list'),
    path("tag/<slug>", views.TagListView.as_view(), name='tag_list'),
    
    
    path('react/', views.post_reaction_view, name='post_react'),
    # Follows
    
    
    path('search/', views.inline_search, name='search'), 
    path('contact/', views.ContactView.as_view(), name='contact'),
]
