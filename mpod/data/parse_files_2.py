import os
import re
import string
import numpy as np

cifs_dir='/home/pepponi/work/physdata/mpod/data_files'

def format_name(prop_tag):
    pr = prop_tag.strip('_')
    return " ".join(pr.split('_'))

def read_file_1(mpod_filepath):
    in_file = open(mpod_filepath, 'r')
    texto = in_file.read()
    in_file.close()
    return texto

def split_lins(texto):
    return map(lambda x: x.strip(), texto.strip().split("\n"))

def get_loops(block_lins):
    non_loop_lines=[]
    non_loop_lines_dic={}
    loops = []
    loops_start_inds=[]
    loops_end_inds=[]
    il = 0
    loop_n = 0
    len_lins = len(block_lins)
    il2= 0
    loop_flag = False
    while il<len_lins:
        if block_lins[il].startswith("loop_"):
            loop_flag = True
            non_loop_lines_dic[loop_n]=non_loop_lines
            loop_n = loop_n + 1
            loop_tags = []
            loop_val_lins = []
            loops_start_inds.append(il+1)
            n_tags = 0
            vals_found = False
            for iloli, loli in enumerate(block_lins[il+1:]):
                if loli.strip().startswith("_"):
                    if vals_found == False:
                        loop_tags.append(loli.strip())
                    else:
                        loops_end_inds.append(il2)
                        il = il2
                        break
                else:
                    vals_found = True
                    loop_val_lins.append(loli)
                    il2 = il+1+iloli+loop_n
            loops.append([loop_tags, loop_val_lins])
            non_loop_lines=[]
            il = il2
        else:
            non_loop_lines.append(block_lins[il])
            il = il+1
            loop_flag = False
    if not loop_flag:
        loops.append([[None], [None]])
        non_loop_lines_dic[loop_n]=non_loop_lines
    return loops, non_loop_lines_dic

def divide_loop_secs(loop):
    loop_tags, loop_val_lins = loop
    if loop_tags[0]==None:
        return [None]
    vals = []
    sections = {}
    props_flag = False
    tensor_flag = False
    uncertainty_flag = False
    props = []
    cond_start = 2
    if len(loop_tags) == 1:
        vals  = map(lambda x: x.strip().strip("'").strip(), loop_val_lins )
        return [loop_tags[0], vals]
    for li in loop_val_lins:
        lips = map(lambda x: x.strip(), li.strip().split())
        vals.append(lips)
    if "_prop_data_label" in loop_tags:
        props_label_flag = True
    if "_prop_data_tensorial_index" in loop_tags:
        tensor_flag = True
        cond_start = 3
    if "_prop_data_uncertainty" in loop_tags:
        uncertainty_flag = True
        cond_start = 4
    if props_label_flag:
        vals_sections = {}
        conds=[]
        flag = True
        if tensor_flag:
            for valo in vals:
                tag = valo[0]
                conds_tags = map(lambda x: x[6:], loop_tags[cond_start:]) #era 3
                cond = valo[cond_start:]
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
                if uncertainty_flag:
                    vals_sections[cond_ind][tag].append([valo[1], valo[2]+'('+valo[3]+')'])
                else:
                    vals_sections[cond_ind][tag].append(valo[1:3])
            return [conds_tags, conds, vals_sections]
        else:
            for valo in vals:
                tag = valo[0]
                tags = []
                if vals_sections.has_key(tag):
                    pass
                else:
                    vals_sections[tag]=[]
                vals_sections[tag].append(valo[1:])
            conds_tags = map(lambda x: x[6:], loop_tags[2:])
            return [conds_tags, vals_sections]

def get_non_looped_props(non_looped_lines):
    btg="_prop"
    otgs = ["phase", "symmetry", "structure"]
    ntgs = ['conditions', 'measurement', 'frame', 'symmetry' ]
    props_desc = {}
    props_tens2 = {}
    props_tens = {}
    other_props = {}
    if non_looped_lines[-1].isdigit():
        pass
    for lin in non_looped_lines:
        first = ''
        if lin.startswith('_'):
            first = lin.split('_')[1]
        if lin.startswith(btg):
            lcs=lin.split()
            pr_str=lcs[0].strip()[6:]
            parts=pr_str.split('_')
            if parts[0] in ntgs:
                if pr_str not in props_desc:
                        props_desc[pr_str] = lcs[1].strip().strip("'").strip()
            else:
                if pr_str not in props_tens:
                    props_tens2[pr_str] = lcs[1].strip().strip("'").strip()
        if first in otgs:
            olcs=lin.split()
            opr_str=olcs[0].strip()
            opr_val=olcs[1].strip().strip("'").strip()
            other_props[opr_str] = opr_val
    for k,v in props_tens2.iteritems():
        props_tens[v]=k
    return props_desc, props_tens, other_props

def parse_mpod_file(filepath):
    texto = read_file_1(filepath)
    data_blocks = texto.split("\ndata_")
    sections=[]
    file_data_blocks = []
    for db in data_blocks[1:]:
        bl_lins = split_lins(db)
        loops, non_loop_lines_dic = get_loops(bl_lins)
        for ln, loop in enumerate(loops):
            non_looped_props = get_non_looped_props(non_loop_lines_dic[ln])
            loop_structs = divide_loop_secs(loop)
            file_data_blocks.append([non_looped_props, loop_structs])
    return file_data_blocks

def format_data_blocks(file_data_blocks, props_ids):
    [tenso_props_dims_dict, tenso_props_ids_dict,
     lnl_props_ids_dict, tenso_props_units_dict, lnl_props_units_dict] = props_ids
    formatted_blocks = []
    for db in file_data_blocks:
        print
        print "dbdbdb"
        print
        print db
        print
        print props_ids
        print
        block = []
        block_head = []
        if db[0][0]:
            for k, v in db[0][0].iteritems():
                propf_id = lnl_props_ids_dict["_prop_"+k]
                propf_unit = ""
                propf_uni = lnl_props_units_dict["_prop_"+k]
                if propf_uni != "n.a." and propf_uni != "1":
                    propf_unit = "[" + propf_uni + "]"
                block_head.append([format_name(k), propf_id, propf_unit, v.strip("'")])
        if db[0][1]:
            if len(db[1])==3:
                for sec_n, sec_v in db[1][2].iteritems():
                    sec = []
                    sec_head = []
                    if db[1][0]:
                        for iv, vv in enumerate(db[1][0]):
                            propl_id = lnl_props_ids_dict["_prop_"+vv]
                            propl_unit = ""
                            propl_uni = lnl_props_units_dict["_prop_"+vv]
                            if propl_uni != "n.a." and propl_uni != "1":
                                propl_unit = "[" + propl_uni + "]"
                            sec_head.append([format_name(vv), propl_id, propl_unit, db[1][1][int(sec_n)][iv].strip("'")])
                    else:
                        sec_head.append(None)
                    print 'sec_v ', sec_v
                    print db[0][1]
                    print tenso_props_dims_dict
                    print tenso_props_ids_dict
                    print tenso_props_units_dict
                    sec = format_tensor_sec(sec_v, db[0][1],
                                tenso_props_dims_dict, tenso_props_ids_dict, tenso_props_units_dict)
                    block.append([sec_head, sec])
            else:
                if db[1][0] is not None:
                    if db[1][1]:
                        other_props = None
                        if db[1][0]:
                            other_props = db[1][0]
                        for sec_tag, sec_vals in db[1][1].iteritems():
                            sec = format_non_tensor_sec(sec_tag, sec_vals, db[0][1],
                            other_props, tenso_props_ids_dict, lnl_props_ids_dict,
                            tenso_props_units_dict, lnl_props_units_dict)
                            print "sec_tag", sec_tag
                            block.append([None, sec])
                else:
                    other_props = None
                    for sec_tag, sec_vals in db[0][1].iteritems():
#                        aa = bb
                        sec = format_non_tensor_sec(sec_tag, sec_tag, db[0][1],
                        other_props, tenso_props_ids_dict, lnl_props_ids_dict,
                        tenso_props_units_dict, lnl_props_units_dict)
                        print "sec_tag", sec_tag
                        block.append([None, sec])
        if not db[0][0]:
            if db[1][0] == '_publ_author_name':
                pass
        formatted_blocks.append([block_head, block])
    return formatted_blocks

def get_dimension(tensor_vals):
    dims = []
    indexes = []
    for cop in tensor_vals:
        indexes.append(map(lambda x: int(x), cop[0]))
    indexes = np.transpose(indexes)
    for ind in indexes:
        dims.append(np.max(ind))
    return dims

def format_tensor_sec(tensor_loop_data_sec, props_tags,
                      tenso_props_dims_dict, tenso_props_ids_dict, tenso_props_units_dict):
    n_sec = []
    print "tlds", tensor_loop_data_sec
    for tag, vals in tensor_loop_data_sec.iteritems():
        dim1 = 0
        dim2 = 0
        dim3 = 0
        dims = []
        prop_name = format_name(props_tags[tag])
        prop_tag = "_prop_"+props_tags[tag]
        prop_id = tenso_props_ids_dict[prop_tag]
        prop_unit = ""
        prop_uni = tenso_props_units_dict[prop_tag]
        if prop_uni != "n.a." and prop_uni != "1":
            prop_unit = "[" + prop_uni + "]"
        dimensions = tenso_props_dims_dict[prop_tag]
        print "prop_name", prop_name, prop_tag, prop_id, prop_unit, dimensions

        try:
            dimensions = tenso_props_dims_dict[prop_tag]
            if dimensions.find(',')>-1:
                dims = map(lambda x: int(x.strip()), dimensions.strip().split(","))
                dim1 = dims[0]
            else:
                dim1 = int(dimensions.strip())
        except:
            pass
        if not dim1:
            dims = get_dimension(vals)
            dim1 = dims[0]
            dim2 = 0
            dim3 = 0
        tenso = []
        if len(dims)==3:
            dim3 = dims[2]
            dim2 = dims[1]
            for i1 in range(dim1):
                tenso.append([])
                for i2 in range(dim2):
                    tenso[i1].append([])
                    for i3 in range(dim3):
                        tenso[i1][i2].append("-")
        elif len(dims)==2:
            dim2 = dims[1]
            for i in range(dim1):
                tenso.append([])
                for j in range(dim2):
                    tenso[i].append("-")
        else:
            tenso=[[]]
            for i in range(dim1):
                tenso[0].append("-")
        print "vals", vals
        for ele in vals:
            val = ele[1]
            if dim3:
                ind1 = int(ele[0][0])-1
                ind2 = int(ele[0][1])-1
                ind3 = int(ele[0][2])-1
                tenso[ind1][ind2][ind3] = val
            elif dim2:
                ind1 = int(ele[0][0])-1
                ind2 = int(ele[0][1])-1
                tenso[ind1][ind2] = val
            else:
                ind1 = int(ele[0])-1
                if tenso[0]!=[]:
                    tenso[0][ind1] = val
                else:
                    tenso[0]=[ele[1]]
        n_sec.append([prop_name, prop_id, prop_unit, tenso])
    return n_sec

def format_non_tensor_sec(sec_tag, sec_vals, props_tags, other_props,
                          tenso_props_ids_dict, lnl_props_ids_dict,
                          tenso_props_units_dict, lnl_props_units_dict):
    sec_prop_tag = props_tags[sec_tag]
    sec_prop_name = format_name(sec_prop_tag)
    sec_prop_tag = "_prop_" + sec_prop_tag
    sec_prop_unit = ""
    sec_prop_uni = ""
    if sec_vals==sec_tag:
        sec_vals = [[sec_vals]]
    try:
        sec_prop_id = tenso_props_ids_dict[sec_prop_tag]
        sec_prop_uni = tenso_props_units_dict[sec_prop_tag]
    except:
        sec_prop_id = lnl_props_ids_dict[sec_prop_tag]
        sec_prop_uni = lnl_props_units_dict[sec_prop_tag]
    if sec_prop_uni != "n.a." and sec_prop_uni != "1":
        sec_prop_unit = " [" + sec_prop_uni + "]"
    sec_prop = [sec_prop_name, sec_prop_id, sec_prop_unit, True]
    oprps = []
    if other_props:
        for prp in other_props:
            prp_name = format_name(prp)
            prp_id = lnl_props_ids_dict["_prop_"+prp]
            prp_uni = lnl_props_units_dict["_prop_"+prp]
            prp_unit = ""
            if prp_uni != "n.a." and prp_uni != "1":
                prp_unit = " [" + prp_uni + "]"
            oprps.append([prp_name, prp_id, prp_unit, False])
        sec_header = [sec_prop]+oprps
    else:
        sec_header = [sec_prop]
    return [sec_header, sec_vals]

def format_tensor(tensor_loop_data, props_tags):
    all_secs = []
    for sec_n, sec_v in tensor_loop_data.iteritems():
        n_sec = format_tensor_sec(sec_v, props_tags)
        all_secs.append(n_sec)
    return all_secs

def all_props_list(file_data_blocks):
    tlps = []
    nlps = []
    lps = []
    for db in file_data_blocks:
        non_looped_props, loop_structs = db
        for k,v in non_looped_props[0].iteritems():
            nlps.append("_prop_"+k)
        for k,v in non_looped_props[1].iteritems():
            tlps.append("_prop_"+v)
        if type(loop_structs[0]) == type(""):
            if not loop_structs[0].startswith("_"):
                lps.append(loop_structs[0])
        if type(loop_structs[0]) == type([]):
            for ls in loop_structs[0]:
                lps.append("_prop_"+ls)
    return tlps, nlps, lps

if __name__ == "__main__":
    tg="_prop"
    props = []
    fil = "1000201.mpod"
#    fil = "1000097.mpod"
#    fil = "1000272.mpod"
    fil = "1000196.mpod"
    filepath=os.path.join(cifs_dir, fil)
    file_data_blocks = parse_mpod_file(filepath)
    bb = all_props_list(file_data_blocks)
#    aa = format_data_blocks(file_data_blocks)
    print bb
#    print aa
    print "fatto"
