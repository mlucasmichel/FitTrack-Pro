from django.contrib import admin
from .models import MealPlan, Meal, MealLog


class MealInline(admin.TabularInline):
    model = Meal
    extra = 1


@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    inlines = [MealInline]
    list_display = ('title', 'is_premium', 'created_at')
    list_filter = ('is_premium',)


@admin.register(MealLog)
class MealLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal', 'servings', 'total_calories', 'logged_at')
    list_filter = ('user', 'logged_at')
    readonly_fields = ('logged_at',)


admin.site.register(Meal)
