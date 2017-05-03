#-*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from .models import *


class FunctionAdmin(admin.ModelAdmin):
    search_fields=("keyword","description")
    list_display=("pk","ontology","keyword","description")
    list_filter=("ontology",)

class OntologyAdmin(admin.ModelAdmin):
    list_display=("pk","name")

class DiseaseAdmin(admin.ModelAdmin):
    list_display=("pk","keyword")

class GeneAdmin(admin.ModelAdmin):
    search_fields=("ensg","description")
    list_display=("pk","ensg","name")

class GeneAliasAdmin(admin.ModelAdmin):
    raw_id_fields=('gene',)
    list_display=("pk","gene","name")

class ExpressionSourceAdmin(admin.ModelAdmin):
    list_display=("pk","name")

class GeneSearchAdmin(admin.ModelAdmin):
    raw_id_fields=('gene',)
    list_display=("pk","gene")

class FunctionSearchAdmin(admin.ModelAdmin):
    raw_id_fields=('function',)
    list_display=("pk","function")

class GeneFunctionAdmin(admin.ModelAdmin):
    raw_id_fields=('gene','function')
    list_display=("pk","gene","function","expression_source","fdr")

# Register your models here.
admin.site.register(Disease, DiseaseAdmin)
admin.site.register(Ontology, OntologyAdmin)
admin.site.register(Function, FunctionAdmin)
admin.site.register(Gene, GeneAdmin)
admin.site.register(GeneAlias, GeneAliasAdmin)
admin.site.register(ExpressionSource, ExpressionSourceAdmin)
admin.site.register(GeneSearch, GeneSearchAdmin)
admin.site.register(FunctionSearch, FunctionSearchAdmin)
admin.site.register(GeneFunction, GeneFunctionAdmin)
