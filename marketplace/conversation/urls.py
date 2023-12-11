from django.urls import path, include
from . import views
# from core.views import contact

app_name = 'conversation'

urlpatterns = [
    path('new/<int:item_pk>/', views.new_conversation, name="new"),
    path('inbox/',views.inbox, name="inbox"),
    path('<int:pk>/', views.detail, name="detail"),

]