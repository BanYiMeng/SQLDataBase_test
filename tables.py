import pandas as pd
#import shutil
import os

pd.set_option('display.unicode.ambiguous_as_wide',True)
pd.set_option('display.unicode.east_asian_width',True)
pd.set_option('display.max_columns',None)
pd.set_option('expand_frame_repr',False)
pd.set_option('display.max_rows',None)
pd.set_option('display.width',None)

class ta(object):
    def __init__(self,path):
        self.dbdata=pd.DataFrame()
        self.path=path
        self.tdata=pd.DataFrame()

    def add(self,user,dbname,tname,value):
        if(tname.isdigit()):
            print("\033[35mNameIllegalError: Name cannot be \033[31mpure Numbers\033[0m")
        else:
            self.dbdata=pd.read_csv(self.path+"database.csv")
            if(dbname==tname):
                print("\033[35mNameExistsError: Name exists \033[0m'\033[31m"+tname+"\033[0m'")
            elif(self.dbdata.loc[self.dbdata["name"]==dbname].empty):
                print("\033[35mDBNotFoundError: No such DataBase \033[0m'\033[31m"+dbname+"\033[0m'")
            else:
                if (self.nodigit(value)):
                    (filer,writer)=self.Val_init(dbname)
                    if(self.tdata.loc[self.tdata["name"]==tname].empty):
                        row={"name":tname,"owner":user}
                        self.tdata=self.tdata.append(row,ignore_index=True)
                        self.saver(filer,writer,dbname)
                        print(self.tdata)
                        value.to_csv(self.path+dbname+"/"+tname+"_const.csv",index=0)
                        print(value)
                        value=value.drop([0,1])
                        value.to_excel(writer,sheet_name=tname,index=0)
                        writer.save()
                    else:
                        print("\033[35mTableExistsError: Table exists \033[0m'\033[32m"+tname+"\033[0m'\033[35m"+" in \033[0m[\033[33m"+dbname+"\033[0m]")

    def delete(self,user,dbname,tname):
        if (self.DBFileExist(dbname)):
            (filer,writer)=self.Val_init(dbname)
            if (self.Auth(user,tname)):
                self.tdata=self.tdata.drop(index=(self.tdata.loc[self.tdata["name"]==tname].index))
                os.remove(self.path+dbname+"/"+tname+"_const.csv")
                self.saver(filer,writer,dbname,tname)
                writer.save()
                print (self.tdata)
    
    def alterT(self,user,dbname,tname,value):
        if (self.DBFileExist(dbname)):
            (filer,writer)=self.Val_init(dbname)
            if (self.Auth(user,tname)):
                if (self.nodigit(value)):
                    self.saver(filer,writer,dbname,tname)
                    values=pd.read_csv(self.path+dbname+"/"+tname+"_const.csv")
                    values[value[0]]=["",value[1]]
                    values.to_csv(self.path+dbname+"/"+tname+"_const.csv",index=0)
                    tmp=filer.parse(tname)
                    tmp[value[0]]=None
                    tmp.to_excel(writer,sheet_name=tname,index=0)
                    writer.save()
                    print(values)

    def getDB(self,dbname):
        if (self.DBFileExist(dbname)):
            self.tdata=pd.read_excel(self.path+dbname+"/"+dbname+".xlsx",sheet_name=dbname)
            print(self.tdata)

    def getT(self,dbname,tname):
        if (self.DBFileExist(dbname)):
            self.tdata=pd.read_excel(self.path+dbname+"/"+dbname+".xlsx",sheet_name=dbname)
            if (self.TFileExist(tname)):
                tmp=pd.read_csv(self.path+dbname+"/"+tname+"_const.csv")
                print(tmp)

    def saver(self,filer,writer,dbname,tname=""):
        self.tdata.to_excel(writer,sheet_name=dbname,index=0)
        for i in filer.sheet_names:
            if (i!=dbname and i!=tname):
                filer.parse(i).to_excel(writer,sheet_name=i,index=0)

    def DBFileExist(self,dbname):
        self.dbdata=pd.read_csv(self.path+"database.csv")
        if(self.dbdata.loc[self.dbdata["name"]==dbname].empty):
            print("\033[35mDBNotFoundError: No such DataBase \033[0m'\033[31m"+dbname+"\033[0m'")
            return False
        else:
            return True

    def Auth(self,user,tname):
        if (self.TFileExist(tname)):
            if(user!=self.tdata.loc[self.tdata["name"]==tname].iloc[0,1]):
                print("\033[35mOperation not permitted\033[0m")
                return False
            else:
                return True

    def TFileExist(self,tname):
        if(self.tdata.loc[self.tdata["name"]==tname].empty):
            print("\033[35mTableNotFoundError: No such Table \033[0m'\033[31m"+tname+"\033[0m'")
            return False
        else:
            return True

    def Val_init(self,dbname):
        filer=pd.ExcelFile(self.path+dbname+"/"+dbname+".xlsx")
        self.tdata=filer.parse(dbname)
        return filer,pd.ExcelWriter(self.path+dbname+"/"+dbname+".xlsx")

    def connecter(self,dbname,tname,user=""):
        if (self.DBFileExist(dbname)):
            (filer,writer)=self.Val_init(dbname)
            if (user==""):
                if (not self.TFileExist(tname)):
                    return (-1,-1,-1,-1)
            else:
                if (not self.Auth(user,tname)):
                    return (-1,-1,-1,-1)
            return (filer.parse(tname,dtype=str),pd.read_csv(self.path+dbname+"/"+tname+"_const.csv"),filer,writer)
        return (-1,-1,-1,-1)

    def nodigit(self,value):
        for i in value:
            if (i.isdigit()):
                print("Column name cannot be \033[35mdigit\033[0m")
                return False
        return True
