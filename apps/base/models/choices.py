from django.db import models


class Statuses(models.TextChoices):
    NEW = 'new', 'New'
    IN_PROGRESS = 'in progress', 'In progress'
    PENDING = 'pending', 'Pending'
    BLOCKED = 'blocked', 'Blocked'
    DONE = 'done', 'Done'