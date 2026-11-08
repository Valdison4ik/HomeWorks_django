from django.db import models

from apps.base.models import TimeStamp1, Statuses
from .tasks import TaskModel


class SubTaskModel(TimeStamp1):
    """ Отдельная часть основной задачи (Task) """
    title = models.CharField(max_length=255,
                             verbose_name='Title',
                             # db_comment='Название подзадачи.'
                             )
    description = models.TextField(verbose_name='Description',
                                   # db_comment='Описание подзадачи.'
                                   )
    task = models.ForeignKey(TaskModel,
                             on_delete=models.CASCADE,
                             related_name='sub_tasks',
                             verbose_name='Task',
                             # db_comment='Основная задача. Один ко многим.'
                             )
    status = models.CharField(default='new',
                              max_length=15,
                              choices=Statuses,
                              verbose_name='Status',
                              # db_comment='Статус подзадачи. Выбор из: New, In progress, Pending, Blocked, Done'
                              )
    deadline = models.DateTimeField(null=True,
                                    blank=True,
                                    verbose_name='Deadline',
                                    # db_comment='Дата и время дедлайн.'
                                    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'sub_task'
        # db_table_comment = 'Отдельная часть основной задачи (Task).'
        verbose_name = 'Subtask'
        verbose_name_plural = 'Subtasks'
