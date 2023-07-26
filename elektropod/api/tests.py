from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Book

#Test Create a new book (POST):
class CreateBookAPITestCase(APITestCase):
    def setUp(self):
        self.create_url = reverse('create-book')

    def test_create_book(self):
        data = {'title': 'Test Book', 'author': 'Test Author', 'publication_date': '2023-07-26', 'isbn': '1234567890123'}
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'Test Book')

#Test Read a specific book (GET):

class GetBookDetailsAPITestCase(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(title='Test Book', author='Test Author', publication_date='2023-07-26', isbn='1234567890123')
        self.get_book_details_url = reverse('get-book-details', args=[self.book.id])

    def test_get_book_details(self):
        response = self.client.get(self.get_book_details_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')
        self.assertEqual(response.data['author'], 'Test Author')

#Test Update a book (PUT):

class UpdateBookAPITestCase(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(title='Test Book', author='Test Author', publication_date='2023-07-26', isbn='1234567890123')
        self.update_book_url = reverse('update-book', args=[self.book.id])
        self.updated_book_data = {'title': 'Updated Book', 'author': 'Updated Author', 'publication_date': '2023-07-27', 'isbn': '1234567890123'}

    def test_update_book(self):
        response = self.client.put(self.update_book_url, self.updated_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')
        self.assertEqual(self.book.author, 'Updated Author')

#Test Delete a book (DELETE):

class DeleteBookAPITestCase(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(title='Test Book', author='Test Author', publication_date='2023-07-26', isbn='1234567890123')
        self.delete_book_url = reverse('delete-book', args=[self.book.id])

    def test_delete_book(self):
        response = self.client.delete(self.delete_book_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

#Test Invalid Book ID (GET and DELETE):

class InvalidBookIDAPITestCase(APITestCase):
    def setUp(self):
        self.invalid_book_id = 999
        self.invalid_get_book_details_url = reverse('get-book-details', args=[self.invalid_book_id])
        self.invalid_delete_book_url = reverse('delete-book', args=[self.invalid_book_id])

    def test_invalid_get_book_details(self):
        response = self.client.get(self.invalid_get_book_details_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_delete_book(self):
        response = self.client.delete(self.invalid_delete_book_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)                        



          
    
    
    
        

        

    

