import pymysql as pm
import prettytable as pt
import time
us=input('enter user id=')
pswd=input('enter password=')
ho=input('enter host=')
data=input('enter database=')
def check_con():
    print('-'*167)
    print("\t\t\t\t\t\t\t\t      CONNECTION CHECKING CONSOLE")
    print()
    con=pm.connect(user=us,password=pswd,host=ho,database=data)
    if con!=None:
        print("\t\t\t\t\t\t\t\t      Connection Established Successfully")
    else:
        print("\t\t\t\t\t\t\t\t      Connection Failed")
    con.close()
#check_con()
#=================================================================
def create_quest():
    try:
        con=pm.connect(user=us,password=pswd,host=ho,database=data)
        cur=con.cursor()
        qry="CREATE TABLE questmst(QID INT(5)PRIMARY KEY,QUEST VARCHAR(50),SUB VARCHAR(20),OP1 VARCHAR(30),OP2 VARCHAR(30),OP3 VARCHAR(30),CORRECT_OP VARCHAR(10));"
        cur.execute(qry)
        print("Table Created Successfully")
    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print('\t\t\t\t\t\t\t\t      Database Error:',e)
    finally:
        if cur:
            cur.close()
        if con:
            con.close()
#create_quest()
#========================================================================
def insert_quest():
    try:
        con=pm.connect(user=us,password=pswd,host=ho,database=data)
        cur=con.cursor()
        u_ich='y'
        while u_ich.lower()=='y':
            print('-'*167)
            print("\t\t\t\t\t\t\t\t      INSERT QUESTION CONSOLE")
            print()
            quest=input("\t\t\t\t\t\t\t\t      Enter Question:")
            sub=input("\t\t\t\t\t\t\t\t      Enter Subject:")
            op1=input("\t\t\t\t\t\t\t\t      Enter Option A:")
            op2=input("\t\t\t\t\t\t\t\t      Enter Option B:")
            op3=input("\t\t\t\t\t\t\t\t      Enter Option C:")
            correct_op=input("\t\t\t\t\t\t\t\t      Enter Correct option[A/B/C]:")
            qry="INSERT INTO questmst VALUES(%s,%s,%s,%s,%s,%s,%s)"
            val=(getmaxid(),quest.upper(),sub.upper(),op1.upper(),op2.upper(),op3.upper(),correct_op.upper())
            cur.execute(qry,val)
            con.commit()
            print()
            print("\t\t\t\t\t\t\t\t      Data inserted successfully")
            print()
            u_ich=input("\t\t\t\t\t\t\t\t      Press Y/y to enter more QUESTIONS:")
            print()
    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print('\t\t\t\t\t\t\t\t      Database Error:',e)
    finally:
        if cur:
            cur.close()
        if con:
            con.close()
#===========================================================
maxid=None
def getmaxid():
    global maxid
    try:
        con=pm.connect(user=us,password=pswd,host=ho,database=data)
        cur=con.cursor()
        qry="SELECT MAX(QID) FROM QUESTMST"
        cur.execute(qry)
        row=cur.fetchone()
        if row[0]!=None:
            maxid=row[0]+1
        else:
            maxid=1
        return maxid
    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print("\t\t\t\t\t\t\t\t      Database error:",e)
    finally:
        if cur:
            cur.close()
        if con:
            con.close()
#print(getmaxid())
#===========================================================
def showall():
    print('-'*167)
    print("\t\t\t\t\t\t\t\t      SHOW TABLE CONSOLE")
    try:
        con=pm.connect(user=us,password=pswd,host=ho,database=data)
        cur=con.cursor()
        qry="SELECT * FROM QUESTMST"
        cur.execute(qry)
        rows=cur.fetchall()
        t=pt.PrettyTable(['QUESTION ID','QUESTION','SUBJECT','OPTION-A','OPTION-B','OPTION-C','CORRECT OPTION'])
        for r in rows:
            t.add_row([r[0],r[1],r[2],r[3],r[4],r[5],r[6]])
        enter=input("\t\t\t\t\t\t\t\t      PRESS ENTER TO VIEW FULL TABLE:")
        print(t)
    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print('\t\t\t\t\t\t\t\t      Database Error:',e)
    finally:
        if cur:
            cur.close()
        if con:
            con.close()
#showall()
#=========================================================
def search_quest(subj):
    try:
        con=pm.connect(user=us,password=pswd,host=ho,database=data)
        cur=con.cursor()
        qry="SELECT * FROM QUESTMST WHERE SUB=%s;"
        val=(subj,)
        cur.execute(qry,val)
        rows=cur.fetchall()
        t=pt.PrettyTable(['QUESTION ID','QUESTION','SUBJECT','OPTION-A','OPTION-B','OPTION-C','CORRECT OPTION'])
        if rows:
            for r in rows:
                t.add_row([r[0],r[1],r[2],r[3],r[4],r[5],r[6]])
            print(t)
        else:
            print("\t\t\t\t\t\t\t\t      Invalid Subject")
    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print('\t\t\t\t\t\t\t\t      Database Error:',e)
    finally:
        if cur:
            cur.close()
        if con:
            con.close()
#==============================================================
def isqidvalid(u_qid):
    try:
        con=pm.connect(user=us,password=pswd,host=ho,database=data)
        cur=con.cursor()
        qry="SELECT QID FROM QUESTMST WHERE QID=%s"
        val=(u_qid,)
        cur.execute(qry,val)
        row=cur.fetchone()
        if row:
            return True
        else:
            return False
    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print('Database Error:',e)
    finally:
        if cur:
            cur.close()
        if con:
            con.close()
#===================================================================
def update_quest(u_qid):
    try:
        con=pm.connect(user=us,password=pswd,host=ho,database=data)
        cur=con.cursor()
        valid=isqidvalid(u_qid)
        if valid:
            n_quest=input("\t\t\t\t\t\t\t\t      Enter New Question:")
            n_sub=input("\t\t\t\t\t\t\t\t      Enter New Subject::")
            n_op1=input("\t\t\t\t\t\t\t\t      Enter New Option A:")
            n_op2=input("\t\t\t\t\t\t\t\t      Enter New Option B:")
            n_op3=input("\t\t\t\t\t\t\t\t      Enter New Option C:")
            n_correct_op=input("\t\t\t\t\t\t\t\t      Enter New Correct option[A/B/C]:")
            qry="UPDATE QUESTMST SET QUEST=%s,SUB=%s,OP1=%s,OP2=%s,OP3=%s,CORRECT_OP=%s WHERE QID=%s"
            val=(n_quest.upper(),n_sub.upper(),n_op1.upper(),n_op2.upper(),n_op3.upper(),n_correct_op.upper(),u_qid)
            cur.execute(qry,val)
            con.commit()
            print()
            print("\t\t\t\t\t\t\t\t      Data updated successfully")
        elif valid==False:
            print("\t\t\t\t\t\t\t\t      Invalid QID")
    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print('\t\t\t\t\t\t\t\t      Database Error:',e)
    finally:
        if cur:
            cur.close()
        if con:
            con.close()
#=======================================================
def delete_quest(u_qid):
    try:
        con=pm.connect(user=us,password=pswd,host=ho,database=data)
        cur=con.cursor()
        valid=isqidvalid(u_qid)
        if valid:
            qry="DELETE FROM QUESTMST WHERE QID=%s"
            val=(u_qid,)
            cur.execute(qry,val)
            con.commit()
            print()
            print("\t\t\t\t\t\t\t\t      Data Deleted successfully")
        elif valid==False:
            print("\t\t\t\t\t\t\t\t      Invalid QID")
    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print('\t\t\t\t\t\t\t\t      Database Error:',e)
    finally:
        if cur:
            cur.close()
        if con:
            con.close()
#========================================================
def valid_subject():
    try:
        con=pm.connect(user=us,password=pswd,host=ho,database=data)
        cur=con.cursor()
        qry="SELECT DISTINCT SUB FROM QUESTMST"
        cur.execute(qry)
        rows=cur.fetchall()
        t=pt.PrettyTable(['VALID SUBJECT'])
        for r in rows:
            t.add_row([r[0]])
        print(t)
    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print('\t\t\t\t\t\t\t\t      Database Error:',e)
    finally:
        if cur:
            cur.close()
        if con:
            con.close()
#========================================================
def valid_qid():
    try:
        con=pm.connect(user=us,password=pswd,host=ho,database=data)
        cur=con.cursor()
        qry="SELECT QID,QUEST FROM QUESTMST"
        cur.execute(qry)
        rows=cur.fetchall()
        t=pt.PrettyTable(['VALID QIDs','QUESTION'])
        for r in rows:
            t.add_row([r[0],r[1]])
        print(t)
    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print('\t\t\t\t\t\t\t\t      Database Error:',e)
    finally:
        if cur:
            cur.close()
        if con:
            con.close()
    
    









#=================driver code==============================
print('-'*167)#length of screen is 167 times a char
print("\t\t\t\t\t\t\t\tWELCOME TO MOCK TEST SOFTWARE")#7 tabs for text in middle
print('-'*167)
while(1):
    print("\t\t\t\t\t\t\t\t-:MAIN SECTION:-")
    print("\t\t\t\t\t\t\t\t1.ADMIN SECTION")
    print("\t\t\t\t\t\t\t\t2.PLAY")
    print("\t\t\t\t\t\t\t\t3.SCOREBOARD")
    print("\t\t\t\t\t\t\t\t4.EXIT")
    ch=int(input("\t\t\t\t\t\t\t\tPlease input your choice[1-4]:"))
    print('-'*167)
    if ch==1:
        print("\t\t\t\t\t\t\t\tWELCOME TO ADMIN PORTAL")
        pswd=input("\t\t\t\t\t\t\t\tPLESE ENTER LOGIN PASSWORD:")
        if pswd=='1234':
            while(1):
                print('-'*167)
                
                print("\t\t\t\t\t\t\t\t    ADMIN PORTAL")
                print("\t\t\t\t\t\t\t\t      A).CHECK CONNECTION")
                print("\t\t\t\t\t\t\t\t      B).ADD QUESTION")
                print("\t\t\t\t\t\t\t\t      C).SHOW ALL QUESTIONS")
                print("\t\t\t\t\t\t\t\t      D).UPDATE QUESTION")
                print("\t\t\t\t\t\t\t\t      E).SEARCH QUESTION")
                print("\t\t\t\t\t\t\t\t      F).DELETE QUESTION")
                print("\t\t\t\t\t\t\t\t      G).EXIT TO MAIN SECTION")
                a_ch=input("\t\t\t\t\t\t\t         Plese enter your choice[A/B/C/D/E/F]:")
                if a_ch.lower()=="a":
                    check_con()
                elif a_ch.lower()=="b":
                    insert_quest()
                elif a_ch.lower()=="c":
                    showall()
                elif a_ch.lower()=="d":
                    print('-'*167)
                    print("UPDATE TABLE CONSOLE")
                    valid_qid()
                    u_qid=int(input("\t\t\t\t\t\t\t\t      Enter QID:"))
                    update_quest(u_qid)
                elif a_ch.lower()=="e":
                    print('-'*167)
                    print("\t\t\t\t\t\t\t\t      SEARCH TABLE CONSOLE")
                    valid_subject()
                    print()
                    subj=input("\t\t\t\t\t\t\t\t      Enter Subject to search:")
                    search_quest(subj)
                elif a_ch.lower()=="f":
                    print('-'*167)
                    print("\t\t\t\t\t\t\t\t      DELETE TABLE CONSOLE")
                    valid_qid()
                    print()
                    u_qid=int(input("\t\t\t\t\t\t\t\t      Enter QID:"))
                    delete_quest(u_qid)
                elif a_ch.lower()=="g":
                    print('-'*167)
                    print("\t\t\t\t\t\t\t\tGoing to Main Section.................")
                    print('-'*167)
                    break
                else:
                    print("\t\t\t\t\t\t\t\tINVALID CHOICE!!")
        else:
            print()
            print()
            print("\t\t\t\t\t\t\t\tWRONG PASSWORD!!")
            print('-'*167)

    elif ch==2:
        print('\t\t\t\t\t\t\t\tPLAY SECTION')
    elif ch==3:
        print("\t\t\t\t\t\t\t\tSCOREBOARD SECTION")
    elif ch==4:
        time.sleep(0.5)
        print("\t\t\t\t\t\t\t\tExiting",end="")
        for i in range(10):
            print(".",end="")
            time.sleep(0.1)
        break
    else:
        print("\t\t\t\t\t\t\t\tInvalid choice")
        print('-'*167)