from django.contrib import admin

# Register your models here.
from .models import  *
admin.site.register(Employee)
admin.site.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display=("number","capacity")
admin.site.register(Order)
admin.site.register(OrderItem)

admin.site.register(SalesReport)
class MenuItemIngredientInline(admin.TabularInline):
    model = MenuItemIngredient
    extra = 1

class MenuItemAdmin(admin.ModelAdmin):
    inlines = [MenuItemIngredientInline]

admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Inventory)

