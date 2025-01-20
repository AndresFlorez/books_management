
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from books_management.adapters.controllers.book_list_create_views import BookListCreateView
from books_management.adapters.controllers.book_retrieve_update_destroy_view import BookRetrieveUpdateDestroyView
from books_management.adapters.controllers.average_price_view import AveragePriceView
from books_management.entities.book import Book


User = get_user_model()


class BookManagementTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        user = User.objects.create_user(
            username='test_user',
            email='test@test.com',
            password='test_password'
        )

        refresh = RefreshToken.for_user(user)
        self.access_token = str(refresh.access_token)
        self.list_create_url = reverse(BookListCreateView.name)
        self.retrieve_update_destroy_url = reverse(BookRetrieveUpdateDestroyView.name, kwargs={'book_id': '123'})
        self.average_price_url = reverse(AveragePriceView.name, kwargs={'year': 2025})
        self.payload = {
            'title': 'Test title',
            'author': 'Test author',
            'published_date': '2025-01-01T00:00:00',
            'genre': 'Test genre',
            'description': 'Test description',
            'price': 10.0,
        }
        self.invalid_payload = {
            'title': 'Test title',
            'author': 'Test author',
            'published_date': '2025-01-01T00:00:00',
            'genre': 'Test genre',
            'description': 'Test description',
        }

    def test_get_book(self):
        """
        Test get book endpoint, should return a book
        """
        response = self.client.get(path=self.list_create_url, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)

    @patch('books_management.infrastructure.repositories.book_repository.BookRepository.create')
    def test_create_book(self, mock_create):
        """
        Test create book endpoint, should return a book
        """

        
        mock_create.return_value = Book.model_validate(self.payload)

        response = self.client.post(path=self.list_create_url, data=self.payload, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['title'], self.payload['title'])
        self.assertEqual(response.data['author'], self.payload['author'])
        self.assertEqual(response.data['published_date'], self.payload['published_date'])
        self.assertEqual(response.data['genre'], self.payload['genre'])
        self.assertEqual(response.data['description'], self.payload['description'])
        self.assertEqual(response.data['price'], self.payload['price'])

    def test_create_book_invalid_payload(self):
        """
        Test create book endpoint with invalid payload, should return 400
        """
        response = self.client.post(path=self.list_create_url, data=self.invalid_payload, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.data)
        self.assertEqual(response.data['errors'][0]['type'], 'missing')
        self.assertEqual(response.data['errors'][0]['msg'], 'Field required')
        self.assertIn('price', response.data['errors'][0]['loc'])
    
    @patch('books_management.infrastructure.repositories.book_repository.BookRepository.update')
    def test_update_book(self, mock_update):
        """
        Test update book endpoint, should return a book
        """
        mock_update.return_value = Book.model_validate(self.payload)
        response = self.client.put(path=f'{self.retrieve_update_destroy_url}', data=self.payload, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['title'], self.payload['title'])
        self.assertEqual(response.data['author'], self.payload['author'])
        self.assertEqual(response.data['published_date'], self.payload['published_date'])
        self.assertEqual(response.data['genre'], self.payload['genre'])
        self.assertEqual(response.data['description'], self.payload['description'])
        self.assertEqual(response.data['price'], self.payload['price'])
    
    def test_update_book_invalid_object_id(self):
        """
        Test update book endpoint with invalid payload, should return 400
        """

        response = self.client.put(path=f'{self.retrieve_update_destroy_url}', data=self.payload, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid book ID')

    def test_update_book_invalid_payload(self):
        """
        Test update book endpoint with invalid payload, should return 400
        """
        response = self.client.put(path=f'{self.retrieve_update_destroy_url}', data=self.invalid_payload, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.data)
        self.assertEqual(response.data['errors'][0]['type'], 'missing')
        self.assertEqual(response.data['errors'][0]['msg'], 'Field required')
        self.assertIn('price', response.data['errors'][0]['loc'])

    @patch('books_management.infrastructure.repositories.book_repository.BookRepository.delete')
    def test_delete_book(self, mock_delete):
        """
        Test delete book endpoint, should return 204
        """
        mock_delete.return_value = True
        response = self.client.delete(path=f'{self.retrieve_update_destroy_url}', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 204)
