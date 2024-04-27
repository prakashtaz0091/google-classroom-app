from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    role_choices = [
        ('student', 'Student'),
        ('teacher', 'Teacher')
    ]
    role = models.CharField(max_length=7, choices=role_choices, default='student')


    def __str__(self):
        return self.user.username+" - "+self.role+"'s profile"




class Classroom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classes')



    def __str__(self):
        return self.name
    


class StudentClassroom(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='get_students')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='get_classes')
    


    def __str__(self):
        return self.student.username + " - " + self.classroom.name



class Post(models.Model):
    
    post_type_choices = [
        ('notice', 'Notice'),
        ('assignment', 'Assignment'),
        ('notes','Notes')
    ]


    title = models.CharField(max_length=100)
    description = models.TextField()
    post_type = models.CharField(max_length=10, choices=post_type_choices)
    created_at = models.DateTimeField(auto_now_add=True)

    post_file = models.FileField(upload_to='uploads/', null=True, blank=True)

    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='get_posts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='get_posts')

    def __str__(self):
        return self.title
