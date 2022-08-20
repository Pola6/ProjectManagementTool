from django.test import TestCase
from django.urls import reverse
from projectmanagement_app.models import ProjectManager, Project, Task
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
import datetime


class ProjectListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_projects = 12

        for number in range(number_of_projects):
            Project.objects.create(
                name=f'Example project {number}',
            )

    def test_url_exists_at_correct_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectmanagement_app/index.html')

    def test_pagination_is_seven(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue('is_paginated' in response.context)
        self.assertEqual(len(response.context['project_list']), 7)

    def test_lists_projects_second_page(self):
        response = self.client.get(reverse('index')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue('is_paginated' in response.context)
        self.assertEqual(len(response.context['project_list']), 5)


class TaskListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Project.objects.create(name='Project number 1')
        number_of_tasks = 12

        for number in range(number_of_tasks):
            Task.objects.create(
                project_id=1,
                name=f'Example task {number}',
                due_date='2023-12-01',
            )

    def test_url_exists_at_correct_location(self):
        response = self.client.get('/project/1/tasks/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('task-list', kwargs={'project_id':1}))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('task-list', kwargs={'project_id':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectmanagement_app/task_list.html')

    def test_pagination_is_seven(self):
        response = self.client.get(reverse('task-list', kwargs={'project_id':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue('is_paginated' in response.context)
        self.assertEqual(len(response.context['task_list']), 7)

    def test_lists_tasks_second_page(self):
        response = self.client.get(reverse('task-list', kwargs={'project_id':1})+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue('is_paginated' in response.context)
        self.assertEqual(len(response.context['task_list']), 5)


class ProjectManagerListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_project_managers = 8

        for number in range(number_of_project_managers):
            ProjectManager.objects.create(
                name=f'Jack Brown {number}',
            )

    def test_url_exists_at_correct_location(self):
        response = self.client.get('/managers/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('projectmanager-list'))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('projectmanager-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectmanagement_app/projectmanager_list.html')

    def test_pagination_is_six(self):
        response = self.client.get(reverse('projectmanager-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue('is_paginated' in response.context)
        self.assertEqual(len(response.context['projectmanager_list']), 6)

    def test_lists_project_managers_second_page(self):
        response = self.client.get(reverse('projectmanager-list')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue('is_paginated' in response.context)
        self.assertEqual(len(response.context['projectmanager_list']), 2)


class ProjectDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Project.objects.create(name='Example project number 1')

    def test_url_exists_at_correct_location(self):
        response = self.client.get('/project/1/projectdetails/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('project-detail', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('project-detail', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectmanagement_app/project_detail.html')


class TaskDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Project.objects.create(name='Example project number 1')
        Task.objects.create(
            project_id=1, 
            name='Example task number 1', 
            due_date='2023-12-01',
        )

    def test_url_exists_at_correct_location(self):
        response = self.client.get('/project/1/tasks/1/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('task-detail', kwargs={'project_id':1, 'pk':1}))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('task-detail', kwargs={'project_id':1, 'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectmanagement_app/task_detail.html')


class ProjectCreateView(TestCase):
    @classmethod
    def setUpTestData(cls):
        ProjectManager.objects.create(name='Jack Brown')

    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='8rly&dR')
        test_user2 = User.objects.create_user(username='testuser2', password='BRlfr2!')

        test_user1.save()
        test_user2.save()

        permission = Permission.objects.get(name='Can add project')
        test_user2.user_permissions.add(permission)
        test_user2.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('project-create'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='8rly&dR')
        response = self.client.get(reverse('project-create'))
        # the response code is 200 instead of 403, as custom error 403 view was set up
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_can_add_project(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.get(reverse('project-create'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.get(reverse('project-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectmanagement_app/project_form.html')

    def test_redirects_to_index_on_success(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.post(reverse('project-create'), {'name':'Example project number 1', 
            'manager':1, 'department':'Finance', 'status':'CO'})
        self.assertRedirects(response, reverse('index'))


class AddTaskView(TestCase):
    @classmethod
    def setUpTestData(cls):
        Project.objects.create(name='Project number 1')

    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='8rly&dR')
        test_user2 = User.objects.create_user(username='testuser2', password='BRlfr2!')

        test_user1.save()
        test_user2.save()

        permission = Permission.objects.get(name='Can add task')
        test_user2.user_permissions.add(permission)
        test_user2.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('task-create', kwargs={'project_id':1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='8rly&dR')
        response = self.client.get(reverse('task-create', kwargs={'project_id':1}))
        # the response code is 200 instead of 403, as custom error 403 view was set up
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_can_add_task(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.get(reverse('task-create', kwargs={'project_id':1}))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.get(reverse('task-create', kwargs={'project_id':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_task.html')

    def test_redirects_to_task_list_on_success(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.post(reverse('task-create', kwargs={'project_id':1}), {'name':'Example task number 1', 
        'project':1, 'due_date': '2023-12-01', 'person_assigned': 'Emma', 'status':'CO', 'priority':'M'})
        self.assertRedirects(response, reverse('task-list', kwargs={'project_id':1}))

    def test_form_error_due_date_past(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        date_in_past = datetime.date.today() - datetime.timedelta(weeks=1)
        response = self.client.post(reverse('task-create', kwargs={'project_id': 1}), {'name':'Example task number 1',
            'project':1, 'due_date': date_in_past, 'person_assigned': 'Emma', 'status':'CO', 'priority':'M'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'due_date', 'Invalid date - due date in past')


class ProjectManagerCreateView(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='8rly&dR')
        test_user2 = User.objects.create_user(username='testuser2', password='BRlfr2!')

        test_user1.save()
        test_user2.save()

        permission = Permission.objects.get(name='Can add project manager')
        test_user2.user_permissions.add(permission)
        test_user2.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('projectmanager-create'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='8rly&dR')
        response = self.client.get(reverse('projectmanager-create'))
        # the response code is 200 instead of 403, as custom error 403 view was set up
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_can_add_projectmanager(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.get(reverse('projectmanager-create'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.get(reverse('projectmanager-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectmanagement_app/projectmanager_form.html')

    def test_redirects_to_projectmanager_list_on_success(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.post(reverse('projectmanager-create'), {'name':'Jack Brown', 
            'department':'Finance'})
        self.assertRedirects(response, reverse('projectmanager-list'))


class ProjectUpdateView(TestCase):
    @classmethod
    def setUpTestData(cls):
        Project.objects.create(name='Example project number 1')
        ProjectManager.objects.create(name='Jack Brown')

    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='8rly&dR')
        test_user2 = User.objects.create_user(username='testuser2', password='BRlfr2!')

        test_user1.save()
        test_user2.save()

        permission = Permission.objects.get(name='Can change project')
        test_user2.user_permissions.add(permission)
        test_user2.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('project-update', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='8rly&dR')
        response = self.client.get(reverse('project-update', kwargs={'pk':1}))
        # the response code is 200 instead of 403, as custom error 403 view was set up
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_can_change_project(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.get(reverse('project-update', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.get(reverse('project-update', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectmanagement_app/project_form.html')

    def test_redirects_to_index_on_success(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.post(reverse('project-update', kwargs={'pk':1}), {'name':'Example project number 1', 
            'manager':1, 'department':'Finance', 'status':'CO'})
        self.assertRedirects(response, reverse('project-detail', kwargs={'pk':1}))


class TaskUpdateView(TestCase):
    @classmethod
    def setUpTestData(cls):
        Project.objects.create(name='Project number 1')
        Task.objects.create(
                project_id=1,
                name='Task number 1',
                due_date='2023-12-01',
            )

    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='8rly&dR')
        test_user2 = User.objects.create_user(username='testuser2', password='BRlfr2!')

        test_user1.save()
        test_user2.save()

        permission = Permission.objects.get(name='Can change task')
        test_user2.user_permissions.add(permission)
        test_user2.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('task-update', kwargs={'project_id':1, 'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='8rly&dR')
        response = self.client.get(reverse('task-update', kwargs={'project_id':1, 'pk':1}))
        # the response code is 200 instead of 403, as custom error 403 view was set up
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_can_change_task(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.get(reverse('task-update', kwargs={'project_id':1, 'pk':1}))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.get(reverse('task-update', kwargs={'project_id':1, 'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectmanagement_app/task_form.html')

    def test_redirects_to_task_list_on_success(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.post(reverse('task-update', kwargs={'project_id':1, 'pk':1}), {'name':'Example task number 1', 
        'project':1, 'due_date': '2023-12-01', 'person_assigned': 'Emma', 'status':'CO', 'priority':'M'})
        self.assertRedirects(response, reverse('task-list', kwargs={'project_id':1}))


class ProjectManagerUpdateView(TestCase):
    @classmethod
    def setUpTestData(cls):
        ProjectManager.objects.create(name='Jack Brown')

    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='8rly&dR')
        test_user2 = User.objects.create_user(username='testuser2', password='BRlfr2!')

        test_user1.save()
        test_user2.save()

        permission = Permission.objects.get(name='Can change project manager')
        test_user2.user_permissions.add(permission)
        test_user2.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('projectmanager-update', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='8rly&dR')
        response = self.client.get(reverse('projectmanager-update', kwargs={'pk':1}))
        # the response code is 200 instead of 403, as custom error 403 view was set up
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_can_change_projectmanager(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.get(reverse('projectmanager-update', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.get(reverse('projectmanager-update', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectmanagement_app/projectmanager_form.html')

    def test_redirects_to_projectmanager_list_on_success(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.post(reverse('projectmanager-update', kwargs={'pk':1}), {'name':'Jack Brown', 
            'department':'Finance'})
        self.assertRedirects(response, reverse('projectmanager-list'))


class ProjectDeleteView(TestCase):
    @classmethod
    def setUpTestData(cls):
        Project.objects.create(name='Example project number 1')
        ProjectManager.objects.create(name='Jack Brown')

    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='8rly&dR')
        test_user2 = User.objects.create_user(username='testuser2', password='BRlfr2!')

        test_user1.save()
        test_user2.save()

        permission = Permission.objects.get(name='Can delete project')
        test_user2.user_permissions.add(permission)
        test_user2.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('project-delete', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='8rly&dR')
        response = self.client.get(reverse('project-delete', kwargs={'pk':1}))
        # the response code is 200 instead of 403, as custom error 403 view was set up
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_can_delete_project(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.get(reverse('project-delete', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.get(reverse('project-delete', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectmanagement_app/project_confirm_delete.html')

    def test_redirects_to_index_on_success(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.post(reverse('project-delete', kwargs={'pk':1}))
        self.assertRedirects(response, reverse('index'))


class TaskDeleteView(TestCase):
    @classmethod
    def setUpTestData(cls):
        Project.objects.create(name='Project number 1')
        Task.objects.create(
                project_id=1,
                name='Task number 1',
                due_date='2023-12-01',
            )

    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='8rly&dR')
        test_user2 = User.objects.create_user(username='testuser2', password='BRlfr2!')

        test_user1.save()
        test_user2.save()

        permission = Permission.objects.get(name='Can delete task')
        test_user2.user_permissions.add(permission)
        test_user2.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('task-delete', kwargs={'project_id':1, 'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='8rly&dR')
        response = self.client.get(reverse('task-delete', kwargs={'project_id':1, 'pk':1}))
        # the response code is 200 instead of 403, as custom error 403 view was set up
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_can_delete_task(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.get(reverse('task-delete', kwargs={'project_id':1, 'pk':1}))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.get(reverse('task-delete', kwargs={'project_id':1, 'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectmanagement_app/task_confirm_delete.html')

    def test_redirects_to_task_list_on_success(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.post(reverse('task-delete', kwargs={'project_id':1, 'pk':1}))
        self.assertRedirects(response, reverse('task-list', kwargs={'project_id':1}))


class ProjectManagerDeleteView(TestCase):
    @classmethod
    def setUpTestData(cls):
        ProjectManager.objects.create(name='Jack Brown')

    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='8rly&dR')
        test_user2 = User.objects.create_user(username='testuser2', password='BRlfr2!')

        test_user1.save()
        test_user2.save()

        permission = Permission.objects.get(name='Can delete project manager')
        test_user2.user_permissions.add(permission)
        test_user2.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('projectmanager-delete', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='8rly&dR')
        response = self.client.get(reverse('projectmanager-delete', kwargs={'pk':1}))
        # the response code is 200 instead of 403, as custom error 403 view was set up
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_can_delete_projectmanager(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.get(reverse('projectmanager-delete', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.get(reverse('projectmanager-delete', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectmanagement_app/projectmanager_confirm_delete.html')

    def test_redirects_to_projectmanager_list_on_success(self):
        login = self.client.login(username='testuser2', password='BRlfr2!')
        response = self.client.post(reverse('projectmanager-delete', kwargs={'pk':1}))
        self.assertRedirects(response, reverse('projectmanager-list'))


class StatisticsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        '''Sets up project and task objects so that the test does not throw a ZeroDivisionError'''
        Project.objects.create(name='Example project number 1')
        Task.objects.create(
            project_id=1, 
            name='Example task number 1', 
            due_date='2023-12-01',
            status="CO",
        )

    def test_url_exists_at_correct_location(self):
        response = self.client.get('/statistics/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statistics.html')


class ManagersProjectsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Project.objects.create(name='Example project number 1')
        ProjectManager.objects.create(name='Jack Brown')

    def test_url_exists_at_correct_location(self):
        response = self.client.get('/managers/1/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('managers-projects', kwargs={'manager_id':1}))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('managers-projects', kwargs={'manager_id':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'managers_projects.html')
