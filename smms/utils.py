import os
from django.conf import settings

import matplotlib.pyplot as plt
from .models import Investment, TotalSalesPrice


def investment_pie():
    invest_value = Investment.objects.all()[0].price
    sale_value = TotalSalesPrice.objects.all()[0].price
    profit = sale_value - invest_value
    x = [invest_value, sale_value, profit]
    base, text = plt.pie(x, colors=['tomato', 'orange', 'red'], )
    plt.legend(['tomato', 'orange', 'red'], loc='best')
    path = os.path.join(settings.BASE_DIR, 'smms', 'static', 'pie.png')
    plt.savefig(path, bbox_inches='tight')
    pass


def monthly_sales_grap():
    pass


def weekly_sales_graph():
    pass
