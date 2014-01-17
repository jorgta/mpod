import os
import re
import string

cifs_dir='/home/gian/work/physdata/mpod/data_files'

def format_name(prop_tag):
    pr = prop_tag.strip('_')
    return " ".join(pr.split('_'))

def read_file_1(mpod_filepath):
    in_file = open(mpod_filepath, 'r')
    texto = in_file.read()
    in_file.close()
    return texto

def get_props(texto):
    tg="_prop"
    ntgs = ['conditions','measurement','frame','symmetry', 'data']
    props = {}
    props_gen = {}
    specific_props_tags = []
    lins = map(lambda x: x.strip(), texto.strip().split("\n"))
    ind=0
    for i, lin in enumerate(lins):
        if lin.find(tg)>-1:
            lcs=lin.split()
            prstr=lcs[0].strip()[5:]
            parts=prstr.split('_')
            if parts[1] in ntgs:
                if prstr not in props_gen:
                    try:
                        props_gen[prstr] = lcs[1].strip().strip("'").strip()
                    except:
                        specific_props_tags.append(prstr)
                        pass
            else:
                if prstr not in props:
                    props[prstr] = lcs[1].strip().strip("'").strip()
    specific_props_tags = specific_props_tags[3:]
    return props, props_gen, specific_props_tags

def get_prop_vals_lines(texto, props_dict):
    parts = texto.split("loop_")
    good = parts[-1].strip()
    lins = map(lambda x: x.strip(), good.strip().split("\n"))
    ind=0
    loop_tags = []
    for i, lin in enumerate(lins):
        if lin.strip()[:5] == "_prop":
            loop_tags.append(lin.strip())
        else:
            ind=i
            break
    val_lins = lins[ind:]
    vals = []
    for li in val_lins:
        lips = map(lambda x: x.strip(), li.strip().split())
        vals.append(lips)
    vals_sections = {}
    conds=[]
    flag = True
    for valo in vals:
        tag = valo[0]
        cond = valo[3:]
        cond_ind = None
        if cond in conds:
            cond_ind = conds.index(cond)
            if vals_sections[cond_ind].has_key(tag):
                pass
            else:
                vals_sections[cond_ind][tag]=[]
        else:
            conds.append(cond)
            cond_ind = conds.index(cond)
            vals_sections[cond_ind] = {}
            vals_sections[cond_ind][tag]=[]
        vals_sections[cond_ind][tag].append(valo[1:3])
    return conds, vals_sections
    

def make_tables(props_struct, props_dict, specific_props_keys, props_dims_dict, props_ids_dict):
    print "props_dims_dict", props_dims_dict
    props_dict2 = {}
    for k,v in props_dict.iteritems():
        props_dict2[v]=format_name(k)
    specific_props = props_struct[0]
    sections = props_struct[1]
#    new_sections = {}
    new_sections = []
    rem_props = []
    for ind, sec in sections.iteritems():
        sec_name = "Experimental conditions "+str(ind)
        new_sec={}
        tables = []
        new_sec['tables'] = tables
        new_sec["specific_exp_conds"] = {}
        this_specific_props = specific_props[ind]
        for si, spk in enumerate(specific_props_keys):
            new_sec["specific_exp_conds"][format_name(spk)]=this_specific_props[si]
##            new_sec["specific_exp_conds"].append([format_name(spk), this_specific_props[si]])
        for pf, tens in sec.iteritems():
            prop = props_dict2[pf]
            rem_props.append(pf)
            prop_id = props_ids_dict[pf]
            dimensions = props_dims_dict[pf]
            dim1 = 0
            dim2 = 0
            if dimensions.find(',')>-1:
                dim1, dim2 = map(lambda x: int(x.strip()), dimensions.strip().split(","))
            else:
                dim1 = int(dimensions.strip())
            tenso = []
            props = "" 
            if dim2:
                for i in range(dim1):
                    tenso.append([])
                    for j in range(dim2):
                        tenso[i].append("-")
            else:
                tenso=[[]]
                for i in range(dim1):
                    tenso[0].append("-")
            for ele in tens:
                val = ele[1]
                if dim2: 
                    ind1 = int(ele[0][0])-1
                    ind2 = int(ele[0][1])-1 
                    tenso[ind1][ind2] = val
                else:
                    ind1 = int(ele[0])-1
                    tenso[0][ind1] = val
##            new_sec['tables'][prop]=tenso
            new_sec['tables'].append([prop, prop_id, tenso])
#        new_sections[sec_name] = new_sec
        new_sections.append(new_sec)
    non_looped_props = {}
    for k,v in props_dict2.iteritems():
        if k not in rem_props:
            non_looped_props[v]=k
##    print "props_struct"
##    print specific_props
##    print sections
##    print "fatto"
##    print new_sections
    return new_sections, non_looped_props


if __name__ == "__main__":
    tg="_prop"
    props = []
    fil = "1000044.mpod"
    filepath=os.path.join(cifs_dir, fil)
    texto = read_file_1(filepath)
    props_dict, agg_props_dict, specific_props_tags = get_props(texto)
    props_struct = get_prop_vals_lines(texto, props_dict)
    tables = make_tables(props_struct, props_dict, specific_props_tags)
    print specific_props_tags
    print agg_props_dict
    print tables