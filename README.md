# Elektropod_Task
# views.py
1.Create a new book (POST):   
This API endpoint will allow users to create a new book entry by sending a POST request with the book details.

    from rest_framework import status        
    from rest_framework.decorators import api_view       
    from rest_framework.response import Response      
    from .models import Book     
    from .serializers import BookSerializer     

    @api_view(['POST']) 

    def create_book(request):    
        if request.method == 'POST':    
            serializer = BookSerializer(data=request.data)    
            if serializer.is_valid():   
               serializer.save()    
               return Response(serializer.data, status=status.HTTP_201_CREATED)    
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     

2.Read all books (GET):     
This API endpoint will retrieve a list of all books from the database.

    @api_view(['GET'])     
    def get_all_books(request):     
        if request.method == 'GET':    
            books = Book.objects.all()      
            serializer = BookSerializer(books, many=True)      
            return Response(serializer.data)    

3.Read a specific book (GET):      
This API endpoint will retrieve details of a specific book using its ID.     

    @api_view(['GET'])        
    def get_book_details(request, book_id):        
        try:      
            book = Book.objects.get(pk=book_id)     
        except Book.DoesNotExist:     
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)      
        if request.method == 'GET':      
            serializer = BookSerializer(book)        
            return Response(serializer.data)     

4.Update a book (PUT):       
This API endpoint will allow users to update the details of an existing book using its ID.     

    @api_view(['PUT'])     
    def update_book(request, book_id):     
       try:      
           book = Book.objects.get(pk=book_id)    
       except Book.DoesNotExist:     
           return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)      
       if request.method == 'PUT':      
           serializer = BookSerializer(book, data=request.data)               
           if serializer.is_valid():                
               serializer.save()                 
               return Response(serializer.data)                    
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                   

5.Delete a book (DELETE):                     
This API endpoint will allow users to delete a specific book using its ID.                 
        
    @api_view(['DELETE'])             
    def delete_book(request, book_id):                 
       try:                       
           book = Book.objects.get(pk=book_id)                     
       except Book.DoesNotExist:                         
           return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)                 
       if request.method == 'DELETE':                
           book.delete()                       
           return Response({'message': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)                            

<b><b>Book Model and Serializer:<b><b>     
Ensure you have the Book model and its corresponding serializer in place.      

# models.py   

    from django.db import models                        
    class Book(models.Model):                       
        title = models.CharField(max_length=100)                          
        author = models.CharField(max_length=100)                     
        publication_date = models.DateField()                   
        isbn = models.CharField(max_length=13)                              
        def __str__(self):     
            return self.title      

# serializers.py   



    from rest_framework import serializers       
    from .models import Book  

    class BookSerializer(serializers.ModelSerializer):      
        class Meta:      
            model = Book      
            fields = '__all__'      

# test.py   
<b>Test Cases : <b>

1.Test Create a new book (POST):      

    from rest_framework.test import APITestCase       
    from rest_framework import status       
    from django.urls import reverse       
    from .models import Book      

    class CreateBookAPITestCase(APITestCase): 

        def setUp(self):      
            self.create_url = reverse('create-book')                    
        def test_create_book(self):       
            data = {'title': 'Test Book', 'author': 'Test Author', 'publication_date': '2023-07-26', 'isbn': '1234567890123'}    
            response = self.client.post(self.create_url, data, format='json')     
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)       
            self.assertEqual(Book.objects.count(), 1)      
            self.assertEqual(Book.objects.get().title, 'Test Book')      

2.Test Read a specific book (GET):      

    class GetBookDetailsAPITestCase(APITestCase):    
        def setUp(self):       
            self.book = Book.objects.create(title='Test Book', author='Test Author', publication_date='2023-07-26', isbn='1234567890123')     
            self.get_book_details_url = reverse('get-book-details', args=[self.book.id])      
        def test_get_book_details(self):       
            response = self.client.get(self.get_book_details_url)     
            self.assertEqual(response.status_code, status.HTTP_200_OK)       
            self.assertEqual(response.data['title'], 'Test Book')      
            self.assertEqual(response.data['author'], 'Test Author')      

3.Test Update a book (PUT):           

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


4.Test Delete a book (DELETE):      



    class DeleteBookAPITestCase(APITestCase):   
        def setUp(self):      
            self.book = Book.objects.create(title='Test Book', author='Test Author', publication_date='2023-07-26', isbn='1234567890123')      
            self.delete_book_url = reverse('delete-book', args=[self.book.id]) 
        
        def test_delete_book(self):         
            response = self.client.delete(self.delete_book_url)      
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)      
            self.assertEqual(Book.objects.count(), 0)       

5.Test Invalid Book ID (GET):      

    class InvalidBookIDAPITestCase(APITestCase):   
        def setUp(self):       
            self.invalid_book_id = 999      
            self.invalid_get_book_details_url = reverse('get-book-details', args=[self.invalid_book_id])     
            self.invalid_delete_book_url = reverse('delete-book', args=[self.invalid_book_id])    
        def test_invalid_get_book_details(self):     
            response = self.client.get(self.invalid_get_book_details_url)    
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 
        
6.Test Invalid Book ID (DELETE): 
        
    def test_invalid_delete_book(self):      
        response = self.client.delete(self.invalid_delete_book_url)     
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)      


        


        
        
        
        
        
        
