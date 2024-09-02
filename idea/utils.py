from django.db.models import Count

from .models import *


class DataMixin:
    paginate_by = 12

    def get_user_context(self, **kwargs):
        context = kwargs
        categories = Category.objects.all()

        context['categories'] = categories
        return context
