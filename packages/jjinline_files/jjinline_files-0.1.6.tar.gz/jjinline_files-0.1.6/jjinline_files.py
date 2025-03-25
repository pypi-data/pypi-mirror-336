""" jj Inline files - "not so pythonic" files inside your code
"""

__version__ = "0.1.6"

import inspect
import jinja2 as jj2, json, yaml, csv
import pypugjs
import re

dic = {}

def perror(msg):
    print("Erro! " + msg)
    exit(1)

def __init__jj():
    # descobrir o path
    path = inspect.stack()[-1].filename
    
    # abrir o ficheiro
    f = open(path).read()

    # procurar por declarações in file FIXME
    infile = re.search(r'("""|\'\'\')ILF((.+?|\n)+)("""|\'\'\')', f)

    try:
        infile = infile.group(2)
        infile = re.sub(r'^==> ?---.+$', '', infile, flags=re.M )   #rem ==>--- comment


        files = re.split(r'==>[ \t]*', infile)[1:]
        for file in files:
            name,cont = re.split(r'\n', file, maxsplit=1)
            name = name.strip()

            if name in dic:
                perror(f"Error '{name}': Ficheiro duplicado")
            dic[name] = cont.rstrip()

    except:
        perror("No inlinefile found here...")

    for name,cont in dic.copy().items():
        if   n := re.match(r'(\w+):json$', name) : dic[ n[1] ] = get_json(cont)
        elif n := re.match(r'(\w+):yaml$', name) : dic[ n[1] ] = get_yaml(cont)
        elif n := re.match(r'(\w+):jj2$', name)  : dic[ n[1] ] = get_jj2(cont)
        elif n := re.match(r'(\w+):pughtml$', name) : dic[ n[1] ] = get_pughtml(cont)
        elif n := re.match(r'(\w+):pugjj2$', name) : dic[ n[1] ] = get_pugjj2(cont)
        elif n := re.match(r'(\w+):f$', name)    : dic[ n[1] ] = get_f(cont)
        elif n := re.match(r'(\w+):csv$', name)  : dic[ n[1] ] = get_csv(cont)
        elif n := re.match(r'(\w+):tsv$', name)  : dic[ n[1] ] = get_tsv(cont)
        elif n := re.match(r'(\w+):lines$', name): dic[ n[1] ] = get_lines(cont)
        elif n := re.match(r'(\w+)(\W.*)',  name): perror(f'Error: {name} - unknown type {n[2]}')

        else: pass

def get_json(cont : str) -> any:
    return json.loads(cont)

def get_yaml(cont : str) -> any:
    return yaml.safe_load(cont)

def get_jj2(cont : str) -> any:         ## Jinja2 template
    temp= jj2.Template(cont)
    def auxf(d={} , **args):
        return temp.render( **d, **args)
    return auxf

def get_pughtml(cont : str) -> any:         ## pugified HTML
    return pypugjs.simple_convert(cont)

def get_pugjj2(cont : str) -> any:         ## pugified Jinja2 template
    temp1 = pypugjs.simple_convert(cont)
    temp= jj2.Template(temp1)
    def auxf(d={} , **args):
        return temp.render( **d, **args)
    return auxf

def get_f(cont):
    def auxf(d={} , **args):
        return eval(f"""f'''{cont}'''""", {**d, **args})
    return auxf

def get_tsv(cont):
    return list(csv.reader(cont.splitlines(),skipinitialspace=True, delimiter="\t"))

def get_csv(cont):
    return list(csv.reader(cont.splitlines(),skipinitialspace=True))

def get_lines(cont):
    return cont.splitlines()

__init__jj()
globals().update(dic)
__all__ = list(dic)

