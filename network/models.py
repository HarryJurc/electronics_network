from django.db import models


class Product(models.Model):
    """
    Модель продукта.
    """
    name = models.CharField(max_length=255, verbose_name="Название")
    model = models.CharField(max_length=255, verbose_name="Модель")
    release_date = models.DateField(verbose_name="Дата выхода на рынок")

    def __str__(self):
        return f"{self.name} {self.model}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class NetworkLink(models.Model):
    """
    Модель звена сети по продаже электроники.
    """
    LEVEL_CHOICES = [
        (0, 'Завод'),
        (1, 'Розничная сеть'),
        (2, 'Индивидуальный предприниматель'),
    ]

    level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name="Уровень иерархии")
    name = models.CharField(max_length=255, verbose_name="Название")

    # Контакты
    email = models.EmailField(unique=True, verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=20, verbose_name="Номер дома")

    # Продукты и поставщик
    products = models.ManyToManyField(Product, related_name="network_links", verbose_name="Продукты")
    supplier = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="traders", verbose_name="Поставщик")

    debt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Задолженность")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return f"{self.get_level_display()}: {self.name} ({self.city})"

    def save(self, *args, **kwargs):
        # Завод не может иметь поставщика
        if self.level == 0:
            self.supplier = None
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"
