"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from blog import views
from blog.views import PostDetailView, HomeView, PostViewSet, login_api, profile_api
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from rest_framework.routers import DefaultRouter




router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', HomeView.as_view(), name='home'),
    path('about/', views.about),
    path('contact/', views.contact),
    path('add/', views.add_post, name='add_post'),
    path('edit/<slug:slug>/', views.edit_post, name= 'edit_post'),
    path('delete/<slug:slug>/', views.delete_post, name='delete_post'),
    path('add_tag/', views.add_tag, name='add_tag'),
    # path('add_author/', views.add_author, name='add_author'),
    # path('author/<int:author_id>/', views.posts_by_author, name='posts_by_author'),
    path("post/<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
    path("ajax/search/", views.ajax_search, name="ajax_search"),
    path("ajax/comment/", views.ajax_comment, name="ajax_comment"),
    path('accounts/', include('django.contrib.auth.urls')),
    path("comment/add/", views.add_comment, name="add_comment"),
    # path('api/posts/', post_list_api),
    # path('api/posts/create/', post_create_api),
    # path('api/posts/<int:pk>/', post_detail_update_delete_api),
    

]
urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
   
    path("api/profile/", profile_api),
]

urlpatterns += [
    path('api/', include(router.urls)),
]
