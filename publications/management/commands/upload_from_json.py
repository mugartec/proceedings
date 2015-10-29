from django.core.management.base import BaseCommand, CommandError
import json
import string
from django.core.files import File
from publications.models import *
from datetime import datetime as dt

_DEFAULT_PATH = 'papers_info.json'

class Command(BaseCommand):
    help = 'Creates/updates database from a json file'

    def handle(self, *args, **kwargs):

    	input_file = input('Path to json file with the format specified in readme.md [papers_info.json]: ')
    	if not input_file:
    		input_file = _DEFAULT_PATH
    	try:
    		json_file = json.load(open(input_file))
    	except:
    		print('Could not read the json file, make sure it exists and has .json extension.')
    		exit()

    	short_name = json_file['conference']['short_name']
    	name = json_file['conference']['name']

    	conference, new = Conference.objects.get_or_create(
    		short_name=short_name, name=name)

    	start_date = dt.strptime(json_file['conference']['start_date'], '%Y-%m-%d')
    	end_date = dt.strptime(json_file['conference']['end_date'], '%Y-%m-%d')

    	conference_instance, new = ConferenceInstance.objects.get_or_create(
    		conference=conference, start_date=start_date, end_date=end_date)

    	add_papers(conference_instance, json_file['papers'])



def add_papers(conference_instance, papers):
	for paper in papers:
		conf_id = paper['id']
		title = paper['title']

		print('processing paper %d: %s' % (conf_id, title))
		p = Paper.objects.filter(conf_id=conf_id, conference_instance=conference_instance) 
		if p:
			print('paper with id %d already existed, overwriting' % conf_id)
			p.delete()

		pt, new = PaperType.objects.get_or_create(
			conference_instance=conference_instance, name=paper['type'])

		authors = []

		for creator in paper['authors']:
			author, new = Author.objects.get_or_create(full_name=creator['name'])
			if 'email' in creator:
				author.email = creator['email']
			author.save()
			if 'affiliations' in creator:
				for affiliation in creator['affiliations']:
					af, new = Affiliation.objects.get_or_create(name=affiliation)
					if not af in author.affiliations.all():
						author.affiliations.add(af)
			
			authors.append(author)

		p = Paper(conf_id=conf_id,
				  title=title,
				  paper_type=pt,
				  conference_instance=conference_instance)

		if 'abstract' in paper:
			p.abstract = paper['abstract']
		if 'path' in paper:
			p.path = paper['path']
		if 'filename' in paper:
			p.filename = paper['filename']
		if 'relative_order' in paper:
			p.proceedings_relative_order = paper['relative_order']

		p.save()

		for author in authors:
			p.authors.add(author)
