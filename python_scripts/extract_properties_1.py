import os
import re
import string

cifs_dir='/home/pepponi/work/physdata/mpod/data_files'
core_dic_filepath="/home/pepponi/work/physdata/cif/cif_core.dic"
mpod_dic_filepath="/home/pepponi/work/physdata/mpod/cif_material_properties_2013_10_03.dic"
fds=os.listdir(cifs_dir)
fds2=filter(lambda x: x[-5:]==".mpod",  fds)
filets=sorted(filter(lambda x: os.path.isfile(os.path.join(cifs_dir,  x)), fds2))

def read_file_1(mpod_filepath):
    in_file = open(mpod_filepath, 'r')
    texto = in_file.read()
    in_file.close()
    return texto

def get_data_code(texto):
    lins = map(lambda x: x.strip(), texto.strip().split("\n"))
    code=0
    for li in lins:
        code = get_data_code_lin(li)
        if code>0:
            return code
    if code==0:
        raise Exception('Cid data_ code', 'missing')
    else:
        return code

def get_data_code_lin(lin):
    l=lin.strip()
    if l[0:5]=='data_':
        return int(l[5:])
    else:
        return 0

def get_info_1(texto,  tags):
    vals=[]
    for tag in tags:
        val=""
        rf = texto.find(tag)
        if rf>-1:
            tl=len(tag)
            st=rf+tl
            rf2 = texto[st:].find('\n')
            val=texto[st:st+rf2].strip().strip("'")
        else:
            val = "None"
        vals.append(val)
    return vals

def get_info_title(texto):
    title_lins=[]
    lins = map(lambda x: x.strip(), texto.strip().split("\n"))
    ind=0
    for i, lin in enumerate(lins):
        if lin.find("_publ_section_title")>-1:
            ind = i
            break
    flag = True
    j=2
    while flag:
        stripped = lins[ind+j].strip().strip("'").strip()
        if stripped[0]==";":
            break
        else:
            title_lins.append(stripped)
            j=j+1
    return " ".join(title_lins)

def get_info_authors(texto):
    authors=[]
    lins = map(lambda x: x.strip(), texto.strip().split("\n"))
    ind=0
    for i, lin in enumerate(lins):
        if lin.find("_publ_author_name")>-1:
            ind = i
            break
    if lins[ind-1]=="loop_":
        flag = True
        j=1
        while flag:
            stripped = lins[ind+j].strip().strip("'").strip()
            if stripped[0]=="_":
                break
            else:
                authors.append(stripped)
                j=j+1
    else:
        authors_stri = lins[ind][len('_publ_author_name'):].strip().strip("'").strip()
        if authors_stri.find(',')>-1:
            authors = authors + authors_stri.split(',')
        else:
            authors.append(authors_stri)
    return authors

def publi_sql(id, publi_vals, title, authors):
    kss = "id, title, authors, journal, year, volume, issue, first_page, last_page, reference, pages_number"
    ks = map(lambda x: x.strip(), kss.split(","))
    formatss = "%d, %s, %s, %s, %d, %s, %s, %d, %d, %s, %d"
    formats = map(lambda x: x.strip(), formatss.split(","))
    func=None
    tks = []
    tvs = []
    fs =[]
    publi_vals=[publi_vals[0]]+[title]+[authors]+publi_vals[1:]
    for i,v in enumerate(publi_vals):
        if not v=="None":
            f=formats[i]
            if f=='%d':
                func=int
            if f=='%s':
                func=lambda x: "'"+str(x)+"'"
            if f=='%f':
                func=float
            try:
                vv=func(v)
                tks.append(ks[i])
                tvs.append(vv)
                fs.append(f)
            except:
                pass
    tags_st = ", ".join(tks)
    frms_st = ", ".join(fs)
    vals_tup = tuple(tvs)
    text_publi="INSERT INTO data_publarticle ("+tags_st+ ") VALUES (" + frms_st+ ");"
    return text_publi %vals_tup

def gen_info_sql(id, publi_id, info_vals):
    kss="code, filename, cod_code, phase_generic, phase_name, chemical_formula, publication_id"
    ks = map(lambda x: x.strip(), kss.split(","))
    formatss = "%d, %s, %d, %s, %s, %s, %d"
    formats = map(lambda x: x.strip(), formatss.split(","))
    func=None
    tks = []
    tvs = []
    fs =[]
    info_vals=[id]+info_vals+[publi_id]
    for i,v in enumerate(info_vals):
        if not v=="None":
            f=formats[i]
            if f=='%d':
                func=int
            if f=='%s':
                func=lambda x: "'"+str(x)+"'"
            if f=='%f':
                func=float
            try:
                vv=func(v)
                tks.append(ks[i])
                tvs.append(vv)
                fs.append(f)
            except:
                pass
    tags_st = ", ".join(tks)
    frms_st = ", ".join(fs)
    vals_tup = tuple(tvs)
    text_gen="INSERT INTO data_datafile ("+tags_st+ ") VALUES (" + frms_st+ ");"
    return text_gen %vals_tup

def format_vals(vals, formats):
    func=None
    tvs = []
    fs =[]
    for i,v in enumerate(vals):
        if not v=="None":
            f=formats[i]
            if f=='%d':
                func=int
            if f=='%s':
                func=lambda x: "'"+str(x)+"'"
            if f=='%f':
                func=float
            try:
                vv=func(v)
                tvs.append(vv)
                fs.append(f)
            except:
                pass
    frms_st = ", ".join(fs)
    vals_tup = tuple(tvs)
    return tvs

def get_props(texto):
    tg="_prop"
    ntgs= ['conditions','measurement','frame','symmetry', 'data']
    props=[]
    props_agg=[]
    lins = map(lambda x: x.strip(), texto.strip().split("\n"))
    ind=0
    for i, lin in enumerate(lins):
        if lin.find(tg)>-1:
            lcs=lin.split()
            prstr=lcs[0].strip()[5:]
            parts=prstr.split('_')
            if parts[1] in ntgs:
                if prstr not in props_agg:
                    props_agg.append(prstr)
            else:
                if prstr not in props:
                    props.append(prstr)
    return props, props_agg


def props_info_in_dic(props):
    props_info = {}
    tgs = ['_name','_category','_type','_type_conditions','_list', '_units', '_units_detail']
    texto = read_file_1(mpod_dic_filepath)
    lins = map(lambda x: x.strip(), texto.strip().split("\n"))
    for prop in props:
        pro_str = "data_prop"+prop
        print pro_str
        for ii, lin in enumerate(lins):
            ind = None
            if lin.startswith(pro_str):
                ind = ii
                break
        cond = True
        jj=1
        if ind:
            props_info[prop] = {}
            while cond:
                pl = lins[ind+jj]
                if pl:
                    plps = pl.split(None, 1)
                    try:
                        tg, vtg = plps
                    except:
                        cond = False
                    tg =tg.strip().strip("'").strip()
                    vtg =vtg.strip().strip("'").strip()
                    if tg in tgs:
                        indt = tgs.index(tg)
                        props_info[prop][tg] = vtg
                jj = jj+1
                if jj > len(tgs) + 1 :
                    cond = False
    print "fatto"
    return props_info



if __name__ == "__main__":
    tg="_prop"
    props = []
    data_props={}
    for i, fil in enumerate(filets):
        filepath=os.path.join(cifs_dir, fil)
        texto = read_file_1(filepath)
        code = get_data_code(texto)
        this_props, this_props_agg = get_props(texto)
        inds = []
        for pr in this_props:
            if not pr in props:
                props.append(pr)
    props = sorted(props)
    for i, fil in enumerate(filets):
        filepath=os.path.join(cifs_dir, fil)
        texto = read_file_1(filepath)
        code = get_data_code(texto)
        this_props, this_props_agg = get_props(texto)
        inds=[]
        for pr in this_props:
            prop_ind=props.index(pr)+1
            inds.append(prop_ind)
        data_props[code]=inds
    print props, data_props
    db_fields = ["id", "tag", "description", "tensor_dimensions", "units", "units_detail"]
    db_fields_str = ', '.join(db_fields)
    print
    print
    sql_lins = []
    for i_pr, pr in enumerate(props):
        the_vals = [tg+pr,pr]
        formats = ['%s', '%s']
        the_vals_2 = format_vals(the_vals, formats)
        record_vals_str = ', '.join(the_vals_2)
        sql_lin="INSERT INTO data_property (" + db_fields_str + ") VALUES (" + str(i_pr+1) + ", "+  record_vals_str + ", 0, 'NULL', 'NULL');"
        sql_lins.append(sql_lin)
    db_fields = ["datafile_id", "property_id"]
    db_fields_str = ', '.join(db_fields)
    for dp in sorted(data_props.keys()):
        for prn in data_props[dp]:
            record_vals_str = ', '.join([str(dp),str(prn)])
            sql_lin="INSERT INTO data_datafile_property (" + db_fields_str + ") VALUES (" + record_vals_str + ");"
            sql_lins.append(sql_lin)
    aa = props_info_in_dic(props)
    tgs = ['_name', '_units', '_units_detail']
    sql_lins2 = []
    for prop in props:
        tp = prop
        print tp
        na = aa[tp]['_name']
        un = aa[tp]['_units']
        ud = aa[tp]['_units_detail']
        lin1 = "UPDATE data_property SET name = " + "'" + ' '.join(na.split('_')) + "'" + "WHERE tag = " + "'" + tg+prop + "';"
        lin2 = "UPDATE data_property SET units = " + "'" + un + "'" + "WHERE tag = " + "'" + tg+prop + "';"
        lin3 = "UPDATE data_property SET units_detail = " + "'" + ud + "'" + "WHERE tag = " + "'" + tg+prop + "';"
        sql_lins2.append(lin1)
        sql_lins2.append(lin2)
        sql_lins2.append(lin3)
    head = "USE giancarlo_mpod;\nDELETE FROM data_property;\nDELETE FROM data_datafile_property;\n"
    tail = "\nCOMMIT;\n"
    sql_text=head+ "\n".join(sql_lins) + "\n" + "\n".join(sql_lins2) + tail
    print sql_text
    out_file_path = "/home/pepponi/work/physdata/mpod/load_properties_2013_10_08.sql"
    out_file = open(out_file_path,"w")
    out_file.write(sql_text)
    out_file.close()
    for prop in props:
        lin3 = "UPDATE data_property SET tensor_dimensions = '0' " + "WHERE tag = " + "'" + tg+prop + "';"
        print lin3
