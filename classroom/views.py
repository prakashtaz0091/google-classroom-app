from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Classroom, StudentClassroom, Post
from .decorators import has_to_be_teacher
from django.views.decorators.http import require_POST

# Create your views here.
@login_required
def home(request):

    if request.user.profile.role=="teacher":
        classrooms = Classroom.objects.filter(user = request.user)
        context ={
            'classrooms':classrooms,
        }



    else:
        joined_classrooms = StudentClassroom.objects.filter(student=request.user)
        available_classrooms = Classroom.objects.all()

        joined_classrooms_names = [classroom.classroom.name for classroom in joined_classrooms] #getting all classrooms name of joined classrooms
        available_classrooms = available_classrooms.exclude(name__in=joined_classrooms_names) #filtering those classrooms where student haven't joined yet

        context ={
            'classrooms':available_classrooms,
            'joined_classrooms': joined_classrooms    
        }


    return render(request,"classroom/home.html", context)

@has_to_be_teacher
def delete_class(request, class_id):
    classroom = Classroom.objects.get(id=class_id)
    classroom.delete()
    messages.success(request, "Classroom deleted successfully")
    return redirect("classroom:home")



@has_to_be_teacher
def enter_class_teacher(request, class_id):

    classroom = Classroom.objects.get(id=class_id)

    classroom_posts = Post.objects.filter(classroom=classroom).filter(user=request.user)




    context = {
        'classroom': classroom,
        'classroom_posts': classroom_posts
    }

    return render(request,"classroom/teacher_class.html", context)


@require_POST
@has_to_be_teacher
def create_post(request):

    if request.method=="POST":
        data = request.POST
        post_title = data.get("title")
        post_desc = data.get("description")
        post_type = data.get("post_type")
        classroom_id = data.get("classroom_id")

        classroom = Classroom.objects.get(id=classroom_id)

        post_file = request.FILES.get('file')


        Post.objects.create(
            title = post_title,
            description = post_desc,
            post_type = post_type,
            post_file = post_file,
            classroom = classroom,
            user = request.user
        )
        
        messages.success(request, "Post created successfully")



    return redirect("classroom:home")



@has_to_be_teacher
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()

    messages.success(request, "Post deleted successfully")

    return redirect("classroom:home")



def login_view(request):

    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("classroom:home")
        else:
            messages.error(request, "Invalid credentials, please try again with correct credentials")
            return render(request, 'classroom/login.html')


    return render(request, 'classroom/login.html')



def register_view(request):


    if request.method=="POST":
        
        #account info
        username = request.POST.get('username')



        if len(username)<4:
            messages.error(request, "Username too short")
            return render(request, 'classroom/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists, Please choose another username")
            return render(request, 'classroom/register.html')


        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')


        if len(password) < 4:
            messages.error(request, "Password too short")
            return render(request, 'classroom/register.html')


        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'classroom/register.html')


        role = request.POST.get('role')

        #personal info
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        
        #creating basic user
        user = User.objects.create_user(username=username, password=password)
        user.save()
        
        #setting user's first_name and last_name as personal info
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        #creating profile
        profile = Profile.objects.create(user=user, role=role)
        profile.save()

        messages.success(request, "Account created successfully")
        return redirect("classroom:login_view")
    
    return render(request, "classroom/register.html")



def logout_view(request):
    logout(request)
    return redirect("classroom:login_view")


@has_to_be_teacher
def create_class(request):

    if request.method=="POST":
        name = request.POST.get("name")
        description = request.POST.get("description")


        Classroom.objects.create(
            name = name,
            description = description,
            user = request.user
        )
        
        messages.success(request, "Classroom created successfully")

        return redirect("classroom:home")




    return render(request, "classroom/create_class.html")




def join_class(request, class_id):

    try:

        classroom = Classroom.objects.get(id=class_id)

    except Classroom.objects.DoesNotExist():
        messages.error(request, "Classroom does not exist, please try joining another classroom")

        return redirect("classroom:home")

    StudentClassroom.objects.create(
        student = request.user,
        classroom = classroom
    )

    messages.success(request, "Joined classroom successfully")


    return redirect("classroom:home")
    
    # return render(request,"classroom/join_class.html")




def enter_class_student(request, class_id):
    

    classroom = Classroom.objects.get(id=class_id)

    posts = Post.objects.filter(classroom=classroom)
    
    context  = {
        'classroom': classroom,
        'posts':posts,
    }

    return render(request, "classroom/student_class.html", context)