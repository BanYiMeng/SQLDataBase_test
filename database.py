import pandas as pd
import os
import shutil

pd.set_option('display.unicode.ambiguous_as_wide',True)
pd.set_option('display.unicode.east_asian_width',True)
pd.set_option('display.max_columns',None)
pd.set_option('expand_frame_repr',False)
pd.set_option('display.max_rows',None)
pd.set_option('display.width',None)

class db(object):
    def __init__(self,path):
        if (not os.path.exists(path+"database.csv")):
            fd = open(path+"database.csv",mode="w")
            fd.write("name,owner,value")
            fd.close()
        self.dbdata=pd.read_csv(path+"database.csv")
        self.path=path

    def add(self,user,name,value):
        if(name.isdigit()):
            print("\033[35mNameIllegalError: Name cannot be \033[31mpure Numbers\033[0m")
        elif (name=="Database"):
            print("\033[35mNameIllegalError: Name cannot be \033[0m'\033[31mdatabase\033[0m'")
        else:
            if(self.dbdata.loc[self.dbdata["name"]==name].empty):
                row={"name":name,"owner":user,"value":value}
                self.dbdata=self.dbdata.append(row,ignore_index=True)
                tmp=pd.DataFrame(columns=["name","owner"])
                os.mkdir(self.path+name)
                tmp.to_excel(self.path+name+"/"+name+".xlsx",sheet_name=name,index=0)
                self.dbdata.to_csv(self.path+"database.csv",index=0)
                print (self.dbdata)
            else:
                print("\033[35mDBExistsError: DataBase exists \033[0m'\033[31m"+name+"\033[0m'")

    def get(self):
        print(self.dbdata)

    def delete(self,user,name):
        if(self.dbdata.loc[self.dbdata["name"]==name].empty):
            print("\033[35mDBNotFoundError: No such DataBase \033[0m'\033[31m"+name+"\033[0m'")
        elif(user!=self.dbdata.loc[self.dbdata["name"]==name].iloc[0,1]):
            print("\033[35mOperation not permitted\033[0m")
        else:
            self.dbdata=self.dbdata.drop(index=(self.dbdata.loc[self.dbdata["name"]==name].index))
            shutil.rmtree(self.path+name)
            self.dbdata.to_csv(self.path+"database.csv",index=0)
            print (self.dbdata)
