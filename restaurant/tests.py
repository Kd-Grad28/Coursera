from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Menu, Booking
from .serializers import MenuSerializer


class ModelTests(TestCase):
    def test_menu_str(self):
        item = Menu.objects.create(title='IceCream', price=80, inventory=100)
        self.assertEqual(str(item), 'IceCream : 80')

    def test_booking_str(self):
        b = Booking.objects.create(name='Ann', no_of_guests=2, booking_date='2026-12-01T19:00:00Z')
        self.assertIn('Ann', str(b))


class HomePageTest(TestCase):
    def test_static_html_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Little Lemon')


class MenuApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        Menu.objects.create(title='Greek Salad', price=12.99, inventory=20)
        Menu.objects.create(title='Bruschetta', price=7.99, inventory=30)
        self.user = User.objects.create_user('chef', password='pass12345!')

    def test_list_menu_is_public(self):
        response = self.client.get('/api/menu/')
        self.assertEqual(response.status_code, 200)
        expected = MenuSerializer(Menu.objects.all(), many=True).data
        self.assertEqual(response.json(), expected)

    def test_get_single_menu_item(self):
        item = Menu.objects.first()
        response = self.client.get(f'/api/menu/{item.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Greek Salad')

    def test_create_menu_requires_login(self):
        data = {'title': 'Soup', 'price': '5.50', 'inventory': 10}
        self.assertEqual(self.client.post('/api/menu/', data, format='json').status_code, 401)
        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.post('/api/menu/', data, format='json').status_code, 201)
        self.assertEqual(Menu.objects.count(), 3)

    def test_update_and_delete_menu_item(self):
        self.client.force_authenticate(self.user)
        item = Menu.objects.first()
        r = self.client.put(f'/api/menu/{item.id}/', {'title': 'Greek Salad XL', 'price': '14.99', 'inventory': 15}, format='json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Menu.objects.get(id=item.id).title, 'Greek Salad XL')
        self.assertEqual(self.client.delete(f'/api/menu/{item.id}/').status_code, 204)


class BookingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('guest', password='pass12345!')
        self.payload = {'name': 'Jane', 'no_of_guests': 4, 'booking_date': '2026-12-01T19:00:00Z'}

    def test_bookings_require_authentication(self):
        self.assertEqual(self.client.get('/api/bookings/').status_code, 401)

    def test_booking_crud(self):
        self.client.force_authenticate(self.user)
        r = self.client.post('/api/bookings/', self.payload, format='json')
        self.assertEqual(r.status_code, 201)
        pk = r.json()['id']
        self.assertEqual(len(self.client.get('/api/bookings/').json()), 1)
        r = self.client.patch(f'/api/bookings/{pk}/', {'no_of_guests': 6}, format='json')
        self.assertEqual(r.json()['no_of_guests'], 6)
        self.assertEqual(self.client.delete(f'/api/bookings/{pk}/').status_code, 204)
        self.assertEqual(Booking.objects.count(), 0)


class AuthenticationTests(TestCase):
    def test_register_login_and_use_token(self):
        client = APIClient()
        # 1. registration
        r = client.post('/auth/users/', {'username': 'newuser', 'password': 'Str0ngPass!234'}, format='json')
        self.assertEqual(r.status_code, 201)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        # 2. token login
        r = client.post('/auth/token/login/', {'username': 'newuser', 'password': 'Str0ngPass!234'}, format='json')
        self.assertEqual(r.status_code, 200)
        token = r.json()['auth_token']
        self.assertTrue(Token.objects.filter(key=token).exists())
        # 3. token grants access to a protected endpoint
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(client.get('/api/bookings/').status_code, 200)
        self.assertEqual(client.get('/auth/users/me/').json()['username'], 'newuser')

    def test_wrong_password_rejected(self):
        User.objects.create_user('bob', password='right-pass-123')
        r = APIClient().post('/auth/token/login/', {'username': 'bob', 'password': 'wrong'}, format='json')
        self.assertEqual(r.status_code, 400)
