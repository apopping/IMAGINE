import ConfigParser
import sys

def read_parameters(par_file):
    cfg=ConfigParser.RawConfigParser()
    cfg.read(par_file)

    par = dict(cfg.items("settings"))

    for p in par:
        par[p]=par[p].split("#",1)[0].strip() # To get rid of inline comments

    globals().update(par)  #Make them availible globally

    return par
