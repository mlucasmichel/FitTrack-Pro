from django.shortcuts import render, get_object_or_404
from .models import Exercise
from django.db.models import Q


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
    body_parts = Exercise.objects.values_list('body_part', flat=True).distinct().order_by('body_part')

    context = {
        'exercises': exercises,
        'body_parts': body_parts,
        'current_body_part': body_part,
    }
    return render(request, 'workouts/exercise_list.html', context)


def exercise_detail(request, exercise_id):
    """
    Displays the detailed 'How-To' page for a specific exercise.
    Includes instructions and a placeholder for progress charts.
    """
    exercise = get_object_or_404(Exercise, id=exercise_id)

    # User's progress data needed here later for Chart.js
    # progress_data = SetLog.objects.filter(user=request.user, exercise=exercise).order_by('workout_log__logged_at')

    context = {
        'exercise': exercise,
        # 'progress_data': progress_data,
    }
    return render(request, 'workouts/exercise_detail.html', context)