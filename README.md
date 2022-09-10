# Project Management Tool

A CRUD web application to manage projects in a company, built with Django framework.

## Project details

![](https://github.com/Pola6/ProjectManagementTool/blob/master/screen_gif.gif)

The application can be used by employees and managers of a company to keep track of projects. The app shows a list of projects and tasks with their details and add/update/delete options.

The website has a user login feature and the content is displayed based on user permissions (unlogged users, employees, managers).

## Requirements

The project requires the following to run:
* Python 3
* pip

## Installation

Follow the steps below to get started with the development environment.

1. Clone the repository
```
$ git clone https://github.com/Pola6/project-management-tool
```
2. Navigate to the project directory
```
$ cd project-management-tool
```
3. Install dependencies
```
$ pip install -r requirements.txt
```
4. To view the app in the browser:
```
$ python manage.py runserver
```
## Tests

The project includes unit tests based on Django TestCase class.

To run tests:
```
$ python manage.py test
```

## Technologies

* Python 3.10
* Django 4
* HTML5
* Bootstrap 5
* SQLite3

## Usage

The home page lists all projects with their statuses and other details. Once a user clicks on a project, a list of tasks for the project is displayed. For each task a user can view and edit the due date, status, person assigned etc.

The managers section lists all managers. Once manager's name is clicked, a list of projects assigned to this manager can be seen.

The statistics section shows projects data statistics such as the number and progress of tasks.

The content is displayed based on user permissions. There are 3 types of permissions:<br>
unlogged users - can view all content but cannot edit it<br>
employees - can view all content and can edit task details<br>
managers - can view all contect and can edit task, manager and project details

To explore the content of the website you can use the below test user accounts:

login: employee_account<br>
password: Employee123

login: manager_account<br>
password: Manager123
