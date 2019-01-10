#!/usr/bin/env python

'''
read an sql database with observation settings
'''

import sqlite3
from sqlite3 import Error


def read_observation_parameters(args, db_file):


    print(args)
    print(db_file)

    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)



    cur = conn.cursor()
    cur.execute("SELECT target,configuration, phase_cal, line_if, cont_if, project, files, notes FROM observation WHERE id=" + str(args.id))
    obs_val = cur.fetchall()
    print(obs_val)
    obs_keys = [description[0] for description in cur.description]
    obs_par = dict(zip(obs_keys,obs_val[0]))

    # read other relevant parameters for the galaxy
    cur.execute("SELECT vel,vel_min,vel_max FROM galaxy WHERE target=" + repr(obs_par['target']))
    extra_val = cur.fetchall()
    print(extra_val)
    extra_keys = [description[0] for description in cur.description]
    extra_par = dict(zip(extra_keys,extra_val[0]))

    # add the extra paramaters to the dicitionary
    obs_par.update(extra_par)


    return obs_par





