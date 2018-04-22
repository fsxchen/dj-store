from django.db import models

# Create your models here.
class GoodsCategory(models.Model):
    """
    商品类别
    """
    name = models.CharField()
    code = models.CharField()
    desc = models.CharField()
    category_type = models.CharField(choices=(()))
    category_image = models.CharField()

    """
    05:min
    """
