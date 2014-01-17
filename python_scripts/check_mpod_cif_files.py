import CifFile
import os

cifs_dir='/home/pepponi/work/physdata/mpod/data_files/new_2013_10_01/copy/copy'
#cifs_dir="/home/gian/work/physdata/mpod/data_files"
core_dic_filepath="/home/pepponi/work/physdata/cif/cif_core.dic"
mpod_dic_filepath="/home/pepponi/work/physdata/mpod/cif_material_properties_2013_10_03.dic"
fds=os.listdir(cifs_dir)
fds2=filter(lambda x: x[-5:]==".mpod",  fds)
filets=sorted(filter(lambda x: os.path.isfile(os.path.join(cifs_dir,  x)), fds2))
core_dic = CifFile.CifDic(core_dic_filepath)
mpod_dic = CifFile.CifDic(mpod_dic_filepath)

for fil in filets[:]:
    filepath=os.path.join(cifs_dir, fil)
    print filepath
    df=CifFile.ReadCif(filepath)
    val_report = CifFile.validate(filepath,  diclist=[core_dic_filepath, mpod_dic_filepath])
    print CifFile.validate_report(val_report)
    print df.keys()

for fil in filets[:]:
    filepath=os.path.join(cifs_dir, fil)
    print filepath
    in_file = open(filepath, 'r')
    lins = in_file.readlines()
    in_file.close()
    ind_beg = 0
    for i_l, lin in enumerate(lins):
        if lin.startswith('data_1000'):
            ind_beg = i_l
            break
    new_lins = lins[:ind_beg]

    new_lins2 = []
    for li in lins[ind_beg:]:
        if not li.startswith('#'):
            new_lins.append(li)

    new_lins.extend(new_lins2)

    texto = '\n'.join(new_lins)
    out_file = open(filepath, 'rw')
    out_file.write(texto)
    out_file.close()
