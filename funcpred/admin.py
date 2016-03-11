#-*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import *

class FunctionAdmin(admin.ModelAdmin):
    search_fields=("keyword","description")
    list_display=("pk","ontology","keyword","description")

class OntologyAdmin(admin.ModelAdmin):
    list_display=("pk","name")

class GeneAdmin(admin.ModelAdmin):
    list_display=("pk","ensg","name")

class GeneAliasAdmin(admin.ModelAdmin):
    raw_id_fields=('gene',)
    list_display=("pk","gene","name")

class ExpressionSourceAdmin(admin.ModelAdmin):
    list_display=("pk","name")

class GeneSearchAdmin(admin.ModelAdmin):
    raw_id_fields=('gene',)
    list_display=("pk","gene")

class GeneFunctionAdmin(admin.ModelAdmin):
    raw_id_fields=('gene','function')
    #list_display=("pk","gene__ensg","function__name","expression_source","fdr")
    list_filter = ('function__ontology',)
    show_full_result_count = False

# Register your models here.
admin.site.register(Ontology, OntologyAdmin)
admin.site.register(Function, FunctionAdmin)
admin.site.register(Gene, GeneAdmin)
admin.site.register(GeneAlias, GeneAliasAdmin)
admin.site.register(ExpressionSource, ExpressionSourceAdmin)
admin.site.register(GeneSearch, GeneSearchAdmin)
admin.site.register(GeneFunction, GeneFunctionAdmin)
