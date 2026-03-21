from django.urls import path
from . import views

urlpatterns = [
    path('exercises/', views.exercise_list, name='exercise_list'),
    path('exercises/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
    path('log/', views.log_workout, name='log_workout'),
    path('log/<int:plan_id>/', views.log_workout, name='log_workout_plan'),
    path('routines/', views.routines_list, name='routines'),
    path('routines/create/', views.create_routine, name='create_routine'),
    path('routines/<int:routine_id>/edit/', views.edit_routine, name='edit_routine'),
    path('routines/<int:routine_id>/delete/', views.delete_routine, name='delete_routine'),
]
