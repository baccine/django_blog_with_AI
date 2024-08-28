from django.contrib import admin
from .models import Post, Category

# 인라인 모델 정의
class PostInline(admin.TabularInline):
    model = Post
    extra = 1

# 커스텀 액션 정의
def make_published(modeladmin, request, queryset):
    queryset.update(status='published')
make_published.short_description = "Mark selected posts as published"

# Post 모델을 위한 ModelAdmin 클래스
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'modified_date', 'category')
    list_filter = ('created_date', 'category')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_date'
    ordering = ('-created_date',)
    actions = [make_published]

# Category 모델을 위한 ModelAdmin 클래스
class CategoryAdmin(admin.ModelAdmin):
    inlines = [PostInline]

# 모델 등록
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)