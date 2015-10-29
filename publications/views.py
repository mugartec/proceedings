from django.shortcuts import render
from publications.models import PaperType, ConferenceInstance, Paper
# Create your views here.


def home(request):
	conferences = ConferenceInstance.objects.all()
	return render(request, 'home.html', {'conferences': conferences})


def conference_instance(request, conf_id):
	conference_instance = ConferenceInstance.objects.get(id=conf_id)
	paper_types = conference_instance.paper_types.all()
	data = {'conference_instance': conference_instance,
			'paper_types': paper_types}
	return render(request, 'papers.html', data)
