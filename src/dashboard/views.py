from django.utils import translation
from django.views.generic import TemplateView

from utils.dashboard.utils import LoginRequiredMixin


class Index(TemplateView):
    redirect_field_name = 'redirect_to'
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        user_language = kwargs.get('lang')
        print(f'User language: {user_language}')
        translation.activate(user_language)
        request.session[translation.LANGUAGE_SESSION_KEY] = user_language
        return super(Index, self).get(request, *args, **kwargs)
