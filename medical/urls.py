
from django.urls import path
from medical.views import consultation_create,consultation_edit,consultation_detail,index


urlpatterns = [
# Consultation
path('index',index,name='index'),
path('consultation/create/<int:appointment_id>',consultation_create,name='create_consultation'),
path('consultation/edit/<int:pk>',consultation_edit,name='consultation_edit'),
path('consultation/<int:pk>', consultation_detail,name='consultation_detail'),

]





# urlpatterns = [
#     path('', placeholder, name='placeholder'),
# ]