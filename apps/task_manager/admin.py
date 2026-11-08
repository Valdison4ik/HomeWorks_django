from django.contrib import admin
from django.template.defaultfilters import truncatechars
from apps.task_manager.models import TaskModel, SubTaskModel, CategoryModel


class SubTaskInline(admin.TabularInline):
    model = SubTaskModel
    extra = 1  # Количество пустых форм для подзадач, отображаемых по умолчанию
    # fk_name = 'task'


@admin.action(description="Set status to 'Done'")
def make_status_done(modeladmin, request, queryset):
    for obj in queryset:
        obj.status = 'done'
        obj.save()


@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'description', 'status', 'deadline', 'created_at')
    # Подключаем инлайн-форму подзадач к основной форме задачи
    inlines = [SubTaskInline]
    actions = [make_status_done]

    @admin.display(description='Title')
    def short_title(self, obj):
        # truncatechars добавляет троеточие в конец, итоговая длина будет ровно 10 символов
        return truncatechars(obj.title, 10)


@admin.register(SubTaskModel)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'task', 'status', 'deadline', 'created_at')
    actions = [make_status_done]


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
