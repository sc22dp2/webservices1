import requests
session = requests.Session()

def get_csrf():
    uri = "http://127.0.0.1:8000/csrf/"
    try:
        rensponse = session.get(uri)
        if rensponse.status_code == 200:
            csrf_token = session.cookies.get("csrftoken", None)
            if not csrf_token:
                print("csrf token error")
        else:
            print("csrf error")
    except:
        print("csrf error")

def register():
    global session
    print("Creating New User:")
    username = input("Username:")
    email = input("Email:")
    password = input("Password:")
    data = {"username":username, "email":email, "password":password}
    get_csrf()
    csrf_token = session.cookies.get("csrftoken", "")
    headers = {"X-CSRFToken": csrf_token}
    uri = "http://127.0.0.1:8000/register/"
    try:
        response = session.post(uri, json = data, headers = headers)
        if response.status_code == 201:
            print("The registration was succesfull")
        else:
            print("The registration failed:" + response.text)
    except requests.RequestException as e:
        print("Error")

def login(url):
    global session
    print("Login User:")
    username = input("Username:")
    password = input("Password:")
    data = {"username":username, "password":password}
    uri = "http://127.0.0.1:8000/login/"
    get_csrf()
    csrf_token = session.cookies.get("csrftoken", "")
    headers = {"X-CSRFToken": csrf_token}
    try:
        response = session.post(uri, json = data, headers = headers)
        if response.status_code == 200:
            print("The login was succesfull")
        else:
            print("The login failed:" + response.text)
    except:
        print("Connection Error")

def logout():
    global session
    uri = "http://127.0.0.1:8000/logout/"
    get_csrf()
    csrf_token = session.cookies.get("csrftoken", "")
    headers = {"X-CSRFToken": csrf_token}
    try:
        response = session.post(uri, headers = headers)
        if response.status_code == 200:
            print("The logout was succesfull")
        else:
            print("The logout failed:" + response.text)
    except:
        print("Connection Error")

def list_instances():
    uri = "http://127.0.0.1:8000/list/"
    try:
        response = session.get(uri)
        if response.status_code == 200:
            data = response.json()
            if not data:
                print("There are not any module instances available")
            else:
                print("code | name | year | semester | professors\n")
                for instance in data:
                    code = instance["code"]
                    module = instance["module"]
                    year = instance["year"]
                    semester = instance["semester"]
                    professors = instance["professors"]
                    print(f"{code} | {module} | {year} | {semester} | {professors}\n")
        else:
            print("Error:" + response.text)
    except:
         print("Error")

def to_stars(rating):
    stars = ""
    for i in range (0 ,rating):
        stars = stars + "*"
    return stars

def view():
    uri = "http://127.0.0.1:8000/view/"
    try:
        response = session.get(uri)
        if response.status_code == 200:
            data = response.json()
            for instance in data:
                full_name = instance["full_name"]
                rating = instance["average_rating"]
                star_rating = to_stars(rating)
                professor_id = instance["professor_id"]
                print(f"The rating of Professor {full_name}({professor_id}) is {star_rating}")
        else:
            print("Error:" + response.text)
    except:
         print("Error")

def average(professor_id, module_code):
    uri = f"http://127.0.0.1:8000/average/?professor_id={professor_id}&module_code={module_code}"
    data = {"professor_id": professor_id, "module_code": module_code}
    try:
        response = session.get(uri)
        data = response.json()
        if response.status_code == 200:
            full_name = data["professor"]
            module = data["module"]
            rating = data["average_rating"]
            star_rating = to_stars(rating)
            if rating == 0:
                print(f"There is no rating yet for {full_name} in module {module}")
            else:
                print(f"The rating of {full_name} {(professor_id)} in module {module} {(module_code)} is {star_rating}")
        else:
            print("Error:" + response.text)
    except:
        print("Error")

def rate(professor_id, module_code, year, semester, rating):
    uri = "http://127.0.0.1:8000/rate/"
    data = {"professor_id": professor_id, "module_code": module_code, "year": year, "semester": semester, "rating": rating}
    get_csrf()
    csrf_token = session.cookies.get("csrftoken", "")
    headers = {"X-CSRFToken": csrf_token}
    try:
        year = int(year)
        semester = int(semester)
        rating = int(rating)
    except:
        ("<Year>, <Semester> and <Rating> should be integers")
    if (rating > 5) or (rating < 1):
        print("<Rating> should be an integer between 1-5")
        return
    try:
        response = session.post(uri, json=data, headers = headers)
        if response.status_code == 201:
            print("Rating was successfull")
        else:
            print("Error:" + response.text)
    except:
        print("Exception occurred:")
       
def main():
    while True:
        command = input("Enter command:")
        command_parts = command.split()
        action = command_parts[0]
        if (action == "register"):
            if (len(command_parts) != 1):
                print("Incorrect command usage. Please try: register")
            else:
                register()
        elif (action == "login"):
            if (len(command_parts) != 2):
                print("Incorrect command usage. Please try: login <url>")
            else:
               login(command_parts[1])
        elif (action == "logout"):
            if (len(command_parts) != 1):
                print("Incorrect command usage. Please try: logout")
            else:
                logout()
        elif (action == "list"):
            if (len(command_parts) != 1):
                print("Incorrect command usage. Please try: list")
            else:
                list_instances()
        elif (action == "view"):
            if (len(command_parts) != 1):
                print("Incorrect command usage. Please try: view")
            else:
                view()
        elif (action == "average"):
            if (len(command_parts) != 3):
                print("Incorrect command usage. Please try: average <professor_id> <module_code>")
            else:
                average(command_parts[1], command_parts[2])
        elif (action == "rate"):
            if (len(command_parts) != 6):
                print("Incorrect command usage. Please try: rate <professor_id> <module_code> <year> <semester> <rating>")
            else:
                rate(command_parts[1], command_parts[2],command_parts[3], command_parts[4],command_parts[5])
        else:
            print("Wrong command")

if __name__ == "__main__":
    main()