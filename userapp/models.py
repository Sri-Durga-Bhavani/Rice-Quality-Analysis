from django.db import models

# Create your models here.
class UserDetails(models.Model):
    user_id = models.AutoField(primary_key=True)
    Username = models.TextField(max_length=30, null=True)
    Email_id = models.EmailField(max_length=30, null = True)
    Image = models.FileField(upload_to='images/', null = True)
    Age = models.IntegerField(null = True)
    Contact = models.TextField(max_length='30', null = True)
    Password = models.TextField(max_length=30, null = True)
    Date_time = models.DateTimeField(auto_now=True, null = True)
    user_status=models.TextField(max_length=30,default='pending',null=True)
    user_feedback = models.TextField(max_length=1000,null=True)
    otp = models.IntegerField(null=True)
    Otp_Status = models.TextField(default = 'pending', max_length = 60, null = True)
    Last_Login_Time = models.TimeField(auto_now_add=True,null = True)
    Last_Login_Date = models.DateField(auto_now_add=True,null = True)
    No_Of_Times_Login = models.IntegerField(default = 0, null = True)
    Message =models.TextField(max_length=250,null=True)
    class  Meta:
        db_table = 'fire_detection_table'



class UserFeedbackModels(models.Model):
    feed_id = models.AutoField(primary_key=True)
    star_feedback = models.TextField(max_length=900)
    star_rating = models.IntegerField()
    star_Date = models.DateTimeField(auto_now_add=True, null=True)
    user_details = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    sentment = models.TextField(max_length=20,null=True)
    class Meta:
        db_table = 'feedback_table'

class Last_login(models.Model):
    Id = models.AutoField(primary_key = True)
    Login_Time = models.DateTimeField(auto_now = True, null = True)

    class Meta:
        db_table = "last_login"

class Dataset(models.Model):
   Data_id = models.AutoField(primary_key=True)
   Image = models.ImageField(upload_to='media/') 
   class Meta:
        db_table = "upload" 