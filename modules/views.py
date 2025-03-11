from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Avg
from .models import Module, Professor, Rating, ModuleInstance
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
@api_view(['GET'])
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})

@api_view(['POST'])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    if not (username and email and password):
        return HttpResponse("Missing credidentials", status=400, content_type = "text/plain")
    if (User.objects.filter(username = username)):
        return HttpResponse("Username exists", status=406, content_type = "text/plain")
    if (User.objects.filter(email = email)):
        return HttpResponse("Email exists", status=406, content_type = "text/plain")
    user = User.objects.create_user(username = username, email = email, password = password)
    user.save()
    return HttpResponse("User created", status=201, content_type = "text/plain")

@api_view(['POST'])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not (username and password):
        return HttpResponse("Missing credidentials", status=400, content_type = "text/plain")
    user = authenticate(request, username=username, password=password)
    if user is None:
        return HttpResponse("Wrong username or password", status=401, content_type = "text/plain")
    login(request,user)
    return HttpResponse("Login was succesfull", status=200, content_type = "text/plain")

@api_view(['POST'])
def logout_user(request):
    logout(request)
    return HttpResponse("Logout was succesfull", status=200, content_type = "text/plain")

@api_view(["GET"])
def list_instances(request):
    instances = ModuleInstance.objects.all()
    data = []
    for instance in instances:
        professor_names=[]
        all_professors = instance.professor.all()
        for prof in all_professors:
            professor_names.append(prof.full_name)
        instance_data = {"code": instance.module.code, "module": instance.module.name, "year": instance.year, "semester": instance.semester, "professors": professor_names}
        data.append(instance_data)
    return JsonResponse(data, safe=False, status=200)

@api_view(["GET"])
def view(request):
    professors = Professor.objects.all()
    if not professors:
        return HttpResponse("No professors available", status=404, content_type = "text/plain")
    data = []
    for professor in professors:
        module_instances = ModuleInstance.objects.filter(professor=professor)
        agg = Rating.objects.filter(module__in=module_instances).aggregate(avg_rating=Avg('rating'))
        average_rating = agg["avg_rating"] or 0
        final_average = round(average_rating)
        professor_data = {"full_name": professor.full_name, "average_rating": final_average, "professor_id": professor.prof_id}
        data.append(professor_data)
    return JsonResponse(data,safe=False, status=200)

@api_view(["GET"])
def average(request):
    professor_id = request.query_params.get("professor_id")
    module_code = request.query_params.get("module_code")
    if not (professor_id and module_code):
        return HttpResponse("Missing Values", status=400, content_type = "text/plain")
    try:
        professor = Professor.objects.filter(prof_id=professor_id).first()
    except Professor.DoesNotExist:
        return HttpResponse("Did not find a professor with this ID", status=404)
    all_module_instances = ModuleInstance.objects.filter(professor = professor, module__code = module_code)
    if not all_module_instances:
        return HttpResponse("Did not found any modules with this code and professor id", status=404, content_type = "text/plain")
    agg = Rating.objects.filter(module__in=all_module_instances).aggregate(avg_rating=Avg('rating'))
    average_rating = agg["avg_rating"] or 0
    final_average = round(average_rating)
    module = Module.objects.filter(code = module_code).first()
    data = {"professor" : professor.full_name, "module": module.name, "average_rating": final_average}
    return JsonResponse(data, status=200)

@api_view(['POST'])
def rate(request):

    professor_id = request.data.get("professor_id")
    module_code = request.data.get("module_code")
    year = request.data.get("year")
    semester = request.data.get("semester")
    rating = request.data.get("rating")

    if not (professor_id and module_code and year and semester and rating):
        return HttpResponse("Missing values", status=400, content_type = "text/plain")
    
    if not request.user.is_authenticated:
        return HttpResponse("You must login to rate", status=401, content_type = "text/plain")
    
    professor = Professor.objects.filter(prof_id = professor_id).first()
    instance = ModuleInstance.objects.filter(professor = professor, module__code = module_code, year = year, semester = semester).first()
    if instance is None:
        return HttpResponse("Could not find any module instances with these values", status=404, content_type = "text/plain")
    
    if Rating.objects.filter(module=instance, user=request.user).exists():
        return HttpResponse("You have already rate this", status=401, content_type = "text/plain")
    else:
        rate_object = Rating.objects.create(module=instance, user=request.user, rating=rating)
        rate_object.save()
        return HttpResponse("Rate Succesful", status=201, content_type = "text/plain")