from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL= reverse('user:create')
TOKEN_URL= reverse('user:token')
ME_URL = reverse('user:me')



def create_user(**params):
    return get_user_model().objects.create_user(**params)



class PublicUserApiTests(TestCase):
    """Test the users api public"""

    def setup(self):
        self.client=APIClient()


    def test_create_valid_user_success(self):
        """Test create user with valid payload successful"""

        payload={
                'email':'saeed@gmail.com',
                'password':'pass123',
                'name':'test name'
        }

        res=self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user= get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)



    def test_user_exists(self):
        """Test that creating user is already exists fail"""
        payload={
                'email':'saeed@gmail.com',
                'password':'pass123',
        }
        create_user(**payload)
        res=self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_too_short(self):
        """Test that the password must be more than 5 character"""
        payload={
                'email':'saeed@gmail.com',
                'password':'123',
        }

        res=self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist=get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exist)


    def test_create_token_for_user(self):
        """Test that creating token for user"""
        payload={
                'email':'saeed@gmail.com',
                'password':'pass123',
        }
        create_user(**payload)
        res=self.client.post(TOKEN_URL,payload)
        self.assertIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_create_token_invalid_credentials(self):
        """Test that token are not created if invalid credential given"""
        create_user(email='saeed@gmail.com',password='password')
        payload={
                'email':'saeed@gmail.com',
                'password':'pass123',
        }

        res=self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token are not created if user does not exust"""
        payload={
                'email':'saeed@gmail.com',
                'password':'pass123',
        }

        res=self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that temail and password are required"""

        res=self.client.post(TOKEN_URL,{'email':'one', 'password':''})
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthurized(self):
        """Test that authuntication is requered for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API that require authentication """

    def setUp(self):
        payload = {'email': 'saeed@gmail.com', 'password': 'pass123', 'name': 'name'}
        self.client = APIClient()
        self.user = create_user(email = 'saeed@gmail.com', password = 'pass123', name = 'name')

        self.client.force_authenticate(user = self.user)

    def test_retrieve_profile_success(self):
        """Test that user can get there profile"""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
                    'name': self.user.name,
                    'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """Test that post method not allowed in me"""

        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating profile for authenticated user"""
        payload = {'name': 'newName', 'password': 'newPass123'}
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
