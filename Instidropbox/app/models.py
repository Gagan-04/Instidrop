"""
Definition of models.
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_student=models.BooleanField(default=False, blank=True)
    is_faculty=models.BooleanField(default=False, blank=True)
    is_hod=models.BooleanField(default=False, blank=True)
    is_principal=models.BooleanField(default=False, blank=True)
    is_staff=models.BooleanField(default=False, blank=True)
    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Faculty(models.Model):
    Faculty_Id=models.CharField(max_length=10)
    Faculty_Name=models.CharField(max_length=50)
    DEPTS = [
    ('CSE', 'CSE'),
    ('MECH', 'MECH'),
    ('Civil', 'Civil'),
    ('ENC', 'ENC'),
    ('ISE', 'ISE'),
    ]
    Department=models.CharField(max_length=10,choices=DEPTS,default="CSE")
    DESIGNATIONS = [
    ('Principal', 'Principal'),
    ('Prof.', 'Professor'),
    ('HOD', 'HOD'),
    ('Asst.Prof.', 'Asst.Professor'),
    ('Asst.Prof.', 'Asso.Professor')
    ]
    Designation=models.CharField(max_length=20,choices=DESIGNATIONS,blank=True)
    Experience=models.IntegerField(help_text="Number of years",blank=True)
    Achievements=models.CharField(max_length=250,blank=True)
    Message=models.CharField(help_text="Message to students",max_length=250,blank=True)
    Contact=models.CharField(max_length=10,blank=True)
    Email=models.EmailField(max_length=50,blank=True)
    Photo=models.ImageField(upload_to='images/',blank=True)
    Place=models.TextField(max_length=100,blank=True)
    Created_Date=models.DateField(default=date.today,blank=True)

    def __str__(self):
        return self.Faculty_Name

class Faculty_subjects(models.Model):
   Faculty_Id=models.ForeignKey(Faculty)
   Subject=models.CharField(max_length=50,blank=True)
   Specialization=models.CharField(max_length=200,blank=True)
   Sub_notes=models.FileField(upload_to='documents/',blank=True)
   sub_Video=models.FileField(upload_to='videos/',blank=True)

   def __str__(self):
       return str(self.Subject)
   
class Students(models.Model):
    Student_Id=models.CharField(max_length=12)
    Student_Name=models.CharField(max_length=50)
    DEPTS = [
    ('CSE', 'CSE'),
    ('MECH', 'MECH'),
    ('Civil', 'Civil'),
    ('ENC', 'ENC'),
    ('ISE', 'ISE'),
    ]
    Department=models.CharField(max_length=10,choices=DEPTS,blank=True)
    Semester=models.PositiveIntegerField(blank=True)
    STATUSES=[
        ('Active','Active'),
        ('In Active','In Active'),
        ]
    Status=models.CharField(max_length=10,choices=STATUSES,blank=True,default="Active")
    Contact=models.CharField(max_length=10,blank=True)
    Email=models.EmailField(max_length=30,blank=True)
    def __str__(self):
        return str(self.Student_Name)+"_"+str(self.Student_Id)

class ReqTypes(models.Model):
    Req_Type_id=models.CharField(primary_key=True,max_length=25)
    Req_Type=models.CharField(max_length=25)
    
    def __str__(self):
        return self.Req_Type

class ReqDetails(models.Model):
    Req_Type=models.CharField(max_length=25)
    Req_details=models.CharField(max_length=250,blank=True)
    sender_id=models.CharField(max_length=10,blank=True)
    receiver_id=models.CharField(max_length=10,blank=True)
    Req_Status=models.CharField(max_length=20,default="Pending",blank=True)
    dateof_request=models.DateField(default=date.today,blank=True)
    dateof_update=models.DateField(default=date.today,blank=True)
    reply_details=models.CharField(max_length=250,blank=True)
    visibilty_sender_id=models.BooleanField(default=True,blank=True)
    document=models.FileField(upload_to='documents/',blank=True)
    visible_to_Hod=models.BooleanField(default=False,blank=True)
    visible_to_Principal=models.BooleanField(default=False,blank=True)
    def __str__(self):
        return str(self.Req_Type+"_")+str(self.sender_id)+"_to_"+str(self.receiver_id)












