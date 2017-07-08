from django.contrib import admin
from django.conf.urls import url, include
# Register your models here.
from .models import *

__author__ = 'TheArchitect'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'date_created', 'date_updated')
    list_filter = ('owner__username',)
    search_fields = ('id', )
    ordering = ("-date_created",)

admin.site.register(Category, CategoryAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'completed', 'sort_weight', 'date_created', 'date_updated')
    search_fields = ('id',)
    list_filter = ('category__owner__username',)
    ordering = ("-date_created",)

admin.site.register(Task, TaskAdmin)