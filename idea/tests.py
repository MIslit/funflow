from django.test import TestCase
from django.db.models import Q

from idea.models import Idea, User, Category

class SearchFormTest(TestCase):

    def setUp(self):
        User.objects.create(username='test_user', email='test@user.com', 
                            password='1513@as;djfESD')
        Category.objects.create(name='На улице', slug='outside')
        Idea.objects.create(title='Поиграй в футбол', 
                            description='Поиграй в футбол на улице',
                            author_id=1,
                            category_id=1)

    def test_serching_ideas(self):
        searched = 'Пои'
        ideas = Idea.objects.filter(Q(title__contains=searched) | Q(description__contains=searched))
        idea = Idea.objects.get(id=1)

        self.assertEqual(ideas[0], idea)
