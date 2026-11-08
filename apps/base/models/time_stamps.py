from django.db import models

class TimeStamp1(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Created at",
                                      # db_comment="Дата и время создания."
                                      )

    class Meta:
        abstract = True
