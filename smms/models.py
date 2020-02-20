import os
from django.db import models
from django.db.models.signals import post_save


# Create your models here.
def path_to_images(filename, instance):
    return os.path.join('picture', str(instance), filename)


class TotalProduct(models.Model):
    """
        model for all the product in the super market
        It keep track of imported and sells goods, keeping
        record of total number of product per category and the
        grand total.
    """
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=200,
                                    null=True, blank=True)
    quantity = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.quantity}) ({self.price})'


class Product(models.Model):
    """models for product contained in the super market"""
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=200, null=True, blank=True)
    supplier = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    picture = models.ImageField(upload_to=path_to_images)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

    def get_product_image(self):
        no_picture = 'path to image'
        if self.picture.url:
            image = self.picture
        else:
            image = no_picture
        return image

    def total_product(self):
        pass


def add_to_total_product(sender, **kwargs):
    """
        signal function to add new product input to TotalProduct
        and if the already exits, increment the price and quantity
    """
    # print(kwargs)
    if kwargs['created']:  # check if product is created successfully
        name = kwargs['instance'].name  # get product name from instance
        category = kwargs['instance'].category  # same as above
        sub_category = kwargs['instance'].sub_category  # same as above
        quantity = kwargs['instance'].quantity  # same here
        price = kwargs['instance'].price  # get product price from instance
        try:  # catch error easily
            # check if product with product already exit in total product
            product = TotalProduct.objects.filter(name=name)
            # filter down to get product categories for secure query
            final_product = product.filter(category=category)
            if sub_category:  # check if product has sub_category
                final_product = final_product.get(sub_category=sub_category)
            else:  # if no sub_category, just pass
                pass
            final_product.quantity += quantity  # add quantity to existing quantity
            # add price to existing one but multiply with number of goods
            final_product.price += price * quantity
            # finally, save the record
            final_product.save()
            print('finally it worked')
        except ValueError:
            print('this is an error with this error message')
        except KeyError:
            print('A key error occured')
        except Exception:  # if error, usually no file matching query
            # create a new product in the TotalProduct and add the values
            new_product = TotalProduct.objects.create(name=name,
                                                      category=category, quantity=quantity,
                                                      sub_category=sub_category, price=price * quantity
                                                      )
            new_product.save()
            print('finish saving the new product in total product')
    print(kwargs)


# signal to add the imported record to existing one
post_save.connect(add_to_total_product, sender=Product)


class Sale(models.Model):
    """models for sale record"""
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=200,
                                    null=True, blank=True)
    supplier = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    picture = models.ImageField(upload_to=path_to_images,
                                null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} {self.quantity}'
