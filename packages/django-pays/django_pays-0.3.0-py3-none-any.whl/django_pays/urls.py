from django.urls import path
from django.db import transaction

from .views import confirm

app_name = "pays"

urlpatterns = [
    path("<slug>/", transaction.atomic(confirm), name="confirm"),
]
