import readline
import pandas as pd
import logins
import ops

DBName=""
sqls=""

def init_sql2op(DB0,TB0,Name):
    global DB
    DB=DB0
    global TB
    TB=TB0
    global User_Name
    User_Name=Name

def getsql():
    global sqls
    while (1):
        sqls+=" "+input("\033[32m>>\033[0m")
        if (sqls[len(sqls)-1]==";"):
            if (preprocessor()==True):
                sqls=""
                continue
            if (l1decode()==True):
                sqls=""
                return
            sqls=""

def preprocessor():
    global sqls
    for i in "0123456789":
        sqls=sqls.replace("("+i,"["+i)
        sqls=sqls.replace(i+")",i+"]")
    sqls=sqls.title().replace("="," = ").replace("<>"," != ").replace(">"," > ").replace("<"," < ").replace("! ="," !=").replace("<  =","<=").replace(">  =",">=").replace("! >"," <=").replace("! <"," >=").replace("("," ( ").replace(")"," ) ").replace(","," , ").replace("'"," ").replace("\""," ").replace(";"," ").split()
    if (len(sqls)==0):
        return True

def Where_decode(i):
    op_OBJ=[]
    op_B=[]
    if (len(sqls)==i):
        return op_OBJ,op_B
    elif (sqls[i]!="Where"):
        ErrorReporter(i-1)
        return False,False
    i+=1
    while (i<len(sqls)):
        if (i+3>len(sqls)):
            ErrorReporter(i)
            return False,False
        if (sqls[i+1] in ["!=",">=","<=","<",">","="]):
            op_OBJ.append([sqls[i],sqls[i+1],sqls[i+2]])
            i+=3
        elif (sqls[i+1]=="Not" and sqls[i+2]=="Between" and sqls[i+4]=="And"):
            op_OBJ.append([sqls[i],"<",sqls[i+3]])
            op_B.append("Or")
            op_OBJ.append([sqls[i],">",sqls[i+5]])
            i+=6
        elif (sqls[i+1]=="Between" and sqls[i+3]=="And"):
            op_OBJ.append([sqls[i],">=",sqls[i+2]])
            op_B.append("And")
            op_OBJ.append([sqls[i],"<=",sqls[i+4]])
            i+=5
        elif (sqls[i+1]=="Not" and sqls[i+2]=="In" and sqls[i+3]=="("):
            tmp=sqls[i]
            i+=4
            while (sqls[i]!=")"):
                op_OBJ.append([tmp,"!=",sqls[i]])
                op_B.append("And")
                if (sqls[i+1]==")"):
                    i+=1
                elif (sqls[i+1]==","):
                    i+=2
                else:
                    ErrorReporter(i)
                    return False,False
            i+=1
        elif (sqls[i+1]=="In" and sqls[i+2]=="("):
            tmp=sqls[i]
            i+=3
            while (sqls[i]!=")"):
                op_OBJ.append([tmp,"=",sqls[i]])
                op_B.append("Or")
                if (sqls[i+1]==")"):
                    i+=1
                elif (sqls[i+1]==","):
                    i+=2
                else:
                    ErrorReporter(i)
                    return False,False
            i+=1
        else:
            ErrorReporter(i+1)
            return False,False
        if (i<len(sqls)):
            if (sqls[i]=="And" or sqls[i]=="Or"):
                op_B.append(sqls[i])
                i+=1
            else:
                ErrorReporter(i)
                return False,False
    return op_OBJ,op_B

def Use_decode():
    global DBName
    DBName=sqls[1]
    print("\033[34mDBName\033[0m=\033[32m"+DBName+"\033[0m")

def CREATEandDROP_decode(CorD):
    t_name=sqls[2]
    i=3
    if (CorD==True):
        if (sqls[1]=="Table"):
            if (sqls[i]!="("):
                ErrorReporter(i)
                return
            i+=1
            value=pd.DataFrame()
            if (sqls[len(sqls)-1]!=")"):
                ErrorReporter(len(sqls)-1)
                return
            while(sqls[i]!=")"):
                const=""
                name=sqls[i]
                i+=1
                types=sqls[i]
                i+=1
                if (sqls[i]!="," and sqls[i]!=")"):
                    if (sqls[i]=="Primary" or sqls[i]=="Not" or sqls[i]=="Foreign"):
                        const=sqls[i]+" "+sqls[i+1]
                        i+=1
                    else:
                        if (types=="Primary" or types=="Not" or types=="Foreign"):
                            ErrorReporter(i-1)
                            return
                        const=sqls[i]
                    i+=1
                    if (sqls[i]!="," and sqls[i]!=")"):
                        ErrorReporter(i-1)
                        return
                    elif (sqls[i]==")"):
                        i-=1
                elif (sqls[i]==")"):
                    i-=1
                elif (sqls[i]==","):
                    if (types=="Null" or types=="Unique" or types=="Check"):
                        ErrorReporter(i-1)
                        return
                i+=1
                if(const=="Primary Key"):
                    value.insert(0,name,[const,types])
                else:
                    value[name]=[const,types]
            if (DBName==""):
                print("\033[31mDatabase not specified\033[0m")
                return
            TB.add(User_Name,DBName,t_name,value)
        elif (sqls[1]=="Database"):
            DB.add(User_Name,t_name,"Reserved")
        else:
            ErrorReporter(1)
    elif (CorD==False):
        if (sqls[1]=="Table"):
            if (DBName==""):
                print("\033[31mDatabase not specified\033[0m")
                return
            TB.delete(User_Name,DBName,t_name)
        elif (sqls[1]=="Database"):
            DB.delete(User_Name,t_name)
        else:
            ErrorReporter(1)

def Alter_decode():
    if (DBName==""):
        print("\033[31mDatabase not specified\033[0m")
        return
    name=sqls[2]
    if (sqls[3]!="Add"):
        ErrorReporter(3)
        return
    value=[sqls[4],sqls[5]]
    TB.alterT(User_Name,DBName,name,value)

def SELECTandDelete_decode(SorD):
    if (DBName==""):
        print("\033[31mDatabase not specified\033[0m")
        return
    i=1
    if (SorD):
        value=[]
        while(sqls[i]!="From"):
            value.append(sqls[i])
            i+=1
            if (sqls[i]==","):
                i+=1
        i+=1
        name=sqls[i]
        i+=1
    else:
        name=sqls[2]
        i=3
        value=None
    (op_OBJ,op_B)=Where_decode(i)
    if (op_OBJ==op_B==False):
        return
    if (SorD):
        ops.op_Select(DBName,name,value,op_OBJ,op_B)
    else:
        ops.op_Delete(DBName,name,op_OBJ,op_B)

def Insert_decode():
    if (DBName==""):
        print("\033[31mDatabase not specified\033[0m")
        return
    if (sqls[1]!="Into"):
        ErrorReporter(1)
        return
    name=sqls[2]
    i=3
    obj_name=[]
    if (sqls[i]=="("):
        i+=1
        while(sqls[i]!=")"):
            obj_name.append(sqls[i])
            i+=1
            if (sqls[i]==","):
                i+=1
        i+=1
    elif (sqls[i]!="Values"):
        ErrorReporter(i)
        return
    i+=1
    if (sqls[i]!="(" or sqls[len(sqls)-1]!=")"):
        ErrorReporter(i)
        return
    else:
        i+=1
    value=[]
    while (sqls[i]!=")"):
        value.append(sqls[i])
        i+=1
        if (sqls[i]==","):
            i+=1
    ops.op_Insert(DBName,name,obj_name,value)

def Update_decode():
    if (DBName==""):
        print("\033[31mDatabase not specified\033[0m")
        return
    name=sqls[1]
    if (sqls[2]!="Set"):
        ErrorReporter(2)
        return
    i=3
    value=[]
    while (i<len(sqls) and sqls[i]!="Where"):
        if (sqls[i+1]!="="):
            ErrorReporter(i)
            return
        value.append([sqls[i],sqls[i+2]])
        i+=3
        if (sqls[i]==","):
            i+=1
    (op_OBJ,op_B)=Where_decode(i)
    if (op_OBJ==op_B==False):
        return
    ops.op_Update(DBName,name,value,op_OBJ,op_B)

def Help_decode():
    if (len(sqls)==3):
        if (sqls[1]=="Database"):
            TB.getDB(sqls[2])
        elif (sqls[1]=="Table"):
            if (DBName==""):
                print("\033[31mDatabase not specified\033[0m")
            else:
                TB.getT(DBName,sqls[2])
        else:
            ErrorReporter(1)
    elif (len(sqls)==2):
        if (sqls[1]=="System"):
            DB.get()
        else:
            ErrorReporter(1)
    else:
        ErrorReporter(0)

def User_decode():
    if (sqls[1]=="Add"):
        logins.addUser()
    elif (sqls[1]=="Delete"):
        return logins.deleteAccount(User_Name)
    elif (sqls[1]=="Password"):
        return logins.changePwd(User_Name)
    elif (sqls[1]=="Logout"):
        print("\033[4mLogout\033[0m")
        return True
    else:
        ErrorReporter(1)

def l1decode():
    try:
        if (sqls[0]=="Use"):
            Use_decode()
        elif (sqls[0]=="Create"):
            CREATEandDROP_decode(True)
        elif (sqls[0]=="Drop"):
            CREATEandDROP_decode(False)
        elif (sqls[0]=="Alter"):
            Alter_decode()
        elif (sqls[0]=="Select"):
            SELECTandDelete_decode(True)
        elif (sqls[0]=="Delete"):
            SELECTandDelete_decode(False)
        elif (sqls[0]=="Insert"):
            Insert_decode()
        elif (sqls[0]=="Update"):
            Update_decode()
        elif (sqls[0]=="Help"):
            Help_decode()
        elif (sqls[0]=="User"):
            return User_decode()
        elif (sqls[0]=="Exit"):
            exit()
        else:
            ErrorReporter(0)
    except IndexError:
        ErrorReporter(len(sqls)-1)

def ErrorReporter(i):
    for x in range(i):
        print(sqls[x]+" ",end="")
    print("\033[4;31m"+sqls[i]+"\033[0m",end="")
    for x in range(i+1,len(sqls)):
        print(" "+sqls[x],end="")
    print("\033[0m;")
