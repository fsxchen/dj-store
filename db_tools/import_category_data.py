import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

import django
django.setup()

from goods.models import GoodsCategory

from db_tools.data.category_data import row_data

for leve1_cat in row_data:
    leve1_intance = GoodsCategory()
    leve1_intance.code = leve1_cat["code"]
    leve1_intance.name = leve1_cat["name"]
    leve1_intance.category_type = 1
    leve1_intance.save()
    for leve2_cat in leve1_cat["sub_categorys"]:
        leve2_intance = GoodsCategory()
        leve2_intance.code = leve2_cat["code"]
        leve2_intance.name = leve2_cat["name"]
        leve2_intance.category_type = 2
        leve2_intance.parent_category = leve1_intance
        leve2_intance.save()

        for leve3_cat in leve2_cat["sub_categorys"]:
            leve3_intance = GoodsCategory()
            leve3_intance.code = leve3_cat["code"]
            leve3_intance.name = leve3_cat["name"]
            leve3_intance.category_type = 3
            leve3_intance.parent_category = leve1_intance
            leve3_intance.save()