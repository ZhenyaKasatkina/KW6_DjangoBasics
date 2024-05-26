from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    """
    Блог
    """
    title = models.CharField(max_length=150, verbose_name="заголовок")
    content = models.TextField(verbose_name="содержимое", **NULLABLE)
    preview = models.ImageField(upload_to="preview/", verbose_name="превью", **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name="просмотры")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата публикации (записи в БД)")

    def __str__(self):
        # Строковое отображение объекта
        return f"{self.title} (количество просмотров: {self.views_count}): {self.content}."

    class Meta:
        verbose_name = "блог"  # Настройка для наименования одного объекта
        verbose_name_plural = "блоги"  # Настройка для наименования набора объектов
