# core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, MenuItemIngredient

@receiver(post_save, sender=Order)
def deduct_inventory(sender, instance, created, **kwargs):
    if instance.status == 'completed' and instance.paid and not instance.inventory_deducted:
        print(f"Signal fired for order {instance.id}")
        print(f"Order {instance.id} has {instance.items.count()} items")

        for item in instance.items.all():
            print(f"Processing item {item.menu_item.name} qty {item.quantity}")
            ingredients = MenuItemIngredient.objects.filter(menu_item=item.menu_item)
            if not ingredients.exists():
                continue
            for ing in ingredients:
                deduct_qty = ing.quantity * item.quantity
                ing.ingredient.quantity -= deduct_qty
                ing.ingredient.save()
        instance.inventory_deducted = True
        instance.save(update_fields=['inventory_deducted'])