#-*- coding: utf-8 -*-
from django.db import models

class GeneAlias(models.Model):
    gene = models.ForeignKey("Gene")
    name = models.CharField(max_length=160)
    description = models.TextField()

    def __unicode__(self):
        return self.name

BIOTYPE_CHOICES=(
        ("lincRNA","lincRNA"),
        ("other","other"),
        ("protein_coding","protein_coding"),
        ("antisense","antisense"),
        ("pseudogene","pseudogene")
)

class Gene(models.Model):
    ensg = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True, null=True)
    biotype = models.CharField(max_length=14, choices=BIOTYPE_CHOICES, default="other")
    status = models.CharField(max_length=160)

    def __unicode__(self):
        return u"%s - %s" % (self.ensg, self.name)

class Ontology(models.Model):
    name = models.CharField(max_length=160)
    description = models.TextField()

    def __unicode__(self):
        return self.name

class Function(models.Model):
    keyword = models.CharField(max_length=160, unique=True)
    description = models.TextField(blank=True, null=True)
    ontology = models.ForeignKey(Ontology)

    def __unicode__(self):
        return self.keyword


class ExpressionSource(models.Model):
    name = models.CharField(max_length=160)
    internal_name = models.CharField(max_length=160)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

class GeneFunction(models.Model):
    gene = models.ForeignKey(Gene)
    function = models.ForeignKey(Function)
    fdr = models.FloatField()
    expression_source = models.ForeignKey(ExpressionSource)
    known = models.BooleanField()

    class Meta:
        ordering = ['fdr',]
        unique_together = (("gene", "function", "expression_source"),)
    
    def __unicode__(self):
        return "%s\t%s\t%g\t%s" % (gene,function,fdr,predictior)

class GeneSearch(models.Model):
    gene = models.ForeignKey(Gene)
    expression_source = models.ManyToManyField(ExpressionSource)
    ontology = models.ManyToManyField(Ontology)

