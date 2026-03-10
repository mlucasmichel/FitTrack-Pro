from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings


class Exercise(models.Model):
    """
    Exercise library populated via RapidAPI (ExerciseDB).
    """
    api_id = models.CharField(
        max_length=50, unique=True, help_text="Unique ID from ExerciseDB API")
    name = models.CharField(max_length=200)
    body_part = models.CharField(max_length=100, db_index=True)
    target_muscle = models.CharField(max_length=100, db_index=True)
    equipment = models.CharField(max_length=100, db_index=True)
    gif_url = models.URLField(max_length=500, null=True, blank=True)
    instructions = models.JSONField(
        default=list, help_text="Step-by-step guide from API")
    local_gif = models.ImageField(upload_to='exercises/', null=True, blank=True)

    def __str__(self):
        return self.name.title()


class WorkoutPlan(models.Model):
    """
    User-created or system-provided workout routines (templates).
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    exercises = models.ManyToManyField(
        Exercise, through='PlanItem', related_name='workout_plans')

    def __str__(self):
        return self.title


class PlanItem(models.Model):
    """
    The 'Target' for an exercise within a plan (e.g., Target 3 sets of 10).
    """
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    target_sets = models.PositiveIntegerField(
        validators=[MinValueValidator(1)])
    target_reps = models.PositiveIntegerField(
        validators=[MinValueValidator(1)])
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.exercise.name} in {self.workout_plan.title}"


class WorkoutLog(models.Model):
    """
    A specific workout session completed by a user.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workout_logs')
    workout_plan = models.ForeignKey(
        WorkoutPlan, on_delete=models.SET_NULL, null=True, blank=True)
    logged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.logged_at.strftime('%Y-%m-%d %H:%M')}"


class SetLog(models.Model):
    """
    Individual data points for each set completed during a session.
    Used for progress charts (Reps/Weight history).
    """
    workout_log = models.ForeignKey(
        WorkoutLog, on_delete=models.CASCADE, related_name='sets')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    weight_kg = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    reps_completed = models.PositiveIntegerField(
        validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.exercise.name}: {self.reps_completed} reps @ {self.weight_kg}kg"
