from django.db import models

class Product(models.Model):
    name = models.CharField("Нименование товара", max_length=100)
    description = models.CharField("Описание", max_length=100)
    price = models.PositiveBigIntegerField("Цена", default=0)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        
    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)


class Order(models.Model):
    title = models.CharField("Номер счета", max_length=100)
    product_to_pay = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.PROTECT)
    amount = models.PositiveBigIntegerField("Количество", default=0)
    state = models.BooleanField("Оплачен", default=False)

    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "Счета"
    
    def __str__(self):
        return self.title
