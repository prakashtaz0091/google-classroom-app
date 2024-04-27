from django.urls import path
from . import views

app_name = 'classroom'

urlpatterns = [
    path('',views.home, name="home"),

    #accounts
    path('accounts/login/',views.login_view, name="login_view"),
    path('accounts/register/',views.register_view, name="register_view"),
    path('accounts/logout/',views.logout_view, name="logout_view"),


    #classroom
    path('create_class/',views.create_class, name="create_class"),
    path('delete_class/<int:class_id>/',views.delete_class, name="delete_class"),
    path('join_class/<int:class_id>/',views.join_class, name="join_class"),
    path('enter_class/teacher/<int:class_id>/',views.enter_class_teacher, name="enter_class_teacher"),
    path('enter_class/student/<int:class_id>/',views.enter_class_student, name="enter_class_student"),


    #post
    path('create_post/',views.create_post, name="create_post"),
    path('delete_post/<int:post_id>/',views.delete_post, name="delete_post"),







]
