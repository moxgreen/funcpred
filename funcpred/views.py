# Create your views here.
from django.views.generic.list import ListView
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, Group

def my_view(request):
        my_object = get_object_or_404(MyModel, pk=1)


from .models import Realta

class RealtaListView(ListView):

    model = Realta

    def get_queryset(self):
        #publisher = get_object_or_404(Publisher, name__iexact=self.args[0])
        return Realta.objects.exclude(latitude=None)

    def get_context_data(self, **kwargs):
        context = super(RealtaListView, self).get_context_data(**kwargs)
        return context

class RealtaMarkersView(RealtaListView):
    template_name="funcprod_app/realta_markers.tab"

def redirect_user_to_realta_admin(request):
    try:
        realta = get_object_or_404(Realta, owner=request.user)
        return redirect(realta.get_admin_url())
    except Realta.MultipleObjectsReturned:
        return redirect("/admin/funcprod_app/realta/")

def homepage(request):
    if request.user.is_staff:
        return redirect("/admin/funcprod_app/realta/")
    else:
        return redirect("/funcprod_app/")
        
