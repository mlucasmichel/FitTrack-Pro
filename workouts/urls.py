from django.urls import path
from . import views

urlpatterns = [
    path('exercises/', views.exercise_list, name='exercise_list'),
    path('exercises/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
    path('log/', views.log_workout, name='log_workout'),
    path('log/<int:plan_id>/', views.log_workout, name='log_workout_plan'),
]