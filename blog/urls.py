from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),  # 게시글 작성 URL 패턴 추가
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),  # 게시글 수정 URL 패턴 추가
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),  # 게시글 삭제 URL 패턴 추가
    path('category/<slug:category_slug>/', views.category_posts, name='category_posts'), # 변경된 부분

    # 또는 슬러그를 사용할 경우:
    # path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
]