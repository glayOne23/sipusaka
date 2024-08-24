"""Journal Model"""
from django.db import models
from apps.sinta.models.university import University


class Journal(models.Model):
    """Journal Model"""
    university = models.ForeignKey(University, on_delete=models.SET_NULL, blank=True, null=True)
    sinta_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    gsholar_url = models.URLField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    editor_url = models.URLField(blank=True, null=True)
    pissn = models.CharField(max_length=255, blank=True, null=True)
    eissn = models.CharField(max_length=255, blank=True, null=True)
    subject = models.TextField(blank=True, null=True)
    accredited = models.CharField(max_length=255, blank=True, null=True)
    scopus = models.CharField(max_length=255, blank=True, null=True)
    garuda_url = models.URLField(blank=True, null=True)
    impact = models.CharField(max_length=255, blank=True, null=True)
    h5_index = models.CharField(max_length=255, blank=True, null=True)
    citation_5y = models.CharField(max_length=255, blank=True, null=True)
    citation = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    garuda_description = models.TextField(blank=True, null=True)
    garuda_image_url = models.URLField(blank=True, null=True)
    garuda_subject = models.TextField(blank=True, null=True)
    aruna_subject = models.TextField(blank=True, null=True)
    doi_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.sinta_id} - {self.name}"

