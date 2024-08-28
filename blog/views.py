from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Category
from .forms import PostForm

def home(request):
    recent_posts = Post.objects.order_by('-created_date')[:5]
    return render(request, 'blog/home.html', {'recent_posts': recent_posts})

def post_list(request):
    post_list = Post.objects.all().order_by('-created_date')
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# def post_detail(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     return render(request, 'blog/post_detail.html', {'post': post})

def my_view(request):
    data = {
        'title': 'My Page Title',
        'items': ['Item1', 'Item2', 'Item3']
    }
    return render(request, 'my_template.html', data)

@login_required
def post_create(request):
    if request.method == "POST": # Post요청 확인
        form = PostForm(request.POST) # PostFrom 인스턴스 생성 인자 전달
        if form.is_valid(): # 폼의 유효성
            post = form.save(commit=False) # Post객체 생성
            post.author = request.user  # 현재는 로그인 기능이 없으므로 나중에 구현
            post.save() #객체 저장
            return redirect('post_detail', pk=post.pk) # 새로 생성된 게시물의 상세 페이지로 리 디렉션 / post_detail URL 패턴에 새 게시물의 기본 키('pk')를 전달
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

# @login_required
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post) # 이미 데이터베이스에 저장된 게시물을 수정 instance = post 기존 Post객체를 폼에 제공
#         if post.author != request.user:
#             return redirect('post_detail', pk=pk)
    
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user  # 현재는 로그인 기능이 없으므로 나중에 구현
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if post.author != request.user:
                return redirect('post_detail', pk=pk)  # 작성자만 수정 가능
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('post_detail', pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category).order_by('-created_date')
    return render(request, 'blog/category_posts.html', {'category': category, 'posts': posts})
