from django.shortcuts import render
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