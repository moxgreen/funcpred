# Create your views here.
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from dal import autocomplete
from .models import GeneSearch, Gene


class GeneSearchForm(forms.ModelForm):
    #gene = forms.ModelChoiceField(
    #    queryset=Gene.objects.all(),
    #    widget = autocomplete.ModelSelect2(url='dal-gene')
    #)
    class Meta:
        model = GeneSearch
        fields = ['gene','expression_source','ontology']
        widgets = {
                'gene': autocomplete.ModelSelect2(url='dal-gene')
        }

def index(request):
    #return HttpResponse('Hello from Python!')
    form = GeneSearchForm()
    return render(request, 'index.html',{'form': form})

class GeneAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Gene.objects.all()

        if self.q:
            qs = qs.filter(ensg__icontains=self.q)

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
