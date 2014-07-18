# Create your views here.
from django.template.loader import get_template
from django.template import Template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils.html import escape
from django.core.mail import send_mail, EmailMessage
from data.my_forms import ContactForm

import menus
import my_menus

import os
import string

images_path=os.path.join(os.path.dirname(__file__),'media/images').replace('\\','/')
css_path=os.path.join(os.path.dirname(__file__),'templates/css').replace('\\','/')
datafiles_path=os.path.join(os.path.dirname(__file__),'media/datafiles').replace('\\','/')
dictionary_path=os.path.join(os.path.dirname(__file__),'media/dictionary').replace('\\','/')

def mpod_base(request, sub_template):
    t = get_template(sub_template)
    request_path=request.get_full_path()
    debug_info=request_path
    my_nav_menu=menus.menu(my_menus.mpod_nav_menu, request_path, 0)
    my_top_menu=menus.menu(my_menus.mpod_top_menu, request_path, 0)
    print my_nav_menu
    print my_top_menu
    html = t.render(Context(
    {"top_menu":my_top_menu,
    "nav_menu":my_nav_menu}
    ))
    return html


def index(request):
    aa=mpod_base(request,'mpod_intro.html')
    return HttpResponse(aa)

def properties(request):
    aa=mpod_base(request,'mpod_properties.html')
    return HttpResponse(aa)

def references(request):
    aa=mpod_base(request,'mpod_references.html')
    return HttpResponse(aa)

def credits(request):
    aa=mpod_base(request,'mpod_credits_logos.html')
    return HttpResponse(aa)

def disclaimer(request):
    aa=mpod_base(request,'mpod_disclaimer.html')
    return HttpResponse(aa)

def get_image(request, file_name):
    ext=file_name.split(".")[1]
    image_path=os.path.join(images_path,file_name)
    print image_path
    image_data = open(image_path, "rb").read()
    return HttpResponse(image_data, mimetype="image/"+ext)

def get_datafile(request, file_name):
    ext=file_name.split(".")[1]
    datafile_path=os.path.join(datafiles_path,file_name)
    datafile_data = open(datafile_path, "rb").read()
    return HttpResponse(datafile_data, mimetype="text")

def get_dictionary(request):
    datafile_path=os.path.join(dictionary_path,"cif_material_properties_0_0_6.dic")
    datafile_data = open(datafile_path, "rb").read()
    return HttpResponse(datafile_data, mimetype="text")

def load_css(request, file_name):
    css_file_path=os.path.join(css_path,file_name)
    css_file = open(css_file_path, "rb").read()
    return HttpResponse(css_file, mimetype="text/css")

def contact(request):
    request_path=request.get_full_path()
    my_top_menu=menus.menu(my_menus.mpod_top_menu, request_path, 0)
    my_nav_menu=menus.menu(my_menus.mpod_nav_menu, request_path, 0)
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['email']
            name = form.cleaned_data['name']
            cc_myself = form.cleaned_data['cc_myself']
            recipients = ['contact@materialproperties.org']
            if cc_myself:
                recipients.append(sender)
            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('/contact/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form
    return render_to_response('mpod_contact.html', {
        'form': form,
        "top_menu":my_top_menu,
        "nav_menu":my_nav_menu,
    })

def contact_success(request):
    aa=mpod_base(request,'contact_success.html')
    return HttpResponse(aa)
