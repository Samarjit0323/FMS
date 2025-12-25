from django.core.management.base import BaseCommand
from cloudinary.uploader import upload
from django.conf import settings
import os

from faculty.models import (
    FacultyProfile,
    PersonalDocs,
    AssignmentDocs,
    ResearchPublications,
)

class Command(BaseCommand):
    help = "Upload local media to Cloudinary and update Neon DB references"

    def upload_and_update(self, instance, field_name, folder):
        file_field = getattr(instance, field_name)

        if not file_field:
            return

        # OLD local path stored in DB
        local_path = os.path.join(settings.BASE_DIR, 'media', str(file_field))

        if not os.path.exists(local_path):
            self.stdout.write(
                self.style.WARNING(f"File not found: {local_path}")
            )
            return

        # Upload to Cloudinary
        result = upload(
            local_path,
            folder=folder,
            resource_type="auto"
        )

        # Save Cloudinary public_id
        setattr(instance, field_name, result['public_id'])
        instance.save(update_fields=[field_name])

        self.stdout.write(
            self.style.SUCCESS(
                f"✔ {local_path} → {result['public_id']}"
            )
        )

    def handle(self, *args, **kwargs):

        self.stdout.write("Migrating FacultyProfile images...")
        for profile in FacultyProfile.objects.all():
            self.upload_and_update(profile, 'image', 'profile_pics')

        self.stdout.write("Migrating PersonalDocs...")
        for doc in PersonalDocs.objects.all():
            self.upload_and_update(doc, 'doc', 'docs/personal_docs')

        self.stdout.write("Migrating AssignmentDocs...")
        for assignment in AssignmentDocs.objects.all():
            self.upload_and_update(assignment, 'file', 'docs/assignments')

        self.stdout.write("Migrating ResearchPublications...")
        for research in ResearchPublications.objects.all():
            self.upload_and_update(research, 'file', 'docs/research')

        self.stdout.write(
            self.style.SUCCESS("🎉 Media migration completed successfully!")
        )
