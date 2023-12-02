from rest_framework.test import APITestCase

from authentication.models import User


class TestModel(APITestCase):
    
    def test_creates_user(self):
        # User class의 MyUserManager의 instance인 objects. objects를 통해 MyUserManager.create_user 접근
        user=User.objects.create_user('testuser1', 'testuser1@example.com', 'password123!@')  

        self.assertIsInstance(user, User)  # check if this user is an instance of the User class
        self.assertEqual(user.email, 'testuser1@example.com') # check if this user's email is equals to the email
        self.assertFalse(user.is_staff)  # this is not created as a super user. so check if this user is not staff.

    def test_creates_super_suer(self):
        user=User.objects.create_superuser('testsuperuser1', 'testsuperuser1@example.com', 'password123!@')
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'testsuperuser1@example.com')
        self.assertTrue(user.is_staff)

    def test_raises_error_when_username_is_not_supplied(self):
        self.assertRaises(ValueError, 
                          User.objects.create_user, 
                          username='', email='testnotusername@example.com', password='password123!@')

    def test_raises_error_message_when_username_is_not_supplied(self):
        with self.assertRaisesMessage(ValueError, 'The given username must be set'):
            User.objects.create_user(username='', email='testuser1@example.com', password='password123!@') 

    def test_raises_error_when_email_is_not_supplied(self):
        self.assertRaises(ValueError, 
                          User.objects.create_user, 
                          username='testnotemail', email='', password='password123!@')

    def test_raises_error_message_when_email_is_not_supplied(self):
        with self.assertRaisesMessage(ValueError, 'The given email must be set'):
            User.objects.create_user(username='testnotemail', email='', password='password123!@')  

    def creates_super_user_with_is_staff_status(self):
        with self.assertRaisesMessage('Superuser must have is_staff=True.'):
            User.objects.create_superuser(username='username', 
                                          email='username@example.com', 
                                          password='password123!@',
                                          is_staff=False)  
    
    def creates_super_user_with_super_user_status(self):
        with self.assertRaisesMessage('Superuser must have is_superuser=True.'):
            User.objects.create_superuser(username='username', 
                                          email='username@example.com', 
                                          password='password123!@',
                                          is_superuser=False)  