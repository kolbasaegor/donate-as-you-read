from django.contrib import admin

from .models import *


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Article, ArticleAdmin)
admin.site.register(User, UserAdmin)
