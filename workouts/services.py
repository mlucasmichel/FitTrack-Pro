import requests
import time
from django.conf import settings
from django.core.files.base import ContentFile
from .models import Exercise


def fetch_and_sync_exercises(total_target=100):
    """
    Fetches exercises from RapidAPI ExerciseDB
    """
    url = f"https://{settings.RAPIDAPI_HOST}/exercises"
    headers = {
        "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
        "X-RapidAPI-Host": settings.RAPIDAPI_HOST
    }

    new_count = 0
    updated_count = 0
    gif_count = 0
    offset = 0
    limit_per_request = 10

    print(f"Starting paginated sync. Target: {total_target} exercises.")

    while offset < total_target:
        params = {
            "limit": str(limit_per_request),
            "offset": str(offset)
        }

        print(f"Fetching offset {offset}...")

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            if not data:
                break

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

                if created:
                    new_count += 1
                else:
                    updated_count += 1

                if not exercise.local_gif:
                    gif_id = item.get('id')
                    image_url = f"https://exercisedb.p.rapidapi.com/image?exerciseId={gif_id}&resolution=360"

                    try:
                        img_response = requests.get(image_url, headers=headers)
                        img_response.raise_for_status()
                        exercise.local_gif.save(f"{gif_id}.gif", ContentFile(
                            img_response.content), save=True)
                        gif_count += 1
                    except Exception as e:
                        print(f"Failed GIF for {exercise.name}: {e}")

            offset += limit_per_request

            time.sleep(1)

        except requests.exceptions.RequestException as e:
            return f"Error on offset {offset}: {e}"

    return f"Done! {new_count} created, {updated_count} updated. {gif_count} new GIFs downloaded."
