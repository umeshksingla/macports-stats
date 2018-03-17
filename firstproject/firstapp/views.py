from django.shortcuts import render
from django.http import Http404

from .models import Port

def index(request):
    return render("Hello, world. You're at the firstapp index.")

# properties of a port
def detail(request, port_id):
	try:
		port = Port.objects.get(pk=port_id)
	except Port.DoesNotExist:
		raise Http404("Port does not exist")
	return render(request, 'firstapp/detail.html', {'port': port})