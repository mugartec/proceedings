from django.core.management.base import BaseCommand, CommandError
from publications.models import *
from PyPDF2 import PdfFileReader
import re

_DEFAULT_FIRST_PAGE = 1

class Command(BaseCommand):
    help = 'Changes the page numbers according to relative order'

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

        first_page = input('Number of the first page of the first paper [1]:')
        if first_page:
            try:
                first_page = int(first_page)
            except:
                print('Come on...')
                exit()
        else:
            first_page = _DEFAULT_FIRST_PAGE
        

        for paper in instance.papers.order_by('proceedings_relative_order').all():
            print('Changing first page of paper #%d to %s' % (paper.conf_id, str(first_page)))
            try:
                content = open(paper.tex_path()).read()
            except:
                print('ERROR: File %s could not be opened, make sure it exists and has read permissions.', paper.tex_path())

            position = content.find('%firstpage')
            if position == -1:
                print('The file' + paper.tex_path() +  ' is not marked with --firstpagenumber.')
                print('Make sure every tex file has a line ending with {n}\%--firstpagenumber,')
                print('where n is the number of the first page. Then run this again.')
                exit()

            new_content = re.sub(r'\{\d+\}%firstpage',
                '{%d}%%firstpage' % first_page, content)
            new_file = open(paper.tex_path(), 'w')
            new_file.write(new_content)
            new_file.close()

            try:
                pdf_file = PdfFileReader(open(paper.pdf_path(), 'rb'))
                first_page += pdf_file.getNumPages()
            except Exception as error:
                print('Could get number of pages from file %s' % paper.pdf_path())
                print('Make sure that all PDFs are in place and run again')
                exit()

        print('\nALL OK.')
