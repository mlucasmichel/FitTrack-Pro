import requests
from django.conf import settings
from django.core.files.base import ContentFile
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
                    'instructions': item.get('instructions', []),
                }
            )

            if not exercise.local_gif:
                gif_id = item.get('id')

                image_url = f"https://exercisedb.p.rapidapi.com/image?exerciseId={gif_id}&resolution=360"

                try:
                    img_response = requests.get(image_url, headers=headers)
                    img_response.raise_for_status()
                    exercise.local_gif.save(f"{gif_id}.gif", ContentFile(img_response.content), save=True)
                except Exception as e:
                    print(f"Failed to download GIF for {exercise.name}: {e}")

            if created:
                count += 1

        return f"Successfully synced {count} exercises with GIFs."

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
