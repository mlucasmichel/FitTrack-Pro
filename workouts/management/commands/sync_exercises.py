from django.core.management.base import BaseCommand
from workouts.services import fetch_and_sync_exercises


class Command(BaseCommand):
    help = 'Fetches exercises from RapidAPI and syncs them to the database'

    def handle(self, *args, **kwargs):
        self.stdout.write("Syncing exercises from API...")
        result = fetch_and_sync_exercises()
        self.stdout.write(self.style.SUCCESS(result))
