from django.shortcuts import render, redirect
from django.contrib import messages
import urllib.request
import urllib.parse
from django.shortcuts import render,redirect
from django.contrib import messages
from userapp.models import *
import random
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import default_storage
import urllib.request
import urllib.parse
#load the model
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input
import numpy as np
from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.applications.inception_v3 import InceptionV3
#from keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.models import load_model

from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img
from tensorflow.keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt



# Create your views here.
def user_index(req):
    return render(req, 'user/index.html')

def user_about(req):
    return render(req, 'user/about.html')

def user_service(req):
    return render(req, 'user/service.html')

def sendSMS(user, otp, mobile):
    data = urllib.parse.urlencode({
        'username': 'Codebook',
        'apikey': '56dbbdc9cea86b276f6c',
        'mobile': mobile,
        'message': f'Hello {user}, your OTP for account activation is {otp}. This message is generated from https://www.codebook.in server. Thank you',
        'senderid': 'CODEBK'
    })
    data = data.encode('utf-8')
    # Disable SSL certificate verification
    # context = ssl._create_unverified_context()
    request = urllib.request.Request("https://smslogin.co/v3/api.php?")
    f = urllib.request.urlopen(request, data)
    return f.read()

def user_register(req):
    if req.method == "POST":
        username = req.POST.get('User_name')
        email = req.POST.get('email_address')
        phone = req.POST.get('Phone_number')
        password = req.POST.get('pass')
        image = req.FILES['image']
        print(username, email,  phone, password, image, 'data')
        image = req.FILES['image']
        otp = str(random.randint(1000, 9999)) 
        print(otp, 'generated otp')
        # email messages
        try:
            user_data = UserDetails.objects.get(Email_id = email)
            messages.info(req, 'mail already registered')
            return redirect('register')
        except:
            mail_message = f'Registration Successfully\n Your 4 digit Pin is below\n {otp}'
            print(mail_message)
            send_mail("Student Password", mail_message , settings.EMAIL_HOST_USER, [email])
            # text message
            sendSMS(username, otp, phone)
        
            UserDetails.objects.create(otp = otp, Username = username, Email_id = email,  Contact = phone, Password = password, Image = image)
            req.session['Email_id'] = email
            messages.success(req, 'Your account was created..')

            return redirect('otp')
    return render(req, 'user/register.html')

def user_admin(req):
    admin_email = 'admin@gmail.com'
    admin_password = 'admin'
    if req.method == 'POST':
        admin_e = req.POST.get('adminname')
        admin_p = req.POST.get('adminpass')
        if (admin_e == admin_email and admin_p == admin_password):
            messages.success(req,'login successfull')
            return redirect('adashboard')
        else:
            messages.error(req,'You are trying to loging with wrong details..')
            return redirect('admin')
    return render(req, 'user/admin.html')

def user_otp(request):
    user_id = request.session['Email_id']
    user =UserDetails.objects.get(Email_id = user_id)
    messages.success(request, 'OTP  Sent successfully')
    print(user_id)
    print(user, 'user avilable')
    print(type(user.otp))
    print(user. otp, 'creaetd otp')   
    if request.method == 'POST':
        u_otp = request.POST.get('otp')
        u_otp = int(u_otp)
        print(u_otp, 'enter otp')
        if u_otp == user.otp:
            print('if')
            user.Otp_Status  = 'verified'
            user.save()
            messages.success(request, 'OTP  verified successfully')
            return redirect('user')
        else:
            print('else')
            messages.error(request, 'Invalid OTP  ') 
            return redirect('otp')
    return render(request, 'user/otp.html')

def user_user(request):
    if request.method == 'POST':
        email = request.POST.get('email_address')
        password = request.POST.get('pass')
        print(email, password)
        try:
            user = UserDetails.objects.get(Email_id = email, Password = password)
            print(user)
            request.session ['user_id'] = user.user_id
            a = request.session['user_id']
            print(a)
            
            if user.Password ==  password :
                if user.user_status == 'Accepted':
                    if user.Otp_Status == 'verified':
                        messages.success(request,'login successfull')
                        request.session['user_id'] = user.user_id
                        print('login sucessfull')
                        user.No_Of_Times_Login += 1
                        user.save()
                        return redirect('dashboard')
                    else:
                         return redirect('otp')
                elif user.Password ==  password and user.user_status == 'Rejected':
                    messages.warning(request,"you account is rejected")
                else:
                    messages.info(request,"your account is in pending")
            else:
                 messages.error(request,'Login credentials was incorrect...')    
        except:
            print(';invalid credentials')
            print('exce ')
            return redirect('user')
    return render(request, 'user/user.html')

def user_contact(req):
    return render(req, 'user/contact.html')

def user_dashboard(req):
    prediction_count =  UserDetails.objects.all().count()
    user_id = req.session["user_id"]
    user = UserDetails.objects.get(user_id = user_id)
    return render(req, 'user/dashboard.html', {'predictions' : prediction_count, 'la' : user})

def user_myprofile(request):
    views_id = request.session['user_id']
    user = UserDetails.objects.get(user_id = views_id)
    if request.method =='POST':
        username = request.POST.get('user_name')
        email = request.POST.get('email_address')
        phone = request.POST.get('Phone_number')
        password = request.POST.get('pass')
        date = request.POST.get('date')
        print(username, email,  phone, password, date,  'data')

        user.Username = username
        user.Email_id = email
        user.Contact = phone
        user.Password = password

        if len(request.FILES)!=0:
            image = request.FILES['image']
            user.Image = image
            user.Username = username
            user.Email_id = email
            user.Contact = phone
            user.Password = password
            user.save()
            messages.success(request, 'Updated Successfully...!')

        else:
            user.Username = username
            user.Email_id = email
            user.Contact = phone
            user.Password = password
            user.save()
            messages.success(request, 'Updated Successfully...!')

    return render(request, 'user/myprofile.html', {'i':user})

model = load_model('Rice_Image_Dataset/rice_model.h5')

ref={
     0:'Arborio', 
      1:'Basmati', 
     2:'Ipsala', 
     3:'Jasmine', 
     4:'Karacadag'
     }

def prediction(path):
  img = image.load_img(path, target_size=(224, 224))
  i = image.img_to_array(img)
  i = np.expand_dims(i, axis=0)
  img = preprocess_input(i)
  pred = np.argmax(model.predict(img), axis=1)
  return ref[pred[0]]


def user_detection(request):
    result = {"message": "No image uploaded"}  # Initialize the result as a dictionary
    uploaded_image_url = None

    if request.method == "POST" and 'img' in request.FILES:
        uploaded_image = request.FILES['img']
        Dataset.objects.create(Image= uploaded_image)
        file_path = default_storage.save(uploaded_image.name, uploaded_image)
        path = settings.MEDIA_ROOT + '/' + file_path
        uploaded_image_url = default_storage.url(file_path)
        result = prediction(path)  # Assuming prediction() returns a dictionary
        request.session['result'] = result
        request.session['uploaded_image_url']=uploaded_image_url
        messages.success(request,'Uploaded image successfully')
        return redirect('result')
    return render(request, 'user/detection.html', {'result': result, 'uploaded_image_url': uploaded_image_url})

def user_result(request):
    result = request.session.get('result', {"message": "No result available"})
    uploaded_image_url = request.session.get('uploaded_image_url', None)
    messages.success(request,'Predicted 98%')# Provide a default value (None in this case)
    return render(request, 'user/result.html', {'result': result, 'uploaded_image_url': uploaded_image_url})

def user_feedback(request):
    views_id = request.session['user_id']
    user = UserDetails.objects.get(user_id = views_id)
    if request.method == 'POST':
        u_feedback = request.POST.get('feedback')
        u_rating = request.POST.get('rating')
        if not user_feedback:
            return redirect('')
        sid=SentimentIntensityAnalyzer()
        score=sid.polarity_scores(u_feedback)
        sentiment=None
        if score['compound']>0 and score['compound']<=0.5:
            sentiment='positive'
        elif score['compound']>=0.5:
            sentiment='very positive'
        elif score['compound']<-0.5:
            sentiment='very negative'
        elif score['compound']<0 and score['compound']>=-0.5:
            sentiment='negative'
        else :
            sentiment='neutral'
        messages.success(request,'Feedback sent successfully')

        print(sentiment)
        user.star_feedback=u_feedback
        user.star_rating = u_rating
        user.save()
        UserFeedbackModels.objects.create(user_details = user, star_feedback = u_feedback, star_rating = u_rating, sentment= sentiment)
    rev=UserFeedbackModels.objects.filter()
    return render(request, 'user/feedback.html')


def userlogout(request):
    view_id = request.session["user_id"]
    user = UserDetails.objects.get(user_id = view_id) 
    t = time.localtime()
    user.Last_Login_Time = t
    current_time = time.strftime('%H:%M:%S', t)
    user.Last_Login_Time = current_time
    current_date = time.strftime('%Y-%m-%d')
    user.Last_Login_Date = current_date
    user.save()
    messages.info(request, 'You are logged out..')
    # print(user.Last_Login_Time)
    # print(user.Last_Login_Date)
    return redirect('user')

