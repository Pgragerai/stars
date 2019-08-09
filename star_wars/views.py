from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView
from django.contrib.auth.mixins import AccessMixin
from rest_framework.authtoken.models import Token
from django.urls import reverse_lazy
from django.shortcuts import render

from star_wars.models import CastingManager, Contestan, Character
from star_wars.forms import ContestanAddForm

import datetime

class LoginWebContenido(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        castingManager = CastingManager.objects.get(usuario=request.user)
        token, _ = Token.objects.get_or_create(user=castingManager.usuario)
        request.session['token'] = token.key
        return super().dispatch(request, *args, **kwargs)


class Home(LoginWebContenido, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        return super(Home, self).get(request, *args, **kwargs)

class AddContestan(LoginWebContenido, CreateView):
    model = Contestan
    form_class = ContestanAddForm
    success_url = reverse_lazy('home')
    template_name = 'contestan_form.html'

    def post(self, request, *args, **kwargs):
        formulario = ContestanAddForm(request.POST)
        if formulario.is_valid():
            character = None
            try:
                character_request = request.POST['character'].split("#")
                character = Character.objects.get(pk=character_request[0])
                return super(AddContestan, self).get(request, *args, **kwargs)
            except Character.DoesNotExist:
                character = Character(id = character_request[0], name= character_request[1])
                actual = datetime.datetime.now().date()
                if ((actual - formulario.cleaned_data.get("date"))/365) >= datetime.timedelta(days=18):
                    contestan = Contestan (first_name=formulario.cleaned_data.get("first_name"),
                                           last_name=formulario.cleaned_data.get("last_name"),
                                           date=formulario.cleaned_data.get("date"),
                                           phone=formulario.cleaned_data.get("phone"),
                                           country=formulario.cleaned_data.get("country"),
                                           email=formulario.cleaned_data.get("email"))
                    character.save()
                    contestan.character=character
                    contestan.save()
                    return render(request, 'home.html')
                else:
                    super(AddContestan, self).get(request, *args, **kwargs)
        else:
            return super(AddContestan, self).get(request, *args, **kwargs)

class ListContestan(LoginWebContenido, ListView):
    model = Contestan
    paginate_by = 5 
    template_name = 'contestan_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ListCharacter(LoginWebContenido, ListView):
    model = Character
    paginate_by = 5
    template_name = 'character_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class DeleteContestan(LoginWebContenido,DeleteView):
    model = Contestan
    template_name = 'contestan_delete.html'

    def post(self, request, *args, **kwargs):
        contestan = Contestan.objects.get(pk=request.POST['contestan'])
        character = Character.objects.get(pk=contestan.character.pk)
        character.delete()
        contestan.delete()
        return render(request, 'home.html')

class UpdateContestan(LoginWebContenido, UpdateView):
    model = Contestan
    form_class = ContestanAddForm
    success_url = reverse_lazy('home')
    template_name = 'contestan_update.html'

    def post(self, request, *args, **kwargs):
        formulario = ContestanAddForm(request.POST)
        if formulario.is_valid():
            contestan = Contestan.objects.get(pk=request.POST['contestan'])
            contestan.first_name = formulario.cleaned_data.get("first_name")
            contestan.last_name = formulario.cleaned_data.get("last_name")
            contestan.date = formulario.cleaned_data.get("date")
            contestan.phone = formulario.cleaned_data.get("phone")
            contestan.country = formulario.cleaned_data.get("country")
            contestan.email = formulario.cleaned_data.get("email")
            contestan.save()
            return render(request, 'home.html')
        else:
            return super(UpdateContestan, self).get(request, *args, **kwargs)

class UpdateCharacter(LoginWebContenido, TemplateView):

    template_name = "character_update.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateCharacter, self).get_context_data(**kwargs)
        context['contestan'] = Contestan.objects.get(pk=self.kwargs['pk'])

        return context


    def get(self, request, *args, **kwargs):
        return super(UpdateCharacter, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            character_request = request.POST['character'].split("#")
            constentan = Contestan.objects.get(pk=request.POST.get('contestan'))
            constentan.character = None
            constentan.save()
            character_new = Character(id=character_request[0], name=character_request[1])
            character_new.save()
            constentan.character = character_new
            constentan.save()
            return super(UpdateCharacter, self).get(request, *args, **kwargs)
        except MultiValueDictKeyError:
            return super(UpdateCharacter, self).get(request, *args, **kwargs)



