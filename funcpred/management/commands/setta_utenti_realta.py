from django.core.management.base import BaseCommand, CommandError
from funcprod_app.models import *
from django.contrib.auth.models import User

class Command(BaseCommand):
    args = ''
    help = 'crea e setta l\'owner delle realta`'

    def handle(self, *args, **options):
        for r in Realta.objects.all():
                if r.email:
                    email=r.email[0:30]
                    u,created=User.objects.get_or_create(email=r.email, defaults={"username":email})
                    r.owner=u
                    r.save()
