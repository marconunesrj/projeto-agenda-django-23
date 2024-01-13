from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from contact.forms import ContactForm
from contact.models import Contact
# from django.utils.translation import gettext_lazy as _
# from django.utils.translation import ugettext as _
from django.utils.translation import gettext as _


@login_required(login_url='contact:login')
def create(request):

    # print(request.method)
    # print(request.POST.get('first_name'))
    # print(request.POST.get('last_name'))

    form_action = reverse('contact:create')

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)

        context = {
            'form': form,
            'form_action': form_action,
        }

        if form.is_valid():
            # Lazy save -> apenas armazenando os dados
            contact = form.save(commit=False)
            # Alterando antes de salvar
            contact.owner = request.user
            # Salvando os dados
            contact.save()
            messages.success(request, _('Contact created successfully!'))
            # Após salvar, redirecionar para a view de update
            return redirect('contact:update', contact_id=contact.pk)

        return render(
            request,
            'contact/create.html',
            context
        )

    context = {
        'form': ContactForm(),
        'form_action': form_action,
    }

    return render(
        request,
        'contact/create.html',
        context
    )


@login_required(login_url='contact:login')
def update(request, contact_id):

    # Buscando o registro, caso não exista levantamos um erro de 404
    contact = get_object_or_404(
        Contact, pk=contact_id, show=True, owner=request.user
    )

    form_action = reverse('contact:update', args=(contact_id,))

    if request.method == 'POST':
        # passando o instance, significa que queremos atualizar o
        # registro existente
        form = ContactForm(request.POST, request.FILES, instance=contact)

        context = {
            'form': form,
            'form_action': form_action,
        }

        if form.is_valid():
            contact = form.save()
            # Após salvar, redirecionar para a view de update
            return redirect('contact:update', contact_id=contact.pk)

        return render(
            request,
            'contact/create.html',
            context
        )

    context = {
        'form': ContactForm(instance=contact),
        'form_action': form_action,
    }

    return render(
        request,
        'contact/create.html',
        context
    )


@login_required(login_url='contact:login')
def delete(request, contact_id):
    contact = get_object_or_404(
        Contact, pk=contact_id, show=True, owner=request.user
    )
    confirmation = request.POST.get('confirmation', 'no')

    if confirmation == 'yes':
        contact.delete()
        # Após excluir, redirecionar para a view index
        return redirect('contact:index')

    return render(
        request,
        'contact/contact.html',
        {
            'contact': contact,
            'confirmation': confirmation,
        }
    )
