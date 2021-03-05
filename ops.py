import pandas as pd
import numpy as np

PATH=""
Users=""

pd.set_option('display.unicode.ambiguous_as_wide',True)
pd.set_option('display.unicode.east_asian_width',True)
pd.set_option('display.max_columns',None)
pd.set_option('expand_frame_repr',False)
pd.set_option('display.max_rows',None)
pd.set_option('display.width',None)

def op_Insert(dbname,tname,obj_name,value):
    (df,const)=mop_load(dbname,tname,Users)
    if (isinstance(df,int)):
        return
    if (obj_name==[]):
        obj_name=const.columns.tolist()
    if (not mop_changer(df,const,obj_name,value,True)):
        return
    df=df.append(dict(zip(obj_name,value)),ignore_index=True)
    mop_save(df,dbname,tname)

def op_Delete(dbname,tname,op_OBJ,op_B):
    (df,const)=mop_load(dbname,tname,Users)
    if (isinstance(df,int)):
        return
    tmp=mop_muti_Where(df,op_OBJ,op_B)
    df=df.drop(tmp.index)
    mop_save(df,dbname,tname)

def op_Update(dbname,tname,value,op_OBJ,op_B):
    (df,const)=mop_load(dbname,tname,Users)
    if (isinstance(df,int)):
        return
    tmp=np.array(value)
    obj_name=tmp[:,0].tolist()
    obj_value=tmp[:,1].tolist()
    if (not mop_changer(df,const,obj_name,obj_value,False)):
        return
    t=mop_muti_Where(df,op_OBJ,op_B)
    df=df.drop(t.index)
    t=t.copy()
    for i,j in zip(obj_name,obj_value):
        t[i]=j  #t.loc[:,i]=j
    df=pd.merge(df,t,how='outer')
    mop_save(df,dbname,tname)

def op_Select(dbname,tname,value,op_OBJ,op_B):
    (df,const)=mop_load(dbname,tname)
    if (isinstance(df,int)):
        return
    if (value[0]=="*"):
        tmp=mop_muti_Where(df,op_OBJ,op_B)
        if (isinstance(tmp,int)):
            return
        print(tmp)
    else:
        for y in value:
            if (y not in const.columns):
                print("columns \033[36m"+y+"\033[0m is not exist")
                return
        tmp=mop_muti_Where(df,op_OBJ,op_B)
        if (isinstance(tmp,int)):
            return
        print(tmp[value])

def mop_muti_Where(df,op_OBJ,op_B):
    i=0
    if (not op_OBJ==[]):
        tmp=mop_Where(df,i,op_OBJ)
        if (isinstance(tmp,int)):
            return tmp
        for x in op_B:
            i+=1
            if (i<len(op_OBJ)):
                tmp1=mop_Where(df,i,op_OBJ)
                if (isinstance(tmp1,int)):
                    return tmp1
            else:
                return tmp
            if (x=="And"):
                tmp=pd.merge(tmp,tmp1)
            else:
                tmp=pd.merge(tmp,tmp1,how='outer')
        return tmp
    else:
        return df
            

def mop_Where(df,i,op_OBJ):
    if (op_OBJ[i][0] in df.columns.tolist()):
        try:
            if (op_OBJ[i][1]=="!=" or op_OBJ[i][1]=="<>"):
                tmp=df.loc[df[op_OBJ[i][0]]!=op_OBJ[i][2]]
            elif (op_OBJ[i][1]==">"):
                tmp=df.loc[df[op_OBJ[i][0]].astype(int)>int(op_OBJ[i][2])]
            elif (op_OBJ[i][1]=="<"):
                tmp=df.loc[df[op_OBJ[i][0]].astype(int)<int(op_OBJ[i][2])]
            elif (op_OBJ[i][1]==">="):
                tmp=df.loc[df[op_OBJ[i][0]].astype(int)>=int(op_OBJ[i][2])]
            elif (op_OBJ[i][1]=="<="):
                tmp=df.loc[df[op_OBJ[i][0]].astype(int)<=int(op_OBJ[i][2])]
            elif (op_OBJ[i][1]=="="):
                tmp=df.loc[df[op_OBJ[i][0]]==op_OBJ[i][2]]
            else:
                tmp=-1
            return tmp
        except ValueError as e:
            print(e)
            return -1
    else:
        print("columns \033[36m"+op_OBJ[i][0]+"\033[0m is not exist")
        return -1

def mop_changer(df,const,obj_name,value,iu):
    if (len(obj_name)!=len(value)):
        print("Values cannot be matched")
        return False
    for x in obj_name:
        if (x not in const.columns):
            print("Something not in columns")
            return False
    if (iu):
        for x in const.columns.tolist():
            if (const[x][0] in ["Primary Key","Not Null"] and x not in obj_name):
                print("\033[35m"+x+"\033[0m require Value for \033[36m"+const[x][0]+"\033[0m")
                return False
    for i,j in zip(obj_name,range(0,len(value))):
        if (i in const.columns and (const[i][0]=="Primary Key" or const[i][0]=="Unique")):
            if (i in obj_name):
                if (not df.loc[df[i]==value[j]].empty):
                    print("\033[36m"+i+"\033[0m should be \033[34munique\033[0m,you cannot insert \033[33m"+value[j]+"\033[0m into it")
                    return False
    return True

def mop_load(dbname,tname,User=""):
    global writer
    global filer
    (df,const,filer,writer)=TB.connecter(dbname,tname,User)
    return (df,const)

def mop_save(df,dbname,tname):
    df.to_excel(writer,sheet_name=tname,index=0)
    TB.saver(filer,writer,dbname,tname)
    print(df)
    writer.save()

def mop_init(tb0,path0,users):
    global TB
    global PATH
    global Users
    Users=users
    PATH=path0
    TB=tb0
