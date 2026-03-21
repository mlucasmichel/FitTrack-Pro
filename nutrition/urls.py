from django.urls import path
from . import views

urlpatterns = [
    path('', views.nutrition_hub, name='nutrition_hub'),
    path('meal/<int:meal_id>/edit/', views.edit_custom_meal, name='edit_custom_meal'),
    path('meal/<int:meal_id>/delete/', views.delete_custom_meal, name='delete_custom_meal'),
    path('plan/<int:plan_id>/', views.meal_plan_detail, name='meal_plan_detail'),
]
