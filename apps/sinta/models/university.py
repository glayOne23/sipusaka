"""University Model"""
from django.db import models


class University(models.Model):
    """University Model"""

    sinta_id = models.IntegerField(unique=True)
    sinta_code = models.CharField(max_length=255, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    abbrev = models.CharField(max_length=255, blank=True, null=True)
    total_department = models.IntegerField(blank=True, null=True)
    total_author = models.IntegerField(blank=True, null=True)
    total_journal = models.IntegerField(blank=True, null=True)
    total_document_scopus = models.IntegerField(blank=True, null=True)
    total_document_gsholar = models.IntegerField(blank=True, null=True)
    total_document_wos = models.IntegerField(blank=True, null=True)
    total_document_garuda = models.IntegerField(blank=True, null=True)
    total_citation_scopus = models.IntegerField(blank=True, null=True)
    total_citation_gsholar = models.IntegerField(blank=True, null=True)
    total_citation_wos = models.IntegerField(blank=True, null=True)
    total_citation_garuda = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.sinta_id} - {self.name}"