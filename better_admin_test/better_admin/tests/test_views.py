from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from better_admin_test_app.models import Company


class ListViewTest(TestCase):

    def setUp(self):
        # all this for logging into the system
        User.objects.create_superuser('user', 'user@test.com', 'pswd')
        self.c = Client()
        self.c.login(username='user', password='pswd')
        # lets create a company
        self.company = Company.objects.create(name='X', address = 'ABC', 
                                              url='http://www.x.com', 
                                              ip_address='192.1.1.1',
                                              volume=100, revenue=10)

    def test_create_view_get(self):
        # hit the url
        list_url = reverse('better_admin_test_app_company_list')
        response = self.c.get(list_url)
        # response should be 200
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'better_admin/list.html')
        self.assertEqual(len(response.context['object_list']), 1)


class DetailViewTest(TestCase):

    def setUp(self):
        # all this for logging into the system
        User.objects.create_superuser('user', 'user@test.com', 'pswd')
        self.c = Client()
        self.c.login(username='user', password='pswd')
        # lets create a company
        self.company = Company.objects.create(name='X', address = 'ABC', 
                                              url='http://www.x.com', 
                                              ip_address='192.1.1.1',
                                              volume=100, revenue=10)

    def test_detail_view_get(self):
        # hit the url
        detail_url = reverse('better_admin_test_app_company_detail',
                             args=(self.company.pk,))
        response = self.c.get(detail_url)
        # response should be 200, detail template, object.name 'X'
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'better_admin/detail.html')
        self.assertEqual(response.context['object'].name, 'X')


class CreateViewTest(TestCase):

    def setUp(self):
        # all this for logging into the system
        User.objects.create_superuser('user', 'user@test.com', 'pswd')
        self.c = Client()
        self.c.login(username='user', password='pswd')

    def test_create_view_get(self):
        # hit the url
        create_url = reverse('better_admin_test_app_company_create')
        response = self.c.get(create_url)
        # response should be 200
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'better_admin/create.html')

    def test_create_view_post(self):
        # hit the url
        create_url = reverse('better_admin_test_app_company_create')
        response = self.c.post(create_url, {'name': 'X',
                                            'address': 'ABC',
                                            'url': 'http://www.x.com',
                                            'ip_address': '192.1.1.1',
                                            'volume': 100,
                                            'revenue': 10},
                                            follow=True)
        # we should get a 200 and a company created
        self.assertEqual(response.status_code, 200)
        # check for redirect to list view
        list_url = reverse('better_admin_test_app_company_list')
        self.assertRedirects(response, list_url)


class PopupViewTest(TestCase):

    def setUp(self):
        # all this for logging into the system
        User.objects.create_superuser('user', 'user@test.com', 'pswd')
        self.c = Client()
        self.c.login(username='user', password='pswd')

    def test_popup_view_get(self):
        # hit the url
        popup_url = reverse('better_admin_test_app_company_popup')
        response = self.c.get(popup_url)
        # response should be 200
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'better_admin/popup.html')

    def test_popup_view_post(self):
        # hit the url
        popup_url = reverse('better_admin_test_app_company_popup')
        response = self.c.post(popup_url, {'name': 'X',
                                            'address': 'ABC',
                                            'url': 'http://www.x.com',
                                            'ip_address': '192.1.1.1',
                                            'volume': 100,
                                            'revenue': 10},
                                            follow=True)
        # we should get a 200 and a company created
        self.assertEqual(response.status_code, 200)


class UpdateViewTest(TestCase):

    def setUp(self):
        # all this for logging into the system
        User.objects.create_superuser('user', 'user@test.com', 'pswd')
        self.c = Client()
        self.c.login(username='user', password='pswd')
        # lets create a company
        self.company = Company.objects.create(name='X', address = 'ABC', 
                                              url='http://www.x.com', 
                                              ip_address='192.1.1.1',
                                              volume=100, revenue=10)

    def test_update_view_get(self):
        # hit the url
        update_url = reverse('better_admin_test_app_company_update',
                             args=(self.company.pk,))
        response = self.c.get(update_url)
        # response should be 200
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'better_admin/update.html')

    def test_update_view_post(self):
        # hit the url
        update_url = reverse('better_admin_test_app_company_update',
                             args=(self.company.pk,))
        response = self.c.post(update_url, {'name': 'Y',
                                            'address': 'ABC',
                                            'url': 'http://www.x.com',
                                            'ip_address': '192.1.1.1',
                                            'volume': 100,
                                            'revenue': 10},
                                            follow=True)
        # we should get a 200 and a company updated
        self.assertEqual(response.status_code, 200)
        # check for redirect to list view
        list_url = reverse('better_admin_test_app_company_list')
        self.assertRedirects(response, list_url)


class DeleteViewTest(TestCase):

    def setUp(self):
        # all this for logging into the system
        User.objects.create_superuser('user', 'user@test.com', 'pswd')
        self.c = Client()
        self.c.login(username='user', password='pswd')
        # lets create a company
        self.company = Company.objects.create(name='X', address = 'ABC', 
                                              url='http://www.x.com', 
                                              ip_address='192.1.1.1',
                                              volume=100, revenue=10)

    def test_delete_view_get(self):
        # hit the url
        delete_url = reverse('better_admin_test_app_company_delete',
                             args=(self.company.pk,))
        response = self.c.get(delete_url)
        # response should be 200
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'better_admin/delete.html')

    def test_delete_view_post(self):
        # hit the url
        delete_url = reverse('better_admin_test_app_company_delete',
                             args=(self.company.pk,))
        response = self.c.post(delete_url, follow=True)
        # we should get a 200 and a company created
        self.assertEqual(response.status_code, 200)
        # check for redirect to list view
        list_url = reverse('better_admin_test_app_company_list')
        self.assertRedirects(response, list_url)
