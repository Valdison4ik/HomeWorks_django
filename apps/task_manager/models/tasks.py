from django.db import models
from django.db.models.functions import TruncDate

from apps.base.models import TimeStamp1, Statuses
from .categories import CategoryModel


class TaskModel(TimeStamp1):
    """ Задача для выполнения """
    title = models.CharField(max_length=255,
                             # unique_for_date='created_at',
                             # db_comment='Название задачи.Уникально для даты.'
                             )
    description = models.TextField(verbose_name='Description',
                                   # db_comment='Описание задачи.'
                                   )
    # parent = models.ForeignKey('self',
    #                            on_delete=models.PROTECT,
    #                            null=True,
    #                            blank=True,
    #                            related_name='child_task',
    #                            verbose_name='task_id',
    #                            db_comment='Основная задача.')
    categories = models.ManyToManyField(CategoryModel,
                                        blank=True,
                                        related_name='tasks',
                                        verbose_name='Categories')
    status = models.CharField(default='new',
                              max_length=15,
                              choices=Statuses,
                              verbose_name='Status',
                              # db_comment='Статус задачи.Выбор из: New, In progress, Pending, Blocked, Done'
                              )
    deadline = models.DateTimeField(null=True,
                                    blank=True,
                                    verbose_name='Deadline',
                                    # db_comment='Дата и время дедлайн.'
                                    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task'
        # db_table_comment = 'Задача для выполнения.'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                TruncDate('created_at'), 'title',
                name='unique_title_in_date') ]
