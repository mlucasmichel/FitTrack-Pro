import json
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.db.models import Q, Sum, F, Max
from django.db.models.functions import TruncDate
from django.shortcuts import redirect, render, get_object_or_404
from .models import Exercise, WorkoutLog, SetLog, WorkoutPlan
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def exercise_list(request):
    """
    Displays a gallery of exercises.
    """
    query = request.GET.get('q')
    body_part = request.GET.get('body_part')

    exercises = Exercise.objects.all().order_by('name')

    if query:
        exercises = exercises.filter(
            Q(name__icontains=query) | Q(target_muscle__icontains=query)
        )

    if body_part:
        exercises = exercises.filter(body_part__iexact=body_part)

    # get body parts for filter dropdown
    body_parts = Exercise.objects.values_list(
        'body_part', flat=True).distinct().order_by('body_part')

    context = {
        'exercises': exercises,
        'body_parts': body_parts,
        'current_body_part': body_part,
    }
    return render(request, 'workouts/exercise_list.html', context)


def exercise_detail(request, exercise_id):
    """
    Displays the detailed 'How-To' page for a specific exercise.
    Includes instructions and data for progress charts.
    """
    exercise = get_object_or_404(Exercise, id=exercise_id)

    chart_data = {
        'labels': [],
        'heaviest_weight': [],
        'estimated_1rm': [],
        'best_set_volume': [],
        'session_volume': [],
        'total_reps': []
    }

    if request.user.is_authenticated:
        daily_stats = SetLog.objects.filter(
            workout_log__user=request.user,
            exercise=exercise
        ).annotate(
            date=TruncDate('workout_log__logged_at')
        ).values('date').annotate(
            max_weight=Max('weight_kg'),
            tot_reps=Sum('reps_completed'),
            # Session Volume
            sess_vol=Sum(F('weight_kg') * F('reps_completed')),
            # Best Set Volume
            best_set=Max(F('weight_kg') * F('reps_completed'))
        ).order_by('date')

        for stat in daily_stats:
            chart_data['labels'].append(stat['date'].strftime('%b %d'))

            w = float(stat['max_weight']) if stat['max_weight'] else 0
            r = int(stat['tot_reps']) if stat['tot_reps'] else 0

            chart_data['heaviest_weight'].append(round(w, 1))
            chart_data['total_reps'].append(r)
            chart_data['session_volume'].append(
                round(float(stat['sess_vol'] or 0), 1))
            chart_data['best_set_volume'].append(
                round(float(stat['best_set'] or 0), 1))

            estimated_1rm = w * (1 + (r / 30.0)) if w > 0 else 0
            chart_data['estimated_1rm'].append(round(estimated_1rm, 1))

    context = {
        'exercise': exercise,
        'chart_data_dict': chart_data,
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string(
            'workouts/partials/_exercise_detail_content.html', context, request=request)
        return HttpResponse(html)

    return render(request, 'workouts/exercise_detail.html', context)


@login_required
def log_workout(request, plan_id=None):
    """
    Allows the user to log a workout session.
    If a plan_id is provided, it pre-fills the session with the plan's exercises.
    """
    workout_plan = None
    if plan_id:
        workout_plan = get_object_or_404(WorkoutPlan, id=plan_id)

    # Get all exercises for logging or to add to a plan
    exercises = Exercise.objects.all().order_by('name')

    if request.method == 'POST':
        workout_log = WorkoutLog.objects.create(user=request.user)

        exercise_ids = request.POST.getlist('exercise_id_order[]')
        unique_ids = set(exercise_ids)

        for e_id in unique_ids:
            weights = request.POST.getlist(f'weight_{e_id}[]')
            reps = request.POST.getlist(f'reps_{e_id}[]')
            exercise = get_object_or_404(Exercise, id=e_id)

            for i in range(len(weights)):
                SetLog.objects.create(
                    workout_log=workout_log,
                    exercise=exercise,
                    weight_kg=weights[i],
                    reps_completed=reps[i]
                )

        return redirect('dashboard')

    context = {
        'workout_plan': workout_plan,
        'exercises': exercises,
    }
    return render(request, 'workouts/log_workout.html', context)


def workout_plan_list(request):
    """
    Displays all workout plans. Premium plans are marked.
    """
    plans = WorkoutPlan.objects.all().order_by('-created_at')

    # Check if user has active premium status
    is_premium_user = False
    if request.user.is_authenticated:
        is_premium_user = getattr(
            request.user.subscription, 'status', '') == 'active'

    context = {
        'plans': plans,
        'is_premium_user': is_premium_user,
    }
    return render(request, 'workouts/workout_plan_list.html', context)


@login_required
def routines_list(request):
    """
    Displays the Routines page. Handles gating logic for Free vs Premium users.
    """
    user = request.user

    # Check Premium Status
    is_premium = False
    if hasattr(user, 'subscription'):
        is_premium = user.subscription.status == 'active'

    # Fetch User's Custom Routines
    user_routines = WorkoutPlan.objects.filter(created_by=user).order_by('-created_at')
    user_routine_count = user_routines.count()

    # Gating Logic for Creating New Routines
    can_create_new = True
    if not is_premium and user_routine_count >= 3:
        can_create_new = False

    # Fetch System Routines
    system_routines = WorkoutPlan.objects.filter(created_by__isnull=True).order_by('title')

    context = {
        'is_premium': is_premium,
        'user_routines': user_routines,
        'system_routines': system_routines,
        'can_create_new': can_create_new,
        'routine_limit': 3,
    }
    return render(request, 'workouts/routines.html', context)


@login_required
def create_routine(request):
    """
    Drag-and-drop builder for custom workout routines.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')

        routine_data_str = request.POST.get('routine_data')

        if title and routine_data_str:
            routine_data = json.loads(routine_data_str)

            plan = WorkoutPlan.objects.create(
                title=title,
                description=description,
                created_by=request.user
            )

            for index, item in enumerate(routine_data):
                exercise = get_object_or_404(Exercise, id=item['exercise_id'])
                PlanItem.objects.create(
                    workout_plan=plan,
                    exercise=exercise,
                    target_sets=item['sets'],
                    target_reps=item['reps'],
                    order=index
                )

            messages.success(request, "Routine saved successfully!")
            return redirect('routines')

    exercises = Exercise.objects.all().order_by('name')
    return render(request, 'workouts/create_routine.html', {'exercises': exercises})