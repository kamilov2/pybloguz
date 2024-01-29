from django.urls import re_path, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    HomePageAPIView, PostDetailAPIView,
    FilterListView, FilterTopListView
    )

urlpatterns = [
    re_path(r'^home/$', HomePageAPIView.as_view(), name="home"),
    re_path(r'^filter/$', FilterListView.as_view(), name='filter'),
    re_path(r'^post/$', PostDetailAPIView.as_view(), name="post"),
    re_path(r'^filter_top/$', FilterTopListView.as_view(), name='filter_top'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]