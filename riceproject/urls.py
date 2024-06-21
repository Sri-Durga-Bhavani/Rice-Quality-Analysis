"""
URL configuration for riceproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from userapp import views as user_view
from adminapp import views as admin_view
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    # User Views
    # ----------

    path('', user_view.user_index, name = 'index'),
    path('about/', user_view.user_about, name = 'about'),
    path('service/', user_view.user_service, name = 'service'),
    path('register/', user_view.user_register, name = 'register'),
    path('alogin/', user_view.user_admin, name = 'admin'),
    path('login/', user_view.user_user, name = 'user'),
    path('otp/', user_view.user_otp, name='otp'),
    path('service/', user_view.user_service, name = 'service'),
    path('contact/', user_view.user_contact, name = 'contact'),
    path('dashboard/', user_view.user_dashboard, name = 'dashboard'),
    path('myprofile/', user_view.user_myprofile, name = 'myprofile'),
    path('detection/', user_view.user_detection, name = 'detection'),
    path('feedback/', user_view.user_feedback, name = 'feedback'),
    path('result/', user_view.user_result, name = 'result'),
    path('userlogout/', user_view.userlogout, name = 'userlogout'),


    # Admin views
    # -----------
    path('abashboard/', admin_view.admin_dashboard, name = 'adashboard'),
    path('pending/', admin_view.admin_pending, name = 'pending'),
    path('manage/', admin_view.admin_manage, name = 'manage'),
    path('upload/', admin_view.admin_upload, name = 'upload'),
    path('train/', admin_view.admin_train, name = 'train'),
    path('test/', admin_view.admin_test, name = 'test'),
    path('accuracy/', admin_view.admin_accuracy, name = 'accuracy'),
    path('afeedback/', admin_view.admin_feedback, name = 'afeedback'),
    path('feedbackanalysis/', admin_view.admin_sentimentAnalysis, name = 'feedbackanalysis'),
    path('feedbackgraph/', admin_view.admin_sentimentgraph, name = 'feedbackgraph'),
    path('admin-change-status/<int:id>',admin_view.Change_Status, name ='change_status'),
    path('admin-delete/<int:id>',admin_view.Delete_User, name ='delete_user'),
    path('adminrejectbtn/<int:x>', admin_view.Admin_Reject_Btn, name='adminreject'),
    path('adminacceptbtn/<int:x>', admin_view.Admin_accept_Btn, name='adminaccept'),
    path('admin_dataset_btn',admin_view.admin_dataset_btn,name='admin_dataset_btn'),
    path('admin_cnn_model',admin_view.admin_cnn_btn,name='admin_cnn_model'),
    path('admin_traintest_btn',admin_view.admin_traintest_btn,name='admin_traintest_btn'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
