from django.urls import path
from .views import PetInfoParamView, PetView

urlpatterns = [
    path("pets/", PetView.as_view()),
    path("pets/<int:pet_id>/", PetInfoParamView.as_view()),
]
