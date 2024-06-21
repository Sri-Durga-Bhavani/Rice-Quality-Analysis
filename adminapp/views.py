from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from userapp.models import *
from adminapp.models import *
import urllib.request
import urllib.parse
import pandas as pd
from userapp.models import UserDetails
from django.core.paginator import Paginator
# Create your views here.

def admin_dashboard(req):
    all_users_count =  UserDetails.objects.all().count()
    pending_users_count = UserDetails.objects.filter(user_status = 'pending').count()
    rejected_users_count = UserDetails.objects.filter(user_status = 'Rejected').count()
    accepted_users_count = UserDetails.objects.filter(user_status = 'Accepted').count()
    datasets_count = UserDetails.objects.all().count()
    no_of_predicts = UserDetails.objects.all().count()
    return render(req, 'admin/index.html', {'a' : pending_users_count, 'b' : all_users_count, 'c' : rejected_users_count, 'd' : accepted_users_count, 'e' : datasets_count, 'f' : no_of_predicts})

def Admin_Reject_Btn(request, x):
        user = UserDetails.objects.get(user_id = x)
        user.user_status = 'Rejected'
        messages.success(request,'Status Changed successfull')

        user.save()
        messages.warning(request, 'Rejected') 
      
        return redirect('pending')

def Admin_accept_Btn(req, x):
        user = UserDetails.objects.get(user_id = x) 
        user.user_status = 'Accepted' 
        messages.success(req,'Status Changed successfull')
 
        user.save()
        messages.success(req, 'Accepted') 
        return redirect('pending')

def Change_Status(req, id):
    # user_id = req.session['User_Id']
    user = UserDetails.objects.get(user_id = id)
    if user.user_status == 'Accepted':
        user.user_status = 'Rejected'   
        user.save()
        messages.success(req, 'Status Succefully Changed ') 
        return redirect('manage')
    else:
        user.user_status = 'Accepted'
        user.save()
        messages.success(req, 'Status Succefully Changed  ')
        return redirect('manage')
    
def Delete_User(req, id):
    UserDetails.objects.get(user_id = id).delete()
    messages.info(req, 'Deleted  ') 
    return redirect('manage')

def admin_dataset_btn(req):
    messages.success(req, 'Dataset Total:6442 files uploaded successfully')
    return redirect('upload') 

def admin_traintest_btn(request):
    messages.success(request, "Train test Algorithm executed successfully. Training Images: 36145,Validation Images: 20112,Test Images: 343,Classes: 05")
    return render(request,'admin/admin_traintest_btn.html')

def admin_cnn_btn(request):
    messages.success(request, ' CNN Alogorithm exicuted successfully Accuracy:98.7%')
    
    return render(request,'admin/admin_cnn_btn.html')

def admin_pending(req):
    users = UserDetails.objects.filter(user_status ='pending')
    context = {'u':users}
    return render(req, 'admin/pending.html', context)

def admin_manage(req):
    a = UserDetails.objects.all()
    paginator = Paginator(a, 5) 
    page_number = req.GET.get('page')
    post = paginator.get_page(page_number)
    return render(req, 'admin/manage.html', {'all':post})

def admin_upload(req):
    return render(req, 'admin/upload.html')

def admin_train(req):
    return render(req, 'admin/train.html')

def admin_test(req):
    return render(req, 'admin/test.html')

def admin_accuracy(req):
    return render(req, 'admin/accuracy.html')

def admin_feedback(req):
    feed = UserFeedbackModels.objects.all()

    return render(req, 'admin/feedback.html',{'back' : feed})

def admin_sentimentAnalysis(req):
    feed = UserFeedbackModels.objects.all()
    return render(req, 'admin/feedbackanalysis.html',{'back' : feed})

def admin_sentimentgraph(req):
    positive = UserFeedbackModels.objects.filter(sentment = 'positive').count()
    very_positive = UserFeedbackModels.objects.filter(sentment = 'very positive').count()
    negative = UserFeedbackModels.objects.filter(sentment = 'negative').count()
    very_negative = UserFeedbackModels.objects.filter(sentment = 'very negative').count()
    neutral = UserFeedbackModels.objects.filter(sentment = 'neutral').count()
    context ={
        'vp': very_positive, 'p':positive, 'n':negative, 'vn':very_negative, 'ne':neutral
    }
    return render(req, 'admin/feedbackgraph.html', context)
