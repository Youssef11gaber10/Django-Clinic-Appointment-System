
from django.urls import path
from medical.views import consultation_create,consultation_edit,consultation_detail,index,prescription_create,prescription_edit,add_test,edit_test,view_summary



urlpatterns = [
# Consultation
path('index',index,name='index'),
path('consultation/create/<int:appointment_id>',consultation_create,name='create_consultation'),
path('consultation/edit/<int:pk>',consultation_edit,name='consultation_edit'),
path('consultation/<int:pk>', consultation_detail,name='consultation_detail'),
#prescription
path('prescription/create/<int:consultation_id>',prescription_create,name='create_prescription'),
path('prescription/edit/<int:pk>',prescription_edit,name='edit_prescription'),
#requesttest
path('test/add/<int:consultation_id>',add_test,name='add_test'),
path('test/edit/<int:pk>',edit_test,name='edit_test'),
#
 path("consultation/summary/<int:pk>", view_summary, name="view_summary"),







]





# urlpatterns = [
#     path('', placeholder, name='placeholder'),
# ]