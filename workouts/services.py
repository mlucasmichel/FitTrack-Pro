import requests
from django.conf import settings
from .models import Exercise


def fetch_and_sync_exercises():
    """
    Fetches exercises from RapidAPI ExerciseDB and saves them to the database.
    """
    url = f"https://{settings.RAPIDAPI_HOST}/exercises"
    headers = {
        "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
        "X-RapidAPI-Host": settings.RAPIDAPI_HOST
    }

    params = {"limit": "10"}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        count = 0
        for item in data:
            exercise, created = Exercise.objects.update_or_create(
                api_id=item.get('id'),
                defaults={
                    'name': item.get('name', 'Unknown Exercise'),
                    'body_part': item.get('bodyPart', 'Unknown'),
                    'target_muscle': item.get('target', 'Unknown'),
                    'equipment': item.get('equipment', 'None'),
                    'gif_url': item.get('gifUrl', ''),
                    'instructions': item.get('instructions', []),
                }
            )
            if created:
                count += 1

        return f"Successfully synced {count} new exercises."

    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"
