#-*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from .models import *


class FunctionAdmin(admin.ModelAdmin):
	list_display=("pk","ontology","keyword","description")
	pass

class OntologyAdmin(admin.ModelAdmin):
	list_display=("pk","name")

class GeneAdmin(admin.ModelAdmin):
	list_display=("pk","ensg","name")

class GeneAliasAdmin(admin.ModelAdmin):
	list_display=("pk","gene","name")

class ExpressionSourceAdmin(admin.ModelAdmin):
	list_display=("pk","name")

# Register your models here.
admin.site.register(Ontology, OntologyAdmin)
admin.site.register(Function, FunctionAdmin)
admin.site.register(Gene, GeneAdmin)
admin.site.register(GeneAlias, GeneAliasAdmin)
admin.site.register(ExpressionSource, ExpressionSourceAdmin)
