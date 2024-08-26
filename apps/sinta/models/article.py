"""Article Model"""
from django.db import models
from apps.sinta.models.journal import Journal


class Article(models.Model):
    """Article Model"""
    journal = models.ForeignKey(Journal, on_delete=models.SET_NULL, blank=True, null=True)
    garuda_id = models.IntegerField(unique=True)
    garuda_url = models.URLField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    author = models.JSONField(blank=True, null=True)
    volume = models.TextField(blank=True, null=True)
    publisher = models.TextField(blank=True, null=True)
    file_url = models.URLField(max_length=1000, blank=True, null=True)
    source_url = models.URLField(max_length=1000, blank=True, null=True)
    gsholar_url = models.URLField(max_length=1000, blank=True, null=True)
    pdf_url = models.URLField(max_length=1000, blank=True, null=True)
    doi_url = models.URLField(max_length=1000, blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    total_journal_document = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.garuda_id} - {self.title}"
