# Create your views here.
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from dal import autocomplete
from .models import GeneSearch, Gene, GeneFunction


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
                'expression_source': forms.CheckboxSelectMultiple(),
                'ontology': forms.CheckboxSelectMultiple()
        }

def index(request):
    #return HttpResponse('Hello from Python!')
    if request.method == 'POST':
        form = GeneSearchForm(request.POST)
        if form.is_valid():
            gene_search=form.save()
        redirect("show_gene_search", gene_search=gene_search.pk)
    else:
        form = GeneSearchForm()
    return render(request, 'index.html',{'form': form})

def show_gene_search(request, gene_search_pk):
    gene_search = GeneSearch.objects.get(pk=gene_search_pk)
    gene_functions = GeneFunction.objects.filter(gene=gene_search.gene, function__ontology__in=gene_search.ontology.all(), expression_source__in=gene_search.expression_source.all())
    return render(request, 'show_gene_search.html',{'gene_search': gene_search,'gene_functions': gene_functions})



class GeneAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Gene.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

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
