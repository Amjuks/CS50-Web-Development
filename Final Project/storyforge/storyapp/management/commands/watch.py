import os
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings

EXCLUDED_FILES = {'variables.scss', 'mixins.scss'}  # Add more files as needed

class Command(BaseCommand):
    help = 'Finds all SCSS folders in static directories and runs sass --watch on them, excluding certain files'

    def handle(self, *args, **options):
        # Get list of installed apps
        installed_apps = settings.INSTALLED_APPS

        # Define base directory for static files
        base_static_dir = 'static'

        sass_command_parts = []

        # Iterate through all installed apps
        for app in installed_apps:
            # Get the app's path
            app_path = os.path.join(settings.BASE_DIR, app.replace('.', '/'))

            # Define the static directory path
            static_path = os.path.join(app_path, base_static_dir)

            if os.path.exists(static_path):
                # Search for SCSS folders
                for root, dirs, files in os.walk(static_path):
                    if 'scss' in dirs:
                        scss_dir = os.path.join(root, 'scss')
                        css_dir = os.path.join(root, 'css')
                        
                        # Filter out excluded files and prepare paths for valid SCSS files
                        for scss_file in os.listdir(scss_dir):
                            if scss_file.endswith('.scss') and scss_file not in EXCLUDED_FILES:
                                scss_file_path = os.path.join(scss_dir, scss_file)
                                css_file_path = os.path.join(css_dir, os.path.splitext(scss_file)[0] + '.css')
                                sass_command_parts.append(f'{scss_file_path}:{css_file_path}')

        if not sass_command_parts:
            self.stdout.write(self.style.WARNING('No valid SCSS files found or all SCSS files are excluded.'))
            return

        # Construct the full sass command
        sass_command = ['sass', '--watch'] + sass_command_parts

        self.stdout.write(self.style.SUCCESS(f'Starting watcher with command: {" ".join(sass_command)}'))

        try:
            # Run sass --watch with the constructed command
            subprocess.run(sass_command, check=True)
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f'Error occurred: {e}'))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR('Sass not found. Make sure it is installed.'))
