from django.db import models
from djongo import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from decimal import Decimal
from bson.decimal128 import Decimal128
 
class GenericDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    context_object_name = 'object'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = getattr(self.model, '__name__', 'Item')
        context['cancel_url'] = self.success_url
        return context


# ---------------- Employees ----------------
class Employee(models.Model):
    ROLES = [
        ('manager', 'Manager'),
        ('waiter', 'Waiter'),
        ('chef', 'Chef'),
        ('accountant','Accountant'),
        ('store keeper','Store Keeper')
        
    ]
    SHIFT_CHOICES = [
        ('morning', 'Morning'),
        ('evening', 'Evening'),
        ('night', 'Night'),
        
    ]
    user_id = models.IntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    role = models.CharField(max_length=50, choices=ROLES)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    hire_date = models.DateField(default=timezone.now)
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES)
class EmployeeDeleteView(GenericDeleteView):
    model = Employee
    success_url = reverse_lazy('employee_list')

  #---------Inventory-----------------
from bson import ObjectId
class Inventory(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.FloatField(default=0)  
    unit = models.CharField(max_length=50, blank=True, null=True)  
    threshold=models.FloatField(default=5)
    @property
    def is_low_stock(self):
        if self.threshold is None:
          return False   
        return self.quantity <= self.threshold
    def __str__(self):
        return self.name 
# ---------------- Menu ----------------
class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('starter', 'Starter'),
        ('main', 'Main Course'),
        ('beverage', 'Beverage'),
        ('dessert', 'Dessert'),
        ('fastfood', 'Fast Food'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ingredients=models.ManyToManyField(Inventory,through='MenuItemIngredient')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - ₹{self.price}"
    
class MenuItemIngredient(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE,related_name='menu_ingredients')
    ingredient = models.ForeignKey(Inventory,on_delete=models.CASCADE)
    quantity= models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.menu_item.name} uses {self.quantity} of {self.ingredient.name}"
    

class MenuDeleteView(GenericDeleteView):
    model = MenuItem
    success_url = reverse_lazy('menu_list')
    
# ---------------- Orders ----------------
class Table(models.Model):
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Table {self.number} ({self.capacity} seats)"
STATUS = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
class Order(models.Model):
    
    customer=models.CharField(max_length=50,null=True,blank=True)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    paid = models.BooleanField(default=False)
    inventory_deducted=models.BooleanField(default=False)
    def get_total_price(self):
        total = Decimal("0.00")
        for item in self.items.all():
            price = item.price or Decimal("0.00")
            if isinstance(price, Decimal128):
                price = price.to_decimal()
            total += price * item.quantity
        return total

    def update_total(self):
        self.total_price = self.get_total_price()
        self.save(update_fields=["total_price"])

    def save(self, *args, **kwargs):
        if isinstance(self.total_price, Decimal128):
            self.total_price = self.total_price.to_decimal()
        elif isinstance(self.total_price, str):
            self.total_price = Decimal(self.total_price)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Order {self.id} - {self.customer}"
    
    def can_deduct_inventory(self):
        return (self.status == 'completed' and 
                self.paid and 
                not self.inventory_deducted and 
                self.items.exists())
         
class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name="items", on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_prepared=models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if self.price is None and self.menu_item:
            self.price =Decimal(str( self.menu_item.price )) 
        super().save(*args, **kwargs)
        
    def get_cost(self):
        price = self.price
        if isinstance(price, Decimal128):   
            price = price.to_decimal()
        return (price or Decimal("0")) * self.quantity

    def __str__(self):
        return f"{self.menu_item.name} - {self.price} "


class OrderDeleteView(GenericDeleteView):
    model = Order
    success_url = reverse_lazy('order_list')
    #Feedback
class Feedback(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='feedbacks')
    feedback = models.TextField()
    rating = models.IntegerField(choices=[(i,i) for i in range(1,6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for Order #{self.order.id}"
    
# ---------------- Reports ----------------
class SalesReport(models.Model):
    date = models.DateField()
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    popular_dish = models.CharField(max_length=100, blank=True)