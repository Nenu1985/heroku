from django.contrib import admin
from blog.models import Post, Comment

# Register your models here.

# admin.site.register(Post)  # the simpliest way

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish',
                    'status')
    list_filter = ('status', 'created', 'publish', 'author')

    search_fields = ('title', 'body')

    # auto complete slug field by title value
    prepopulated_fields = {'slug': ('title',)}

    # authors can be searched with lookup widget (lupa)
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
