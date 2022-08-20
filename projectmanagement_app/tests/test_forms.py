from django.test import TestCase
import datetime
from projectmanagement_app.forms import TaskForm
from projectmanagement_app.models import Project

class TaskFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Project.objects.create(name='Increase customer satisfaction')

    def test_task_form_due_date_field_label(self):
        form = TaskForm()
        self.assertEqual(form.fields['due_date'].label, 'Due date')

    def test_task_form_due_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=2)
        project_id = Project.objects.get(id=1)
        form = TaskForm(data={'project': project_id, 'name': 'Task number 1', 'due_date': date, 'status': 'CO', 'person_assigned': 'Jack', 
                              'additional_information': 'Some comments', 'priority': 'M'})
        self.assertFalse(form.is_valid())

    def test_task_form_due_date_in_future(self):
        date = datetime.date.today() + datetime.timedelta(days=2)
        project_id = Project.objects.get(id=1)
        form = TaskForm(data={'project': project_id, 'name': 'Task number 1', 'due_date': date, 'status': 'CO', 'person_assigned': 'Jack', 
                              'additional_information': 'Some comments', 'priority': 'M'})
        self.assertTrue(form.is_valid())

    def test_task_form_due_date_today(self):
        date = datetime.date.today()
        project_id = Project.objects.get(id=1)
        form = TaskForm(data={'project': project_id, 'name': 'Task number 1', 'due_date': date, 'status': 'CO', 'person_assigned': 'Jack', 
                              'additional_information': 'Some comments', 'priority': 'M'})
        self.assertTrue(form.is_valid())
