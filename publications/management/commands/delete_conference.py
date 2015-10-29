from django.core.management.base import BaseCommand, CommandError
from publications.models import *

_DEFAULT_PATH = 'papers_info.json'

class Command(BaseCommand):
    help = 'Removes a conference instance with all its papers and paper-types'

    def handle(self, *args, **kwargs):
        data = input('Conference short name and year (e.g. ICGT 2015): ').split()
        try:
            short_name = " ".join(data[:-1])
            year = int(data[-1])
            conference_instance = ConferenceInstance.objects.get(
                start_date__year=year, conference__short_name=short_name)
        except:
            print('ERROR: Conference not found.')
            exit()

        conference_instance.delete()
        print('Conference %s deleted' % " ".join(data))
