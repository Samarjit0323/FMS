# your_app_name/management/commands/migrate_media.py

import os
from django.core.management.base import BaseCommand
from faculty.models import FacultyProfile # <-- CHANGE 'FacultyProfile' to your model name
from django.conf import settings # Needed for potential pathing

class Command(BaseCommand):
    help = 'Updates DB records with Cloudinary Public IDs based on local file paths.'

    def handle(self, *args, **options):
        # Filter for objects that actually have an image/file to migrate
        # Adjust 'image' to your actual CloudinaryField name
        records_to_migrate = FacultyProfile.objects.filter(image__isnull=False).exclude(image='')
        
        self.stdout.write(f"Found {records_to_migrate.count()} records to migrate...")

        for profile in records_to_migrate:
            try:
                # 1. Get the old file name/path stored in the database
                # Access the underlying string value directly from the CloudinaryField object
                old_relative_path = str(profile.image) 

                # IMPORTANT: Skip records that are already migrated or empty
                # An already-migrated field would have no extension (e.g., 'profile_pics/dr_smith')
                # if '.' not in old_relative_path:
                #     self.stdout.write(self.style.WARNING(f"Skipping PK {profile.pk}: Already appears migrated or empty."))
                #     continue
                    
                # 2. Derive the Cloudinary Public ID (by removing the extension)
                public_id = os.path.splitext(old_relative_path)[0]

                # 3. Update the CloudinaryField with the Public ID
                profile.image = public_id
                profile.save()
                
                self.stdout.write(self.style.SUCCESS(
                    f"Updated PK {profile.pk} | Old Path: {old_relative_path} -> New ID: {public_id}"
                ))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error migrating PK {profile.pk}: {e}"))