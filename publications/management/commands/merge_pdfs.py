from django.core.management.base import BaseCommand, CommandError
from PyPDF2 import PdfFileMerger, PdfFileReader
from publications.models import *
import os

_DEFAULT_OUTPUT_PATH = './proceedings.pdf'

class Command(BaseCommand):
    help = 'Merges all Pdfs in relative order'

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

        merger = PdfFileMerger()

        for paper in instance.papers.order_by('proceedings_relative_order').all():
            print('adding %s' % paper.pdf_path())
            try:
                merger.append(PdfFileReader(open(paper.pdf_path(), 'rb')))
            except Exception as err:
                print('ERROR: %s' % err)

        print('\nAll ok, now let\'s save it...')

        output_path = input('\nInsert the output path [./proceedings.pdf]:')

        if not output_path:
            output_path = _DEFAULT_OUTPUT_PATH

        merger.write(output_path)
        print('\nPDF file written to %s' % output_path)
