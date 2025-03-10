from django.http import HttpResponse

def home(request):
    return HttpResponse("Hola, este es el home de MyFinPlanner")
    