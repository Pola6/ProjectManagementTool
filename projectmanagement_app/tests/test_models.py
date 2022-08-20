from django.test import TestCase
from projectmanagement_app.models import ProjectManager, Project, Task


class ProjectManagerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ProjectManager.objects.create(name='Michael Smith')

    def test_name_label(self):
        projectmanager = ProjectManager.objects.get(id=1)
        field_label = projectmanager._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_department_label(self):
        projectmanager = ProjectManager.objects.get(id=1)
        field_label = projectmanager._meta.get_field('department').verbose_name
        self.assertEqual(field_label, 'department')

    def test_name_max_length(self):
        projectmanager = ProjectManager.objects.get(id=1)
        max_length = projectmanager._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_name(self):
        projectmanager = ProjectManager.objects.get(id=1)
        expected_object_name = f'{projectmanager.name}'
        self.assertEqual(str(projectmanager), expected_object_name)


class ProjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Project.objects.create(name='Increase customer satisfaction')
    
    def test_name_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_description_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_department_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('department').verbose_name
        self.assertEqual(field_label, 'department')

    def test_manager_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('manager').verbose_name
        self.assertEqual(field_label, 'manager')

    def test_status_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'status')

    def test_name_max_length(self):
        project = Project.objects.get(id=1)
        max_length = project._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_department_max_length(self):
        project = Project.objects.get(id=1)
        max_length = project._meta.get_field('department').max_length
        self.assertEqual(max_length, 100)    
    
    def test_status_max_length(self):
        project = Project.objects.get(id=1)
        max_length = project._meta.get_field('status').max_length
        self.assertEqual(max_length, 2)  

    def test_object_name_is_name(self):
        project = Project.objects.get(id=1)
        expected_object_name = f'{project.name}'
        self.assertEqual(str(project), expected_object_name)
        

class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Project.objects.create(name='Increase customer satisfaction')
        Task.objects.create(name='Market research', project_id=1, due_date='2023-12-01')

    def test_project_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('project').verbose_name
        self.assertEqual(field_label, 'project')

    def test_name_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_due_date_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('due_date').verbose_name
        self.assertEqual(field_label, 'due date')

    def test_status_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'status')

    def test_person_assigned_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('person_assigned').verbose_name
        self.assertEqual(field_label, 'person assigned')
    
    def test_additional_information_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('additional_information').verbose_name
        self.assertEqual(field_label, 'additional information')

    def test_priority_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('priority').verbose_name
        self.assertEqual(field_label, 'priority')

    def test_name_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)  

    def test_status_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field('status').max_length
        self.assertEqual(max_length, 2)  

    def test_person_assigned_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field('person_assigned').max_length
        self.assertEqual(max_length, 100)  

    def test_priority_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field('priority').max_length
        self.assertEqual(max_length, 1)  

    def test_object_name_is_name(self):
        task = Task.objects.get(id=1)
        expected_object_name = f'{task.name}'
        self.assertEqual(str(task), expected_object_name)
        