from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AuthenticationTests(TestCase):
	def test_home_redirects_anonymous_users_to_login(self):
		response = self.client.get(reverse('index'))

		self.assertRedirects(response, f'{reverse("login")}?next={reverse("index")}')

	def test_registration_creates_user_and_logs_them_in(self):
		response = self.client.post(reverse('register'), {
			'username': 'ada',
			'email': 'ada@example.com',
			'password1': 'A-strong-password-123',
			'password2': 'A-strong-password-123',
		})

		self.assertRedirects(response, reverse('index'))
		self.assertTrue(response.wsgi_request.user.is_authenticated)
		self.assertEqual(User.objects.get(username='ada').email, 'ada@example.com')

	def test_invalid_registration_is_rendered_again(self):
		response = self.client.post(reverse('register'), {
			'username': 'ada',
			'email': 'not-an-email',
			'password1': 'password',
			'password2': 'different-password',
		})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Enter a valid email address.')
		self.assertEqual(User.objects.count(), 0)

	def test_login_authenticates_user(self):
		User.objects.create_user(username='ada', password='A-strong-password-123')

		response = self.client.post(reverse('login'), {
			'username': 'ada',
			'password': 'A-strong-password-123',
		})

		self.assertRedirects(response, reverse('index'))
		self.assertTrue(response.wsgi_request.user.is_authenticated)

	def test_invalid_login_is_rendered_again(self):
		User.objects.create_user(username='ada', password='A-strong-password-123')

		response = self.client.post(reverse('login'), {
			'username': 'ada',
			'password': 'wrong-password',
		})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Please enter a correct username and password.')

	def test_external_next_url_is_ignored(self):
		User.objects.create_user(username='ada', password='A-strong-password-123')

		response = self.client.post(
			f'{reverse("login")}?next=https://example.com',
			{
				'username': 'ada',
				'password': 'A-strong-password-123',
				'next': 'https://example.com',
			},
		)

		self.assertRedirects(response, reverse('index'))

	def test_logout_redirects_to_login(self):
		user = User.objects.create_user(username='ada', password='A-strong-password-123')
		self.client.force_login(user)

		response = self.client.post(reverse('logout'))

		self.assertRedirects(response, reverse('login'))
