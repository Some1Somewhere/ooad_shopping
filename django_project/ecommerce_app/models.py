from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=191)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    clicks = models.IntegerField(default=0)
    recommended = models.ForeignKey("Product", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    cart_id = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    

    def __str__(self):
        return "{}:{}".format(self.product.name, self.id)

    def update_quantity(self, quantity):
        self.quantity = self.quantity + quantity
        self.save()

    def total_cost(self):
        return self.quantity * self.price


class Order(models.Model):
    name = models.CharField(max_length=191)
    email = models.EmailField()
    postal_code = models.IntegerField()
    address = models.CharField(max_length=191)
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return "{}:{}".format(self.id, self.email)

    def total_cost(self):
        return sum([ li.cost() for li in self.lineitem_set.all() ] )


