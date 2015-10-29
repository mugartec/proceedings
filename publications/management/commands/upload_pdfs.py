from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from publications.models import *

_DEFAULT_PATH = 'papers_info.json'

class Command(BaseCommand):
    help = 'Creates/updates database from a json file'

    def handle(self, *args, **kwargs):
        data = input('Conference short name and year (e.g. ICGT 2015): ').split()
        try:
            short_name = " ".join(data[:-1])
            year = int(data[-1])
            instance = ConferenceInstance.objects.get(
                start_date__year=year, conference__short_name=short_name)
        except Exception as error:
            print(error)
            print('ERROR: Conference not found.')
            exit()

        err_cnt = 0
        for paper in instance.papers.all():
            print('\nUploading %s' % paper.pdf_path())
            if paper.has_pdf():
                if paper.pdf:
                    print('\tfile already existed, overwriting')
                paper.pdf = File(open(paper.pdf_path(), 'rb'))
                paper.save()
            else:
                err_cnt += 1
                print('ERROR file not found: %s' % paper.pdf_path())

        if err_cnt:
            print('\n%d FILES NOT FOUND' % err_cnt)
        else:
            print('\nALL OK!')