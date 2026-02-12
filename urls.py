from django.urls import path
from . import views

urlpatterns =[
 # Employees
    path("employees/", views.employee_list, name="employee_list"),
    path("employees/new/", views.employee_create, name="employee_create"),
    path("employees/<int:pk>/edit/", views.edit_employee, name="edit_employee"),
    path("employees/<int:pk>/delete/", views.delete_employee, name="delete_employee"),
  
#Inventory
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/new/', views.inventory_create, name='inventory_create'),
    path('inventory/<int:pk>/edit/', views.inventory_edit, name='inventory_edit'),
    path('inventory/<int:pk>/delete/', views.inventory_delete, name='inventory_delete'),

    # Menu
    path("menu/", views.menu_list, name="menu_list"),
    path("menu/new/", views.menu_create, name="menu_create"),
    path("menu/<int:pk>/edit/", views.edit_menu, name="edit_menu"),
    path("menu/<int:pk>/delete/", views.delete_menu, name="delete_menu"),

    # Orders
    path("orders/", views.order_list, name="order_list"),
    path("orders/new/", views.order_create, name="order_create"),
    path("orders/<int:pk>/edit/", views.order_edit, name="order_edit"),
    path("orders/<int:pk>/delete/", views.order_delete, name="order_delete"),
    path("orders/<int:pk>/", views.order_detail, name="order_detail"),
    path("orders/<int:pk>/paid/", views.order_mark_paid, name="order_mark_paid"),
    #Bill
    path("orders/<int:pk>/bill/", views.order_bill, name="order_bill"),
    #feedback
    path('order/<int:order_id>/feedback/', views.add_feedback, name='add_feedback'),
    #kitchen
    path('kitchen/', views.kitchen_dashboard, name='kitchen_dashboard'),
    path('kitchen/update/<str:order_id>/', views.update_order_status, name='update_order_status'),
   path('kitchen/orders-list/', views.kitchen_orders_list, name='kitchen_orders_list'), 
    #Reports
    path("reports/", views.reports_dashboard, name="reports_dashboard"),
   ]
