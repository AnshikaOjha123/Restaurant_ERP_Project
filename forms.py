from django import forms
from django.forms import BaseInlineFormSet,inlineformset_factory
from .models import  Employee, MenuItem,MenuItemIngredient, Order, OrderItem, Inventory,Feedback

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['user_id', 'name', 'phone', 'address', 'role', 'salary', 'hire_date', 'shift']
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
from django import forms
from django.forms import inlineformset_factory
from .models import MenuItem, MenuItemIngredient, Inventory


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'category','image','available']

class MenuItemIngredientForm(forms.ModelForm):
    class Meta:
        model = MenuItemIngredient
        fields = ['ingredient', 'quantity']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from core.models import Inventory
        self.fields['ingredient'].queryset = Inventory.objects.all()
        
MenuItemIngredientFormSet = inlineformset_factory(
    MenuItem,
    MenuItemIngredient,
    form=MenuItemIngredientForm,
    extra=5,
    can_delete=True,
    fields=["ingredient","quantity"],
)   



class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'quantity', 'unit']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
        }



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer", "table", "status"]
        widgets = {
            "customer": forms.TextInput(attrs={"class": "form-control"}),
            "table": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }
        


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["menu_item", "quantity"]
        widgets = {
            "menu_item": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
        }


OrderItemFormSet = inlineformset_factory(Order,
                                         OrderItem,
                                         fields=["menu_item","quantity"],
                                         form=OrderItemForm, extra=5,can_delete=True)


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["feedback", "rating"]

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)

        feedback = self.instance  
        if feedback and feedback.order and feedback.order.status != "completed":
            for field in self.fields.values():
                field.disabled = True