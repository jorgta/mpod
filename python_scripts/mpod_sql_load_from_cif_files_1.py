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
                func=lambda x: '"'+str(x)+'"' if x.find("'")!=-1 else "'"+str(x)+"'"
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

def gen_info_sql(info_vals, publi_id):
    kss="code, filename, cod_code, phase_generic, phase_name, chemical_formula, publication_id"
    ks = map(lambda x: x.strip(), kss.split(","))
    formatss = "%d, %s, %d, %s, %s, %s, %d"
    formats = map(lambda x: x.strip(), formatss.split(","))
    func=None
    tks = []
    tvs = []
    fs =[]
    info_vals=info_vals+[publi_id]
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

if __name__ == "__main__":
    gen_tags = ['_cod_database_code', '_phase_generic', '_phase_name', '_chemical_formula_sum']
    publi_tags = ['_journal_name_full', '_journal_year', '_journal_volume',
                  '_journal_issue', '_journal_page_first', '_journal_page_last',
                  '_journal_article_reference', '_journal_pages_number' ]
    sql_lins_1=[]
    sql_lins_2=[]
    gen_info_lins=[]
    publi_info_lins=[]
    titles=[]
    ii = 1
    for i, fil in enumerate(filets):
        print fil
        filepath=os.path.join(cifs_dir, fil)
        texto = read_file_1(filepath)
        title = get_info_title(texto)
        if title in titles:
            ind=1+titles.index(title)  #python indexing starts from 0 index of publis from 1
        else:
            titles.append(title)
            publi_vals=[ii]
            publi_vals = publi_vals + get_info_1(texto, publi_tags)
            authors = get_info_authors(texto)
            authors_str = "; ".join(authors)
            title = get_info_title(texto)
            aa = publi_sql(ii, publi_vals, title, authors_str)
            sql_lins_1.append(aa)
            ind = ii
            ii = ii+1
        code = get_data_code(texto)
        gen_vals=[code, fil]
        publi_vals=[ii]
        gen_info_lin = ""
        publi_info_lin = ""
        gen_vals = gen_vals + get_info_1(texto, gen_tags)
#        print i, ind, gen_vals
        bb = gen_info_sql(gen_vals, ind)
        sql_lins_2.append(bb)
#        gen_info_lin = "\t".join(gen_vals)
#        gen_info_lins.append(gen_info_lin)
#        publi_info_lins.append(gen_info_lin)
    text_1 = "\n".join(sql_lins_1)
    text_2 = "\n".join(sql_lins_2)
    head = "USE giancarlo_mpod;\n"
    tail = "\nCOMMIT;\n"
    text_tot = head + text_1 + '\n' +  text_2 +tail
    out_file_path = "/home/pepponi/work/physdata/mpod/load_db_gen_2013_10_24.sql"
    out_file = open(out_file_path, "w")
    out_file.write(text_tot)
    out_file.close()
