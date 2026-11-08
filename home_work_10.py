import os
# import logging
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# sql_logger = logging.getLogger('django.db.backends')
# sql_logger.setLevel(logging.DEBUG)
# sql_logger.addHandler(logging.StreamHandler())

from datetime import timedelta
from django.utils import timezone
from django.db.models import F
from apps.task_manager.models import TaskModel, SubTaskModel


"""
    Создание записей:
    Task:
        title: "Prepare presentation".
        description: "Prepare materials and slides for the presentation".
        status: "New".
        deadline: Today's date + 3 days.

"""
task = TaskModel(title='Prepare presentation',
                 description='Prepare materials and slides for the presentation',
                 status='new',
                 deadline=timezone.now() + timedelta(days=3))
task.save()

print(f' id:{task.id}\n title:{task.title}\n description:{task.description}\n '
          f'status:{task.status}\n deadline:{task.deadline}\n created_at:{task.created_at}')

task_101 = TaskModel.objects.create(title='Prepare presentation_1',
                 description='Prepare materials and slides for the presentation',
                 # status='new', # значение по умолчанию
                 deadline=timezone.now() + timedelta(days=3))

"""
Создание записей:
SubTasks для "Prepare presentation":
        title: "Gather information".
            description: "Find necessary information for the presentation".
            status: "New".
            deadline: Today's date + 2 days.
        title: "Create slides".
            description: "Create presentation slides".
            status: "New".
            deadline: Today's date + 1 day.
"""
task = TaskModel.objects.get(title='Prepare presentation')

sub_task_list = [SubTaskModel(title='Gather information',
                              description='Find necessary information for the presentation',
                              task=task,
                              status='new',
                              deadline=timezone.now() + timedelta(days=2)),
                 SubTaskModel(title='Create slides',
                              description='Create presentation slides',
                              task=task,
                              status='new',
                              deadline=timezone.now() + timedelta(days=1))
                 ]
for sub_task in sub_task_list:
    sub_task.save()

print(f'Создано записей:{len(sub_task_list)}')
for sub_task in sub_task_list:
    print(f'{sub_task.id} - {sub_task.title} - {sub_task.description} - {sub_task.task} - {sub_task.status} - {sub_task.deadline}')

"""
Чтение записей:
Tasks со статусом "New":
        Вывести все задачи, у которых статус "New".
"""

new_tasks_list = TaskModel.objects.filter(status='new')

for task in new_tasks_list:
    print(f' id:{task.id}\n title:{task.title}\n description:{task.description}\n '
          f'status:{task.status}\n deadline:{task.deadline}\n created_at:{task.created_at}')
    print('*' * 50)

"""
Чтение записей:
SubTasks с просроченным статусом "Done":
        Вывести все подзадачи, у которых статус "Done", но срок выполнения истек.
"""

done_sub_tasks_list = SubTaskModel.objects.filter(status='done', deadline__lt=timezone.now())

for sub_task in done_sub_tasks_list:
    print(f'{sub_task.id} - {sub_task.title} - {sub_task.status} - {sub_task.deadline}')

"""
Изменение записей:
    Измените статус "Prepare presentation" на "In progress".
"""

updated_task = TaskModel.objects.filter(title='Prepare presentation')
print(f'Найдено записей:{updated_task.count()}')
for task in updated_task:
    print(f'{task.id} - {task.title} - {task.status}')

updated_task.update(status='in progress')

for task in updated_task:
    print(f'{task.id} - {task.title} - {task.status}')


"""
Изменение записей:
    Измените срок выполнения для "Gather information" на два дня назад.
"""
sub_task_u1 = SubTaskModel.objects.filter(title='Gather information')

print(f'Найдено записей:{sub_task_u1.count()}')
for sub_task in sub_task_u1:
    print(f'{sub_task.id} - {sub_task.title} - {sub_task.deadline}')

sub_task_u1.update(deadline=F('deadline') - timedelta(days=2))
for sub_task in sub_task_u1:
    print(f'{sub_task.id} - {sub_task.title} - {sub_task.deadline}')

"""
Изменение записей:
    Измените описание для "Create slides" на "Create and format presentation slides".
"""

sub_task_u2 = SubTaskModel.objects.filter(title='Create slides')

print(f'Найдено записей:{sub_task_u2.count()}')
for sub_task in sub_task_u2:
    print(f'{sub_task.id} - {sub_task.title} - {sub_task.description}')

sub_task_u2.update(description='Create and format presentation slides')
for sub_task in sub_task_u2:
    print(f'{sub_task.id} - {sub_task.title} - {sub_task.description}')


"""
Удаление записей:
    Удалите задачу "Prepare presentation" и все ее подзадачи.
"""
print(*sub_task_u2)

# нахожу записи с указанным названием
task_for_delete = TaskModel.objects.filter(title='Prepare presentation')
print(f'Найдено записей:{task_for_delete.count()}')
for task in task_for_delete:
    print(f' {task.id} - {task.title} - {task.created_at}')

# сохраняю ид найденных задач
task_id_list = [t.id for t in task_for_delete]
# print(task_id_list)

# ищу подзадачи по сохраненным ИД задач - до удаления быть должны
sub_tasks_for_delete = SubTaskModel.objects.filter(task__id__in=task_id_list)
print(f'Найдено связанных записей:{sub_tasks_for_delete.count()}')
for sub_task in sub_tasks_for_delete:
    print(f'{sub_task.id} - {sub_task.title} - {sub_task.deadline}')

# удаляю найденные задачи
task_for_delete.delete() # on_delete=models.CASCADE
print(*task_for_delete)

# ищу подзадачи по сохраненным ИД задач - должно быть пусто
sub_tasks_for_delete = SubTaskModel.objects.filter(task__id__in=task_id_list)
print(f'Найдено связанных записей:{sub_tasks_for_delete.count()}')
for sub_task in sub_tasks_for_delete:
    print(f'{sub_task.id} - {sub_task.title} - {sub_task.deadline}')
