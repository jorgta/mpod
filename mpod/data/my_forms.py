from models import *
from django.db import models
from django.utils.html import escape
from django.template.defaultfilters import capfirst
from django.forms.models import model_to_dict
from django.template.loader import get_template
from django.template import Template
from django.template import Context
from captcha.fields import CaptchaField
from django.core.mail import send_mail, EmailMessage


from parse_files_2 import *

datafiles_path = os.path.join(os.path.dirname(__file__),'../media/datafiles').replace('\\','/')
uploads_path = os.path.join(datafiles_path, "uploaded")

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size':'40'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':'8', 'style': 'vertical-align:text-top;'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'size':'40'}))
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size':'40'}))
    cc_myself = forms.BooleanField(required=False)
    captcha = CaptchaField()


class UploadFileForm(forms.Form):
    mpod_file  = forms.FileField()
    pdf_file = forms.FileField()
    email = forms.EmailField(widget=forms.TextInput(attrs={'size':'40'}))
    name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'size':'40'}))
    message = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':'8', 'style': 'vertical-align:text-top;'}))
    captcha = CaptchaField()

def handle_uploaded_files(f1, f2, time_st):
    new_dir = os.path.join(uploads_path, time_st)
    os.mkdir(new_dir)
    d1 = open(os.path.join(new_dir, f1.name), 'wb+')
    d2 = open(os.path.join(new_dir, f2.name), 'wb+')
    for chunk1 in f1.chunks():
        d1.write(chunk1)
    for chunk2 in f2.chunks():
        d2.write(chunk2)
    d1.close()
    d2.close()

def handle_pdf_file(f):
    print uploads_path
    print f.name
    destination = open(os.path.join(uploads_path, f.name), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def handle_mpod_file(f):
    print uploads_path
    print f.name
    destination = open(os.path.join(uploads_path, f.name), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    
def send_upload_notif(f1, f2, time_st, e_mail_add, opt_mail_data):
    [name, message] = opt_mail_data
    new_dir = os.path.join(uploads_path, time_st)
    d1 = os.path.join(new_dir, f1.name)
    d2 = os.path.join(new_dir, f2.name)
    subject = "[MPOD]: new submission from "+ name
    messag = "[MPOD]: new submission \n from: %s \n email: %s \n  "%(name,e_mail_add) + message
    from_add = "submit@materialproperties.org"
    to_adds = ["submit@materialproperties.org"]
    mail = EmailMessage(subject, messag, from_add, to_adds)
    mail.attach_file(d1)
    mail.attach_file(d2)
    mail.send()

    

def get_labels(model, cap=True, esc=True):
    opts = model._meta
    field_list = []
    for f in opts.fields + opts.many_to_many:
        if not f.editable or isinstance(f, models.AutoField):
            continue
        field_list.append(f.name)
    return field_list

def get_labels_and_data_1obj(model, oggetto=None, cap=None, esc=None):
    opts = model._meta
    data_list=[]
    for f in opts.fields + opts.many_to_many:
        line=[]
        if not f.editable or isinstance(f, models.AutoField):
            continue
        data_list.append([format_name(f.name), f.value_from_object(oggetto)])
    print "data_list", data_list
    return data_list

def get_labels_and_data(model, oggetti=None, cap=True, esc=True):
    opts = model._meta
    field_list = []
    oggettil=None
    data_lists=[]
    if oggetti:
        if not isinstance(oggetti,list):
            oggettil=oggetti
##            oggettil=[oggetti]
        else:
            oggettil=oggetti
    for f in opts.fields:
        if not f.editable or isinstance(f, models.AutoField):
            continue
        field_list.append(f.name)
        if oggettil:
            data_list=[]
            for oggetto in oggettil:
                data_list.append(f.value_from_object(oggetto))
            data_lists.append(data_list)
    return (field_list, zip(*data_lists))

def get_labels_and_data_links(model, oggetti=None, cap=True, esc=True):
    link_f=[0,1,2,6]
    opts = model._meta
    field_list = []
    oggettil=None
    data_lists=[]
    links_lists=[]
    data_links_lists = []
    if oggetti:
        if not isinstance(oggetti,list):
            oggettil=oggetti
##            oggettil=[oggetti]
        else:
            oggettil=oggetti
    for ii, f in enumerate(opts.fields):
        if not f.editable or isinstance(f, models.AutoField):
            continue
        field_list.append(format_name(f.name))
        if oggettil:
            data_list=[]
            links_list=[]
            data_links_list=[]
            for oggetto in oggettil:
                val = f.value_from_object(oggetto)
                data_list.append(val)
                link_item=None
                if ii in link_f:
                    if ii==0:
                        link_item = "/dataitem/"+str(val)
                    if ii==1:
                        link_item = "/datafiles/"+val
                    if ii==2:
                        if val:
                            cod_str=str(val)
                            link_item="http://www.crystallography.net/cif/"+cod_str[0]+"/"+cod_str+".cif"
                    if ii==6:
                        link_item = "/articles/"+str(val)
                links_list.append(link_item)
                data_links_list.append([val, link_item])
            data_lists.append(data_list)
            links_lists.append(links_list)
            data_links_lists.append(data_links_list)
    return (field_list, zip(*data_lists), zip(*links_lists), zip(*data_links_lists))

def view_as_table(modello, oggetti=None, cap=True, esc=True, header=None):
    """
    prints the model header and or instance as a table
    """
    labels, data_mat = get_labels_and_data(modello, oggetti, cap, esc)
    t = get_template('data/data_list_table.html')
    c=Context({
    'header': header,
    'hor_headers_list': labels,
    'data_matrix' : data_mat,
    })
    html_out=t.render(c)
    return html_out

def view_linked_properties_list(oggetti=None, header=None):
    link_f=[1]
    opts = Property._meta
    fields_labels_list = []
    data_links_lists=[]
    my_fields=[opts.fields[2]]+opts.fields[4:]
    for ii, f in enumerate(my_fields):
        fields_labels_list.append(format_name(f.name))        
    if oggetti:
        data_links_list=[]
        for oggetto in oggetti:
            data_links_list=[]
            for ii, f in enumerate(my_fields):
                val = f.value_from_object(oggetto)
                link_item=None
                if ii==0:
                    link_item = "/properties/"+str(opts.fields[0].value_from_object(oggetto))
                    val = val [5:]                
                data_links_list.append([val, link_item])
            data_links_lists.append(data_links_list)
##    return (field_list, zip(*data_links_lists))
    t = get_template('data/properties_list_table_linked.html')
    c=Context({
    'header': header,
    'hor_headers_list': fields_labels_list,
    'data_matrix' : data_links_lists,
    })
    html_out=t.render(c)
    return html_out

def view_linked_articles_list(oggetti=None, header=None):
    link_f=[1]
    opts = PublArticle._meta
    fields_labels_list = []
    data_links_lists=[]
    my_fields=opts.fields[:4]
    for ii, f in enumerate(my_fields):
        fields_labels_list.append(format_name(f.name))        
    if oggetti:
        data_links_list=[]
        for oggetto in oggetti:
            data_links_list=[]
            for ii, f in enumerate(my_fields):
                val = f.value_from_object(oggetto)
                link_item=None
                if ii==0:
                    link_item = "/articles/"+str(val)             
                data_links_list.append([val, link_item])
            data_links_lists.append(data_links_list)
##    return (field_list, zip(*data_links_lists))
    t = get_template('data/articles_list_table_linked.html')
    c=Context({
    'header': header,
    'hor_headers_list': fields_labels_list,
    'data_matrix' : data_links_lists,
    })
    html_out=t.render(c)
    return html_out

def view_obj_as_2cols_table(modello, oggetto=None, cap=None, esc=True, header=None):
    """
    prints the model header and or instance as a 2 cols table
    """
    labels_data = get_labels_and_data_1obj(modello, oggetto, cap, esc)
    t = get_template('data/data_1obj_table.html')
    c=Context({
    'header': header,
    'labels_data': labels_data,
    'caption': cap,
    })
    html_out=t.render(c)
    return html_out

def html_linked_dataitem(dataitem=None):
    """
    prints the model header and or instance as a 2 cols table
    """
    labels_data = get_labels_and_data_1obj(DataFile, dataitem)
    opts = DataFile._meta
    link_f = [0,1,2,6]
    data_links_list = []
    for ii, f in enumerate(opts.fields):
        if not f.editable or isinstance(f, models.AutoField):
            continue
        val = f.value_from_object(dataitem)
        link_item = None
        if ii in link_f:
            if ii==0:
                link_item = "/dataitem/"+str(val)
            if ii==1:
                link_item = "/datafiles/"+val
            if ii==2:
                if val:
                    cod_str=str(val)
                    link_item="http://www.crystallography.net/cif/"+cod_str[0]+"/"+cod_str+".cif"
            if ii==6:
                link_item = "/articles/"+str(val)
        data_links_list.append([format_name(f.name), val, link_item])
    t = get_template('data/data_linked_dataitem.html')
    c=Context({
    'header': "Datafile info",
    'data_links_list': data_links_list,
    })
    html_out=t.render(c)
    return html_out

def view_as_linked_table(modello, oggetti=None, cap=True, esc=True, header=None):
    """
    prints the model header and or instance as a table
    linki is a sequence of tuples[(fiels1, link1),(field2, link2),]
    """
    labels, data_mat, links_mat, data_links_mat = get_labels_and_data_links(modello, oggetti, cap, esc)
    t = get_template('data/data_list_table_linked.html')
    c=Context({
    'header': header,
    'hor_headers_list': labels,
    'data_matrix' : data_mat,
    'links_matrix' : links_mat,
    'data_links_matrix' : data_links_mat,
    })
    html_out=t.render(c)
    return html_out

def data_item_html(dataitem_id):
    datafile_item = None
    try:
        datafile_item = DataFile.objects.get(code__exact = dataitem_id)
    except:
        return None, None
    mpod_filepath = os.path.join(datafiles_path, dataitem_id+".mpod")
    file_data_blocks = parse_mpod_file(mpod_filepath)
    print 'file_data_blocks', file_data_blocks
    tenso_props, nl_props, l_props = all_props_list(file_data_blocks)
    print 'tenso_props', tenso_props
    print 'nl_props', nl_props
    print 'l_props', l_props
    
    
    tenso_props_dims_dict = {}
    tenso_props_ids_dict = {}
    tenso_props_units_dict = {}
    lnl_props_ids_dict = {}
    lnl_props_units_dict = {}
    for tp in tenso_props:
        tprp = Property.objects.get(tag__exact = tp)
        tenso_props_dims_dict[tp] = tprp.tensor_dimensions
        tenso_props_ids_dict[tp] = tprp.id
        tenso_props_units_dict[tp] = tprp.units
    for nlp in nl_props:
        nlprp = ExperimentalParCond.objects.get(tag__exact = nlp)
        lnl_props_ids_dict[nlp] = nlprp.id
        lnl_props_units_dict[nlp] = nlprp.units
    for lp in l_props:
        lprp = ExperimentalParCond.objects.get(tag__exact = lp)
        lnl_props_ids_dict[lp] = lprp.id
        lnl_props_units_dict[lp] = lprp.units
    props_ids = [tenso_props_dims_dict, tenso_props_ids_dict, lnl_props_ids_dict,
     tenso_props_units_dict, lnl_props_units_dict ]
    formatted_data_blocks = format_data_blocks(file_data_blocks, props_ids)
    t_tables = get_template('data/view_dataitem_tensors_new.html')
    html_datafile = html_linked_dataitem(datafile_item)
    c_tables=Context({
    'header': "Property values",
    'formatted_data_blocks' : formatted_data_blocks,
    })
    html_tables = t_tables.render(c_tables)
    return html_datafile, html_tables
