from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Avg
from .models import Module, Professor, Rating, ModuleInstance
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie

# sends the cookie to the client
@ensure_csrf_cookie
@api_view(['GET'])
def get_csrf_token(request):
    return HttpResponse("CSRF cookie set", status=200, content_type = "text/plain")

# registers user
@api_view(["POST"])
def register(request):
    # gets data from request
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    # validates
    if not (username and email and password):
        return HttpResponse("Missing credidentials", status=400, content_type = "text/plain")
    if (User.objects.filter(username = username)):
        return HttpResponse("Username exists", status=406, content_type = "text/plain")
    if (User.objects.filter(email = email)):
        return HttpResponse("Email exists", status=406, content_type = "text/plain")
    # creates new user using Django's User model
    user = User.objects.create_user(username = username, email = email, password = password)
    user.save()
    return HttpResponse("User created", status=201, content_type = "text/plain")

# logs in user
@api_view(["POST"])
def login_user(request):
    # gets data from request
    username = request.data.get("username")
    password = request.data.get("password")
    # validates
    if not (username and password):
        return HttpResponse("Missing credidentials", status=400, content_type = "text/plain")
    # authenticates using Django's build-in function
    user = authenticate(request, username=username, password=password)
    if user is None:
        return HttpResponse("Wrong username or password", status=401, content_type = "text/plain")
    # logs the user in using Django's build-in function
    login(request,user)
    return HttpResponse("Login was succesfull", status=200, content_type = "text/plain")

# logs out user
@api_view(["POST"])
def logout_user(request):
    # if user is logged in it logs them out using Django's build-in function
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse("Logout was succesfull", status=200, content_type = "text/plain")
    else:
        return HttpResponse("The user was not logged in", status=400, content_type = "text/plain")

# lists all module instances
@api_view(["GET"])
def list_instances(request):
    # gets all instances
    instances = ModuleInstance.objects.all()
    data = []
    # makes a dictionary for each instance and adds it to a list with all instances
    for instance in instances:
        # appends professor names of each instance in a list
        professor_names=[]
        all_professors = instance.professor.all()
        for prof in all_professors:
            professor_names.append(prof.full_name)
        instance_data = {"code": instance.module.code, "module": instance.module.name, "year": instance.year, "semester": instance.semester, "professors": professor_names}
        data.append(instance_data)
    return JsonResponse(data, safe=False, status=200)

# view ratings of all professors
@api_view(["GET"])
def view(request):
    # gets all professors
    professors = Professor.objects.all()
    if not professors:
        return HttpResponse("No professors available", status=404, content_type = "text/plain")
    data = []
    # finds all module instances for each professor and finds the average of their ratings
    for professor in professors:
        module_instances = ModuleInstance.objects.filter(professor=professor)
        ratings = list(Rating.objects.filter(module__in=module_instances).values_list("rating", flat=True))
        if ratings:
            average_rating = round(sum(ratings)/len(ratings))
        else:
            average_rating = 0
        # makes a dictionary for each professor and appends all the dictionaries in a list to return
        professor_data = {"full_name": professor.full_name, "average_rating": average_rating, "professor_id": professor.prof_id}
        data.append(professor_data)
    return JsonResponse(data,safe=False, status=200)

# view rating of a specific professor and module
@api_view(["GET"])
def average(request):
    # gets data from request
    professor_id = request.query_params.get("professor_id")
    module_code = request.query_params.get("module_code")
    # validates
    if not (professor_id and module_code):
        return HttpResponse("Missing Values", status=400, content_type = "text/plain")
    # tries to find all module instances with given professor and module and informs if not any exist
    professor = Professor.objects.filter(prof_id=professor_id).first()
    if professor is None:
        return HttpResponse("Did not find a professor with this ID", status=404)
    all_module_instances = ModuleInstance.objects.filter(professor = professor, module__code = module_code)
    if not all_module_instances:
        return HttpResponse("Did not found any modules with this code and professor id", status=404, content_type = "text/plain")
    # gets ratings of all module instances with specific professor and module and calculates their average
    ratings = list(Rating.objects.filter(module__in=all_module_instances).values_list("rating", flat=True))
    if ratings:
        average_rating = round(sum(ratings)/len(ratings))
    else:
        average_rating = 0
    module = Module.objects.filter(code = module_code).first()
    data = {"professor" : professor.full_name, "module": module.name, "average_rating": average_rating}
    return JsonResponse(data, status=200)

# rates specific module instance
@api_view(["POST"])
def rate(request):
    # gets data from request
    professor_id = request.data.get("professor_id")
    module_code = request.data.get("module_code")
    year = request.data.get("year")
    semester = request.data.get("semester")
    rating = request.data.get("rating")
    # validates
    if not (professor_id and module_code and year and semester and rating):
        return HttpResponse("Missing values", status=400, content_type = "text/plain")
    
    if not request.user.is_authenticated:
        return HttpResponse("You must login to rate", status=401, content_type = "text/plain")
    # gets module instance and check if it exists or if the user has already rated it
    professor = Professor.objects.filter(prof_id = professor_id).first()
    if professor is None:
        return HttpResponse("Could not find any module instances with these values", status=404, content_type = "text/plain")
    instance = ModuleInstance.objects.filter(professor = professor, module__code = module_code, year = year, semester = semester).first()
    if instance is None:
        return HttpResponse("Could not find any module instances with these values", status=404, content_type = "text/plain")
    if Rating.objects.filter(module=instance, user=request.user).exists():
        return HttpResponse("You have already rate this", status=401, content_type = "text/plain")
    else:
        # makes rating
        rate_object = Rating.objects.create(module=instance, user=request.user, rating=rating)
        rate_object.save()
        return HttpResponse("Rate Succesful", status=201, content_type = "text/plain")