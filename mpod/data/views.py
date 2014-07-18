# Create your views here.
from django.template.loader import get_template
from django.template import Template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.db.models import Q
from django.shortcuts import render_to_response
from django.views.generic.list_detail import object_list
from models import *
from django.utils.html import escape
import datetime


from my_forms import *


import menus
import my_menus

def render_any(anyx):
    t=Template("{{anyxx}}")
    html = t.render(Context({
    "anyxx":anyx,
    },))
    return html   

def data_base(request, sub_template):
    t = get_template(sub_template)
    request_path=request.get_full_path()
    debug_info=request_path
    my_top_menu=menus.menu(my_menus.data_top_menu, request_path, 0)
    my_nav_menu=menus.menu(my_menus.mpod_nav_menu, request_path, 0)
    html = t.render(Context(
    {"top_menu":my_top_menu,
    "nav_menu":my_nav_menu}
    ))
    return html

def dict_base(request, sub_template):
    t = get_template(sub_template)
    request_path=request.get_full_path()
    debug_info=request_path
    my_top_menu=menus.menu(my_menus.dict_top_menu, request_path, 0)
    my_nav_menu=menus.menu(my_menus.mpod_nav_menu, request_path, 0)
    html = t.render(Context(
    {"top_menu":my_top_menu,
    "nav_menu":my_nav_menu}
    ))
    return html

def data_properties(request):
    ogge = Property.objects.all()
    t = get_template('data/properties_list_view.html')
    request_path=request.get_full_path()
    my_top_menu=menus.menu(my_menus.data_top_menu, request_path, 0)
    my_nav_menu=menus.menu(my_menus.mpod_nav_menu, request_path, 0)
    properties_list_table_html = view_linked_properties_list(oggetti=ogge, header=None)
    html = t.render(Context(
    {"top_menu":my_top_menu,
    "nav_menu":my_nav_menu,
    "properties_list_table" : properties_list_table_html,
    }
    ))
    return HttpResponse(html)

def data_intro(request):
    aa=data_base(request,'data/mpod_data_intro.html')
    return HttpResponse(aa)

def data_doc(request):
    aa=data_base(request,'data/mpod_data_doc.html')
    return HttpResponse(aa)

def data_references(request):
    aa=data_base(request,'data/mpod_data_references.html')
    return HttpResponse(aa)

def dict_intro(request):
    aa=dict_base(request,'data/mpod_dict_intro.html')
    return HttpResponse(aa)

def dict_doc(request):
    aa=dict_base(request,'data/mpod_dict_doc.html')
    return HttpResponse(aa)

def view_article(request, article_id):
    ogge = None
    html_res = None
    html_res2 = None
    datafiles = None
    try:
        ogge = PublArticle.objects.get(id__exact = article_id)
        datafiles = DataFile.objects.filter(publication__id__exact = article_id)
    except:
        pass
    if ogge:
        html_res = view_obj_as_2cols_table ( PublArticle, ogge, cap="Publication details")
        html_res2 = view_as_linked_table(DataFile, oggetti=datafiles, header='Associated datafiles')        
    t = get_template('data/publi_view.html')
    request_path=request.get_full_path()
    debug_info=request_path
    my_top_menu=menus.menu(my_menus.data_top_menu, request_path, 0)
    my_nav_menu=menus.menu(my_menus.mpod_nav_menu, request_path, 0)
    html = t.render(Context(
        {"top_menu":my_top_menu,
        "nav_menu":my_nav_menu,
        "publi_table": html_res,
        "associated_datafiles": html_res2,
        }
        ))
    response=HttpResponse(html)
##    response.write(debug_info)
    return HttpResponse(response)

def view_property(request, property_id):
    ogge = None
    html_res = None
    html_res2 = None
    try:
        ogge = Property.objects.get(id__exact = property_id)
    except:
        pass
    if ogge:
        datafiles = DataFile.objects.filter(properties__id__exact = property_id)
        html_res = view_obj_as_2cols_table (Property, ogge, cap="Property details")
        html_res2 = view_as_linked_table(DataFile, oggetti=datafiles, header='Associated datafiles')
    t = get_template('data/property_view.html')
    request_path=request.get_full_path()
    debug_info=request_path
    my_top_menu=menus.menu(my_menus.data_top_menu, request_path, 0)
    my_nav_menu=menus.menu(my_menus.mpod_nav_menu, request_path, 0)
    html = t.render(Context(
        {"top_menu":my_top_menu,
        "nav_menu":my_nav_menu,
        "property_table": html_res,
        "associated_datafiles": html_res2,
        }
        ))
    response=HttpResponse(html)
##    response.write(debug_info)
    return HttpResponse(response)

def view_exparcond(request, exparcond_id):
    t = get_template('data/experimentalparcond_view.html')
    request_path=request.get_full_path()
    debug_info=request_path
    my_top_menu=menus.menu(my_menus.data_top_menu, request_path, 0)
    my_nav_menu=menus.menu(my_menus.mpod_nav_menu, request_path, 0)
    ogge = ExperimentalParCond.objects.filter(id__exact = exparcond_id).distinct()
    html_res = None
    if ogge:
        ogge = ogge[0]
        html_res = view_obj_as_2cols_table (ExperimentalParCond, ogge, cap="Experimental Parameter/Condition details")
    html = t.render(Context(
        {"top_menu":my_top_menu,
        "nav_menu":my_nav_menu,
        "property_table": html_res,
        }
        ))
    response=HttpResponse(html)
##    response.write(debug_info)
    return HttpResponse(response)

def view_data_item(request, dataitem_id):
#    ogge = DataFile.objects.get(code__exact = dataitem_id)
    t = get_template('data/datafile_view.html')
    request_path=request.get_full_path()
    debug_info=request_path
    my_top_menu=menus.menu(my_menus.data_top_menu, request_path, 0)
    my_nav_menu=menus.menu(my_menus.mpod_nav_menu, request_path, 0)
##    html_dataitem, html_gen_props, html_tables = data_item_html(dataitem_id)
    html_dataitem, html_tables = data_item_html(dataitem_id)
    html = t.render(Context(
        {"top_menu":my_top_menu,
        "nav_menu":my_nav_menu,
        "html_dataitem":html_dataitem,
##        "html_gen_props":html_gen_props,
        "html_tables":html_tables,
        }
        ))
    response=HttpResponse(html)
##    response.write(debug_info)
    return HttpResponse(response)

def get_datafiles(phase_name_q='', formula_q='', cod_code_q='', publ_author_q=''):
    name_set = None
    formula_set = None
    cod_code_set = None
    tot_set = None
    res = None
    res_obj = None
    if phase_name_q:
        name_set = (Q(phase_name__icontains=phase_name_q) | Q(phase_generic__icontains=phase_name_q))
        res_obj = DataFile.objects.filter(name_set)

    if formula_q:
        formula_set = Q(chemical_formula__icontains=formula_q)
        if res_obj:
            res_obj = res_obj.filter(formula_set)
        else:
            res_obj = DataFile.objects.filter(formula_set)
    
    if publ_author_q:
        author_set = Q(publication__authors__icontains=publ_author_q)
        if res_obj:
            res_obj = res_obj.filter(author_set)
        else:
            res_obj = DataFile.objects.filter(author_set)

    if cod_code_q:
        try:
            cod_code_set = Q(cod_code__exact = int(cod_code_q))
            res_obj = DataFile.objects.filter(cod_code_set)
        except:
            pass
        
    if res_obj:
        html_res = view_as_linked_table(DataFile, oggetti=res_obj, header='Found datafiles')
    else:
        html_res=''
    return html_res

def data_search(request):
    t = get_template('data/mpod_data_search.html')
    request_path=request.get_full_path()
    debug_info=request_path
    my_top_menu=menus.menu(my_menus.data_top_menu, request_path, 0)
    my_nav_menu=menus.menu(my_menus.mpod_nav_menu, request_path, 0)
    html = t.render(Context(
    {"top_menu":my_top_menu,
    "nav_menu":my_nav_menu}
    ))
    query_phase_name = request.GET.get('phase_name', '')
    query_formula = request.GET.get('formula', '')
    query_cod_code = request.GET.get('cod_code', '')
    query_publ_author = request.GET.get('publ_author', '')
    if ( query_phase_name or query_formula or query_cod_code or query_publ_author):
        html_results = get_datafiles(query_phase_name, query_formula, query_cod_code, query_publ_author)
    else:
        html_results=None
    html = t.render(Context(
        {"top_menu":my_top_menu,
        "nav_menu":my_nav_menu,
        "query_phase_name": query_phase_name,
        "query_formula": query_formula,
        "query_cod_code": query_cod_code,
        "query_publ_author": query_publ_author,
        "results": html_results,
        }
        ))
    response=HttpResponse(html)
##    response.write(debug_info)
    return HttpResponse(response)

def get_publis(title_q='', author_q='', journal_q=''):
    title_set = None
    journal_set = None
    author_set = None
    tot_set = None
    res = None
    res_obj = None
    if title_q:
        title_set = Q(title__icontains=title_q)
        res_obj = PublArticle.objects.filter(title_set)
    if author_q:
        author_set = Q(authors__icontains=author_q)
        if res_obj:
            res_obj = res_obj.filter(author_set)
        else:
            res_obj = PublArticle.objects.filter(author_set)
    if journal_q:
        journal_set = Q(journal__icontains=journal_q)
        if res_obj:
            res_obj = res_obj.filter(journal_set)
        else:
            res_obj = PublArticle.objects.filter(journal_set)
    if res_obj:
        html_res = view_linked_articles_list(oggetti=res_obj, header='Found articles')
    else:
        html_res=''
    return html_res

def publi_search(request):
    t = get_template('data/mpod_publi_search.html')
    request_path=request.get_full_path()
    debug_info=request_path
    my_top_menu=menus.menu(my_menus.data_top_menu, request_path, 0)
    my_nav_menu=menus.menu(my_menus.mpod_nav_menu, request_path, 0)
    html = t.render(Context(
    {"top_menu":my_top_menu,
    "nav_menu":my_nav_menu}
    ))
    query_title = request.GET.get('title', '')
    query_author = request.GET.get('author', '')
    query_journal = request.GET.get('journal', '')
    if ( query_title or query_author or query_journal):
        html_results = get_publis(query_title, query_author, query_journal)
    else:
        html_results=None
    html = t.render(Context(
        {"top_menu":my_top_menu,
        "nav_menu":my_nav_menu,
        "query_title": query_title,
        "query_author": query_author,
        "query_journal": query_journal,
        "results": html_results,
        }
        ))
    response=HttpResponse(html)
##    response.write(debug_info)
    return HttpResponse(response)



def submit_file(request):
    time_st = "_"
    request_path=request.get_full_path()
    my_top_menu=menus.menu(my_menus.data_top_menu, request_path, 0)
    my_nav_menu=menus.menu(my_menus.mpod_nav_menu, request_path, 0)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        val = form.is_valid()
        if val:
            time_st = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
            f1 = request.FILES['mpod_file']
            f2 = request.FILES['pdf_file']
            email_add = form.cleaned_data['email']
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']
            opt_mail_data = [name, message]
            handle_uploaded_files(f1, f2, time_st)
            #send_upload_notif(f1, f2, time_st, email_add, opt_email_data)
            return HttpResponseRedirect('/datafiles/upload/success/')
        else:
            pass
    else:
        form = UploadFileForm()
    return render_to_response('data/mpod_file_submit.html', 
            {'form': form, 
            'time_stamp': time_st,
            "top_menu":my_top_menu,
            "nav_menu":my_nav_menu,
             })

def upload_success(request):
    aa=data_base(request,'data/upload_success.html')
    return HttpResponse(aa)

##Mi intento
def tabla(request, dataitem_id):
#    ogge = DataFile.objects.get(code__exact = dataitem_id)
    t = get_template('data/datafile_view.html')
    request_path=request.get_full_path()
    debug_info=request_path
    my_top_menu=menus.menu(my_menus.data_top_menu, request_path, 0)
    my_nav_menu=menus.menu(my_menus.mpod_nav_menu, request_path, 0)
##    html_dataitem, html_gen_props, html_tables = data_item_html(dataitem_id)
    html_dataitem, html_tables = data_item_html(dataitem_id)
    html = t.render(Context(
        {"top_menu":my_top_menu,
        "nav_menu":my_nav_menu,
        "html_dataitem":html_dataitem,
##        "html_gen_props":html_gen_props,
        "html_tables":html_tables,
        }
        ))
    response=HttpResponse(html)
##    response.write(debug_info)
    return HttpResponse(response)