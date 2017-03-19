from django.contrib import admin

from blog.models import Post, Category

admin.site.register(Post)

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):

    list_display = ("category_name", "category_short")
