from django.test import TestCase
from . import models

class StackTests(TestCase):

    def test_create_stack(self):
        stack = models.Stacks.objects.create(title="Mobile")
        title = stack.title
        self.assertEquals(title, "Mobile")
        print(123123)