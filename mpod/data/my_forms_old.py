from models import *
from django.db import models
from django.utils.html import escape
from django.template.defaultfilters import capfirst
from django.forms.models import model_to_dict
from django.template.loader import get_template
from django.template import Template
from django.template import Context

from parse_files_1 import *

datafiles_path=os.path.join(os.path.dirname(__file__),'../media/datafiles').replace('\\','/')

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
        data_list.append([f.name, f.value_from_object(oggetto)])
    print data_list
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
        field_list.append(f.name)
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
        fields_labels_list.append(f.name)        
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
    for ii, f in enumerate(opts.fields + opts.many_to_many):
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
        data_links_list.append([f.name, val, link_item])
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
    datafile_item = DataFile.objects.get(code__exact = dataitem_id)
    mpod_filepath = os.path.join(datafiles_path, dataitem_id+".mpod")
    texto = read_file_1(mpod_filepath)
    props_dict, gen_props_dict, specific_props_tags = get_props(texto)
    props_dims_dict = {}
    props_ids_dict = {}
    non_looped_props_ids_dict = {}
    for pk, pv in props_dict.iteritems():
        prp = Property.objects.get(tag__exact = "_prop"+pk)
        props_dims_dict[pv] = prp.tensor_dimensions
        props_ids_dict[pv] = prp.id
        non_looped_props_ids_dict[format_name(pk)] = prp.id
    gen_props_dict_name = {}
    for k,v in gen_props_dict.iteritems():
        gen_props_dict_name[format_name(k)]=v
    props_struct = get_prop_vals_lines(texto, props_dict)
    tables, non_looped_props_dict = make_tables(props_struct, props_dict, specific_props_tags, props_dims_dict, props_ids_dict)
    non_looped_props = []
    for nlpk, nlpv in non_looped_props_dict.iteritems():
        p_ind =  non_looped_props_ids_dict[nlpk]
        non_looped_props.append([p_ind, nlpk, nlpv])
    t_gen_props = get_template('data/view_dataitem_gen_props.html')
    t_tables = get_template('data/view_dataitem_tensors.html')
    html_datafile = html_linked_dataitem(datafile_item)
    c_gen_props=Context({
    'header': "General Experimental conditions",
    'gen_props_dict' : gen_props_dict_name,
    'tables' : tables,
    })
    c_tables=Context({
    'header': "Property values",
    'non_looped_props': sorted(non_looped_props),
    'tables' : tables,
    })
    html_gen_props=t_gen_props.render(c_gen_props)
    html_tables = t_tables.render(c_tables)
    return html_datafile, html_gen_props, html_tables