import database as dbs
import tables as tabs
import logins as lgs
import sql2op
import ops
import os

raw_path=os.path.dirname(os.path.realpath(__file__))
thispath=raw_path+"/data/"

db0=dbs.db(thispath)
tb0=tabs.ta(thispath)

while(1):
    name=lgs.safes(raw_path)
    ops.mop_init(tb0,thispath,name)
    sql2op.init_sql2op(db0,tb0,name)
    sql2op.getsql()
