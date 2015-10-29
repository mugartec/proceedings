from django.db import models
import os

# Create your models here.


class Affiliation(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100, unique=True)


class Author(models.Model):
    def __str__(self):
        return self.full_name

    affiliations = models.ManyToManyField(Affiliation)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)


class Conference(models.Model):
    def __str__(self):
        return self.short_name

    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=10, unique=True)


class ConferenceInstance(models.Model):
    def __str__(self):
        return self.conference.short_name + ' ' + str(self.year())

    conference = models.ForeignKey(Conference)
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

    def year(self):
        return self.start_date.year

    def short_description(self):
        return '%s %d' % (self.conference.short_name, self.year())


class PaperType(models.Model):
    def __str__(self):
        return self.name

    conference_instance = models.ForeignKey(ConferenceInstance, related_name='paper_types')
    name = models.CharField(max_length=50, unique=True)

    def sorted_papers(self):
        return sorted(self.papers.all(), key=lambda x: x.conf_id)


class Paper(models.Model):
    def __str__(self):
        return self.title + ' - ' + ', '.join([x.full_name for x in self.authors.all()])

    conference_instance = models.ForeignKey(ConferenceInstance, related_name='papers')
    paper_type = models.ForeignKey(PaperType, related_name='papers')
    authors = models.ManyToManyField(Author, related_name='papers')
    first_author = models.ForeignKey(Author, null=True)
    title = models.CharField(max_length=200)
    pdf = models.FileField(upload_to='papers/', blank=True, null=True)
    path = models.CharField(max_length=200, blank=True, null=True)
    filename = models.CharField(max_length=100, blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    conf_id = models.PositiveIntegerField()
    proceedings_relative_order = models.PositiveIntegerField(blank=True, null=True)
    session_relative_order = models.PositiveIntegerField(blank=True, null=True)

    def authors_string(self):
        string = ""
        for author in self.authors.all():
            string += author.full_name + ', '
        return string[:-2][::-1].replace(' ,', ' dna ', 1)[::-1]

    def has_pdf(self):
        return os.path.isfile(self.pdf_path())

    def tex_path(self):
        return os.path.join(self.path, self.filename + '.tex')

    def pdf_path(self):
        return os.path.join(self.path, self.filename + '.pdf')

