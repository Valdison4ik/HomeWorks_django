from django.db import models


class CategoryModel(models.Model):
    """ Категория выполнения """
    title = models.CharField(max_length=100,
                             unique=True,
                             verbose_name='Category',
                             # db_comment='Название категории.'
                             )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'category'
        # db_table_comment = 'Категория выполнения.'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
