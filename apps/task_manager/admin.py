
from django.contrib import admin
from apps.task_manager.models import TaskModel, SubTaskModel, CategoryModel


@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'status', 'deadline', 'created_at')


@admin.register(SubTaskModel)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'task', 'status', 'deadline', 'created_at')


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
