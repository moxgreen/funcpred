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

from .models import GeneSearch, FunctionSearch, Gene, GeneFunction, Function, Ontology, Session

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

class QuickGeneSearchForm(forms.ModelForm):
    #gene = forms.ModelChoiceField(
    #    queryset=Gene.objects.all(),
    #    widget = autocomplete.ModelSelect2(url='dal-gene')
    #)
    class Meta:
        model = GeneSearch
        fields = ['gene']
        labels = {
            'gene': "",
        }
        widgets = {
                'gene': autocomplete.ModelSelect2(url='dal-gene'),
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
    form = QuickGeneSearchForm(request.POST)
    if request.method == 'POST':
        s = Session.objects.get_or_create(session_id=request.session._get_or_create_session_key(), ip_address=request.META.get('REMOTE_ADDR'))
        form = QuickGeneSearchForm(request.POST, initial={"session": s})
        if form.is_valid():
            gene_search=form.save()
            gene_search.expression_source.add(1)

            return redirect("show_gene_search", gene_search_pk=gene_search.pk)
    return render(request, 'home.html',{'form': form})

def browse_ontologies(request):
    ontologies=Ontology.objects.all()
    return render(request, 'browse_ontologies.html',{'ontologies': ontologies})

def browse_functions(request, ontology_pk):
    functions=Function.objects.filter(ontology=int(ontology_pk))
    return render(request, 'browse_functions.html',{'functions': functions})

def make_basic_function_search(request, function_pk):
    s = Session.objects.get_or_create(session_id=request.session._get_or_create_session_key(), ip_address=request.META.get('REMOTE_ADDR'))
    fs=FunctionSearch.objects.create(function=Function.objects.get(pk=int(function_pk)), session=s[0])
    fs.expression_source.add(1)

    return show_function_search(request,function_search_pk=fs.pk)
    


def gene_search(request):
    if request.method == 'POST':
        s = Session.objects.get_or_create(session_id=request.session._get_or_create_session_key(), ip_address=request.META.get('REMOTE_ADDR'))
        form = GeneSearchForm(request.POST, initial={"session": s})
        if form.is_valid():
            gene_search=form.save()
            return redirect("show_gene_search", gene_search_pk=gene_search.pk)
    else:
        form = GeneSearchForm()
    return render(request, 'search_gene.html',{'form': form})

def function_search(request):
    if request.method == 'POST':
        s = Session.objects.get_or_create(session_id=request.session._get_or_create_session_key(), ip_address=request.META.get('REMOTE_ADDR'))
        form = FunctionSearchForm(request.POST, initial={"session": s})
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
            'known': gf.known,
            'best_fdr': "%.2g" % min_fdr[gf.gene.pk],
        })
        if len(exp_sources)>1:
           data[-1]['exp_sources'] = [ e in has_expression_source[gf.gene.pk] for e in exp_sources]
    ################

    exp_sources_top=exp_sources
    if len(exp_sources)==1:
        exp_sources=[]

    return render(request, 'show_function_search.html',{'function_search': function_search,'gene_functions':gene_functions, 'data': data , 'exp_sources_top': exp_sources_top, 'exp_sources': exp_sources})

def show_gene_search(request, gene_search_pk):
    gene_search = GeneSearch.objects.get(pk=gene_search_pk)
    exp_sources = [e.name for e in gene_search.expression_source.all()]


    gene_functions = GeneFunction.objects.filter(gene=gene_search.gene, expression_source__in=gene_search.expression_source.all())
    if gene_search.ontology.count():
        gene_functions = gene_functions.filter(function__ontology__in=gene_search.ontology.all())
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
            'known': gf.known,
            'best_fdr': "%.2g" % min_fdr[gf.function.pk],
        })
        if len(exp_sources)>1:
            data[-1]['exp_sources'] = [ e in has_expression_source[gf.function.pk] for e in exp_sources]
    ################

    exp_sources_top=exp_sources
    if len(exp_sources)==1:
        exp_sources=[]

    #data.sort(key=itemgetter('best_fdr'))#sorting made by js in data_table

    return render(request, 'show_gene_search.html',{'gene_search': gene_search,'gene_functions':gene_functions, 'data': data , 'exp_sources': exp_sources,'exp_sources_top':exp_sources_top})

class GeneAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Gene.objects.all()
        q=self.q
        q=q.strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(ensg__icontains=q))
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
