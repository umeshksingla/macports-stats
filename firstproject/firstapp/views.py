import json

from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Port, Submission, PortIndex

def index(request):
    return render(request, 'firstapp/index.html', {'home': "Hello, world. You're at the firstapp index."})


# properties of a port
def detail(request, port_id):
    try:
        port = Port.objects.get(pk=port_id)
    except Port.DoesNotExist:
        raise Http404("Port does not exist")
    return render(request, 'firstapp/detail.html', {'port': port})

@csrf_exempt
def get_submissions(request):
    if request.method == 'POST':
        submission = request.body.decode("utf-8").split('=', 1)[1]
        submission = json.loads(submission)
        s = Submission(data=submission)
        s.save()
    return HttpResponse("Success getting user's submission.")


@csrf_exempt
def get_portindex(request):
    if request.method == 'POST':
        portindex = request.body.decode("utf-8")
        portindex = json.loads(portindex)
        p = PortIndex(data=portindex)
        p.save()
    return HttpResponse("Success getting portindex.")