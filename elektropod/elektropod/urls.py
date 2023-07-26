"""
URL configuration for elektropod project.

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
from api import views

app_name = 'books' 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/books/', views.create_book, name='create-book'),
    #path('api/books/', views.get_all_books, name='get-book-details'),
    path('api/books/<int:book_id>/', views.get_book_details, name='get-book-details'),
    path('api/books/<int:book_id>/update/', views.update_book, name='update-book'),
    path('api/books/<int:book_id>/delete/', views.delete_book, name='delete-book'),
]
