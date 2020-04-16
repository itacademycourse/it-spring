from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from . import models
from . import forms

# Create your views here.


def all_materials(request):
    # material_list = models.Material.objects.all()
    material_list = models.Material.theory.all()
    return render(request,
                  'materials/all_materials.html',
                  {"materials": material_list})


def material_details(request, year, month, day, slug):
    material = get_object_or_404(models.Material,
                                 slug=slug,
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day)
    return render(request,
                  'materials/detail.html',
                  {'material': material})


def share_material(request, material_id):
    material = get_object_or_404(models.Material,
                                 id=material_id)
    sent = False
    if request.method == 'POST':
        form = forms.EmailMaterialForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            material_uri = request.build_absolute_uri(
                material.get_absolute_url(),
            )
            subject = "{} ({}) recommends you {}".format(
                cd['name'],
                cd['my_email'],
                material.title,
            )
            body = "{title} at {uri}\n\n {name} recommends you with comment:\n\n{comment}".format(
                title=material.title,
                uri=material_uri,
                name=cd['name'],
                comment=cd['comment'],
            )
            send_mail(subject, body, 'admin@mysite.com', [cd['to_email'], ])
            sent = True
    else:
        form = forms.EmailMaterialForm()
    return render(request,
                  'materials/share.html',
                  {'material': material, 'form': form, 'sent':sent})
