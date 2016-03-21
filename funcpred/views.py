# Create your views here.
from collections import defaultdict
from operator import itemgetter
from django.utils import timezone
from django.http import HttpResponse#, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
#from django.core.urlresolvers import reverse
from dal import autocomplete
from django.db.models import Q
import operator

from .models import GeneSearch, FunctionSearch, Gene, GeneFunction, Function, Ontology

class GeneSearchForm(forms.ModelForm):
    #gene = forms.ModelChoiceField(
    #    queryset=Gene.objects.all(),
    #    widget = autocomplete.ModelSelect2(url='dal-gene')
    #)
    class Meta:
        model = GeneSearch
        fields = ['gene','expression_source','ontology']
        widgets = {
                'gene': autocomplete.ModelSelect2(url='dal-gene'),
                #'expression_source': forms.CheckboxSelectMultiple(),
                'ontology': forms.CheckboxSelectMultiple()
        }

class FunctionSearchForm(forms.ModelForm):
    #gene = forms.ModelChoiceField(
    #    queryset=Gene.objects.all(),
    #    widget = autocomplete.ModelSelect2(url='dal-gene')
    #)
    class Meta:
        model = FunctionSearch
        fields = ['ontology','function','expression_source','biotype']
        widgets = {
                'function': autocomplete.ModelSelect2(url='dal-function',forward=['ontology',]),
        }

def home(request):
    return render(request, 'home.html')

def browse_ontologies(request):
    ontologies=Ontology.objects.all()
    return render(request, 'browse_ontologies.html',{'ontologies': ontologies})

def browse_functions(request, ontology_pk):
    functions=Function.objects.filter(ontology=int(ontology_pk))
    return render(request, 'browse_functions.html',{'functions': functions})

def make_basic_function_search(request, function_pk):
    fs=FunctionSearch.objects.create(function=Function.objects.get(pk=int(function_pk)))
    fs.expression_source.add(1)

    return show_function_search(request,function_search_pk=fs.pk)
    


def gene_search(request):
    if request.method == 'POST':
        form = GeneSearchForm(request.POST)
        if form.is_valid():
            gene_search=form.save()
            return redirect("show_gene_search", gene_search_pk=gene_search.pk)
    else:
        form = GeneSearchForm()
    return render(request, 'search_gene.html',{'form': form})

def function_search(request):
    if request.method == 'POST':
        form = FunctionSearchForm(request.POST)
        if form.is_valid():
            function_search=form.save()
            return redirect("show_function_search", function_search_pk=function_search.pk)
    else:
        form = FunctionSearchForm()
    return render(request, 'search_function.html',{'form': form})

def show_function_search(request, function_search_pk):
    function_search = FunctionSearch.objects.get(pk=function_search_pk)
    exp_sources = [e.name for e in function_search.expression_source.all()]
    gene_functions = GeneFunction.objects.filter(function=function_search.function, expression_source__in=function_search.expression_source.all())
    if function_search.biotype:
        gene_functions = gene_functions.filter(biotype=function_search.biotype)
    #return render(request, 'show_gene_search.html',{'gene_search': gene_search,'gene_functions':gene_functions})
    
    # aggregate ####
    min_fdr=defaultdict(set)
    has_expression_source=defaultdict(set)
    for gf in gene_functions:
        min_fdr[gf.gene.pk].add(gf.fdr)
        has_expression_source[gf.gene.pk].add(gf.expression_source.name)
    min_fdr = {k:min(v) for k,v in min_fdr.iteritems()}
    
    data=[]
    for gf in gene_functions:
        data.append({
            'gene': gf.gene,
            'best_fdr': "%.2g" % min_fdr[gf.gene.pk],
            'exp_sources': ( e in has_expression_source[gf.gene.pk] for e in exp_sources)
        })
    ################

    return render(request, 'show_function_search.html',{'function_search': function_search,'gene_functions':gene_functions, 'data': data , 'exp_sources': exp_sources})


    # aggregate ####
    min_fdr=defaultdict(set)
    has_expression_source=defaultdict(set)
    for gf in gene_functions:
        min_fdr[gf.gene.pk].add(gf.fdr)
        has_expression_source[gf.gene.pk].add(gf.expression_source.name)
    min_fdr = {k:min(v) for k,v in min_fdr.iteritems()}
    
    data=[]
    for gf in gene_functions:
        data.append({
            'gene': gf.gene,
            'biotype': gf.gene.biotype,
            'description':gf.gene.description,
            'best_fdr': min_fdr[gf.gene.pk],
        })
        for c in columns:
            v=False
            if c in has_expression_source[gf.function.pk]:
                v=True
            data[-1][c]=v
    ################

    data.sort(key=itemgetter('best_fdr'))

    return render(request, 'show_function_search.html',{'function_search': function_search,'gene_functions':gene_functions})

def show_gene_search(request, gene_search_pk):
    gene_search = GeneSearch.objects.get(pk=gene_search_pk)
    exp_sources = [e.name for e in gene_search.expression_source.all()]


    gene_functions = GeneFunction.objects.filter(gene=gene_search.gene, function__ontology__in=gene_search.ontology.all(), expression_source__in=gene_search.expression_source.all())
    #return render(request, 'show_gene_search.html',{'gene_search': gene_search,'gene_functions':gene_functions})
    
    # aggregate ####
    min_fdr=defaultdict(set)
    has_expression_source=defaultdict(set)
    for gf in gene_functions:
        min_fdr[gf.function.pk].add(gf.fdr)
        has_expression_source[gf.function.pk].add(gf.expression_source.name)
    min_fdr = {k:min(v) for k,v in min_fdr.iteritems()}
    
    data=[]
    for gf in gene_functions:
        data.append({
            'function': gf.function,
            'best_fdr': "%.2g" % min_fdr[gf.function.pk],
            'exp_sources': ( e in has_expression_source[gf.function.pk] for e in exp_sources)
        })
    ################

    #data.sort(key=itemgetter('best_fdr'))#sorting made by js in data_table

    return render(request, 'show_gene_search.html',{'gene_search': gene_search,'gene_functions':gene_functions, 'data': data , 'exp_sources': exp_sources})

class GeneAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Gene.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class FunctionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Function.objects.all()
        if self.q:
            ontology = self.forwarded.get('ontology', None)
            if ontology is not None:
                qs = qs.filter(ontology__pk=int(ontology))
            query1 = reduce(operator.and_, (Q(description__icontains=x) for x in self.q.split()))
            query2 = reduce(operator.and_, (Q(keyword__icontains=x) for x in self.q.split()))
            qs = qs.filter(query1 | query2)
        return qs

#from django.views.generic.list import ListView
#class RealtaListView(ListView):
#
#    model = Realta
#
#    def get_queryset(self):
#        #publisher = get_object_or_404(Publisher, name__iexact=self.args[0])
#        return Realta.objects.exclude(latitude=None)
#
#    def get_context_data(self, **kwargs):
#        context = super(RealtaListView, self).get_context_data(**kwargs)
#        return context
#
#class RealtaMarkersView(RealtaListView):
#    template_name="funcprod_app/realta_markers.tab"
#
