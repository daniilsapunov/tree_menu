from django.db import models


class MenuItem(models.Model):
    name: str = models.CharField(max_length=77)
    url: str = models.CharField(max_length=200)
    parent: 'MenuItem' = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    menu_name: str = models.CharField(max_length=50, db_index=True)
    order: int = models.IntegerField(default=0)

    class Meta:
        ordering = ('order', 'name')

    def __str__(self) -> str:
        return self.name
