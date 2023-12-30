from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Todo


class TodosAPITestCase(APITestCase):

    def create_todo(self):
        sample_todo = {'title': 'hello', 'desc': 'test'}
        response = self.client.post(reverse('create-list-todo'), sample_todo)
        return response

    def authenticate(self):
        user = {'username': 'username',
                'email': 'user@example.com',
                'password': 'password'}

        # 1. register
        self.client.post(reverse('register'), user)

        # 2. login
        response = self.client.post(reverse('login'),
                                    {'email': user['email'], 'password': user['password']})

        # 3. set header: add header to client
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.data['token']}"
        )


class TestListCreateTodosAPIView(TodosAPITestCase):

    def test_should_not_create_todo_with_no_auth(self):
        response = self.create_todo()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_not_create_todo(self):
        # 제대로 Todo가 생성되었다면 이전의 전체 Todo 개수에서 +1이 되어야 함
        previous_todo_count = Todo.objects.all().count()

        self.authenticate()

        response = self.create_todo()

        self.assertEqual(Todo.objects.all().count(), previous_todo_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 제대로 생성되었다면, response에 담긴 Todo 객체의 값도 생성한 값과 일치해야 함
        self.assertEqual(response.data['title'], 'hello')
        self.assertEqual(response.data['desc'], 'test')

    def test_retreives_all_todos(self):
        self.authenticate()

        response = self.client.get(reverse('create-list-todo'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 반환된 값의 타입이 list인지
        self.assertIsInstance(response.data['results'], list)

        # if you want to check that all tests are passing whenever we create, we get the pagination links
        self.create_todo()

        response = self.client.get(reverse('create-list-todo'))

        self.assertIsInstance(response.data['count'], int)
        self.assertEqual(response.data['count'], 1)


class TestTodoDetailAPIView(TodosAPITestCase):

    def test_retreives_one_item(self):
        self.authenticate()
        new_todo = self.create_todo()

        response = self.client.get(
            reverse('detail-todo', kwargs={'id': new_todo.data['id']})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        todo = Todo.objects.get(id=new_todo.data['id'])
        self.assertEqual(todo.title, new_todo.data['title'])  # DB verify

    def test_update_one_item(self):
        self.authenticate()
        new_todo = self.create_todo()

        response = self.client.patch(
            reverse('detail-todo', kwargs={'id': new_todo.data['id']}), {
                'title': 'update title', 'is_complete': True,
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_todo = Todo.objects.get(id=response.data['id'])
        self.assertEqual(updated_todo.is_complete, True)  # False -> True로 바뀌었는지 검증
        self.assertEqual(updated_todo.title, 'update title')

    def test_delete_one_item(self):
        self.authenticate()
        new_todo = self.create_todo()

        prev_db_count = Todo.objects.all().count()
        self.assertGreater(prev_db_count, 0)
        self.assertEqual(prev_db_count, 1)

        response = self.client.delete(
            reverse('detail-todo', kwargs={'id': new_todo.data['id']})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.all().count(), 0)

