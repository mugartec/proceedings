from django.core.management.base import BaseCommand, CommandError
from publications.models import Paper, ConferenceInstance
from subprocess import check_call
import sys, os

_DEFAULT_PATH = 'papers_info.json'
_DEFAULT_COMMAND = 'pdflatex -halt-on-error'

class Command(BaseCommand):
    help = 'Removes a conference instance with all its papers and paper-types'

    def handle(self, *args, **kwargs):
        data = input('Conference short name and year (e.g. ICGT 2015): ').split()
        try:
            short_name = " ".join(data[:-1])
            year = int(data[-1])
            conference_instance = ConferenceInstance.objects.get(
                start_date__year=year, conference__short_name=short_name)
        except Exception as error:
            print(error)
            print('ERROR: Conference not found.')
            exit()

        cmd = input('LaTeX compilation command [%s]: ' % _DEFAULT_COMMAND)
        if not cmd:
            cmd = _DEFAULT_COMMAND

        errors = []
        for paper in conference_instance.papers.all():
            try:
                command = 'cd %s && %s %s' % (paper.path, cmd, paper.tex_path())
                print('\n\n-----------------COMPILING PAPER %d' % paper.conf_id)
                check_call(command, shell=True)
            except Exception as error:
                errors.append((paper.conf_id, command, error))

        print('\n\n----------RESULTS----------')
        if errors:
            print('\n %d COMPILATION ERRORS:' % len(errors))
            for error in errors:
                print('\n--------PAPER %d' % error[0])
                print('COMMAND: %s' % error[1])
                print('ERROR: %s' % error[2])
                print('----END PAPER %d' % error[0])
        else:
            print('\n\tALL OK!')

        print('\n---------END RESULTS--------')

