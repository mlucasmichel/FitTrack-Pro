from django.contrib import admin
from .models import Exercise, WorkoutPlan, PlanItem, WorkoutLog, SetLog


class PlanItemInline(admin.TabularInline):
    model = PlanItem
    extra = 1


class SetLogInline(admin.TabularInline):
    model = SetLog
    extra = 0


@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    inlines = [PlanItemInline]
    list_display = ('title', 'is_premium', 'created_at')


@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    inlines = [SetLogInline]
    list_display = ('user', 'workout_plan', 'logged_at')
    list_filter = ('user', 'logged_at')


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'body_part', 'target_muscle', 'equipment')
    list_filter = ('body_part', 'target_muscle', 'equipment')
    search_fields = ('name',)


admin.site.register(SetLog)
