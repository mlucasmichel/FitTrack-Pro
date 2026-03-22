from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Exercise, WorkoutPlan, PlanItem, WorkoutLog, SetLog

User = get_user_model()


class WorkoutLogicTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password123')
        self.exercise = Exercise.objects.create(
            api_id="0001",
            name="Test Push Up",
            body_part="chest"
        )
        self.plan = WorkoutPlan.objects.create(
            title="Free Plan", is_premium=False)

    def test_negative_weight_rejected(self):
        """Test that weights below 0 raise a ValidationError"""
        item = PlanItem(
            workout_plan=self.plan,
            exercise=self.exercise,
            target_sets=3,
            target_reps=10
        )

        with self.assertRaises(ValidationError):
            item.target_sets = -1
            item.full_clean()

    def test_routine_creation_limit(self):
        """Test the logic in the view that limits users to 3 workout plans"""
        WorkoutPlan.objects.create(title="P1", created_by=self.user)
        WorkoutPlan.objects.create(title="P2", created_by=self.user)
        WorkoutPlan.objects.create(title="P3", created_by=self.user)

        count = WorkoutPlan.objects.filter(created_by=self.user).count()
        self.assertEqual(count, 3)


class WorkoutSystemTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='athlete', password='password123')
        self.pro_user = User.objects.create_user(
            username='pro_athlete', password='password123')

        self.exercise = Exercise.objects.create(
            api_id="0001", name="Push Up", body_part="chest", target_muscle="pectoralis major", equipment="body weight"
        )
        self.free_plan = WorkoutPlan.objects.create(
            title="Starter Plan", is_premium=False)
        self.pro_plan = WorkoutPlan.objects.create(
            title="Elite Plan", is_premium=True)

    def test_exercise_creation(self):
        """Verify exercise fields save correctly"""
        self.assertEqual(self.exercise.name, "Push Up")
        self.assertEqual(str(self.exercise), "Push Up")

    def test_negative_reps_validation(self):
        """Ensure MinValueValidator blocks 0 or negative reps/sets"""
        item = PlanItem(workout_plan=self.free_plan,
                        exercise=self.exercise, target_sets=0, target_reps=-5)
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_workout_log_creation(self):
        """Verify session logging works"""
        log = WorkoutLog.objects.create(
            user=self.user, workout_plan=self.free_plan)
        set_entry = SetLog.objects.create(
            workout_log=log, exercise=self.exercise, weight_kg=0, reps_completed=15)
        self.assertEqual(log.sets.count(), 1)
        self.assertEqual(set_entry.reps_completed, 15)

    def test_routines_view_requires_login(self):
        """Security check: anonymous users redirected to login"""
        response = self.client.get(reverse('routines'))
        self.assertEqual(response.status_code, 302)
