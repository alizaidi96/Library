import os
import time
import sys
from datetime import datetime
import cx_Oracle


con = cx_Oracle.connect("system/password@localhost/xe")
cur = con.cursor()


class Book():
    def __init__(self,title,author,publication,pub_year,bookid,current_status,deleted):
        self.title = title
        self.author = author
        self.publication = publication
        self.pub_year = pub_year
        self.bookid = bookid
        self.current_status = current_status
        self.deleted = deleted
        
    def add_book_to_db(self):
        cur.execute("""insert into Book values (:1,:2,:3,:4,:5,:6,:7)""",{'1':self.title,'2':self.author,'3':self.publication,'4':self.pub_year,'5':self.bookid,'6':self.current_status,'7':self.deleted})
        con.commit()
        
        
class Member():
    def __init__(self,user_id,name,phone_no,fine,deleted,password):
        self.user_id = user_id
        self.name = name
        self.phone_no = phone_no
        self.fine = fine
        self.deleted = deleted
        self.password = password
        
        
    def add_member_to_db(self):
        cur.execute("""insert into Member values (:1,:2,:3,:4,:5,:6)""",{'1':self.user_id,'2':self.name,'3':self.phone_no,'4':self.fine,'5':self.deleted,'6':self.password})
        con.commit()
 
        
class Issue_history():
    def __init__(self,user_id,bookid,issue_date,return_date,issue_id,deleted):
        self.user_id = user_id 
        self.bookid = bookid
        self.issue_date = issue_date    
        self.return_date = return_date
        self.issue_id = issue_id
        self.deleted = deleted
        
    def add_issue_to_db(self):
        cur.execute("""alter session set nls_date_format = 'DD/MM/YYYY'""")
        cur.execute("""insert into Issue_history values (:1,:2,:3,:4,:5,:6)""",{'1':self.user_id,'2':self.bookid,'3':self.issue_date,'4':self.return_date,'5':self.issue_id,'6':self.deleted})
        con.commit()


class Lib_admin():
    def __init__(self,aid,password):
        self.aid = aid
        self.password = password
        
        


def home():
    c = 0
    os.system('CLS')
    while(c != 4):
        print("WELCOME TO PYTHON LIBRARY MANAGEMENT SYSTEM")
        print("1. LOGIN")
        print("2. SIGNUP")
        print("3. ADMIN")
        print("4. EXIT")
        c = int(input("\nEnter your choice (1 - 4): "))        
        if c == 1:
            os.system('CLS')
            login()
        elif c == 2:
            os.system('CLS')
            add_member()
        elif c == 3:
            os.system('CLS')
            admin_login()
        elif c == 4:
            sys.exit()
        else:
            print("\nInvalid choice entered.")
            time.sleep(2)
            os.system('CLS')
            
            
def login():
    uid = input("USER ID: ")
    password = input("PASSWORD: ")
    cur.execute("""select * from Member where user_id = :1 and password = :2""",(uid,password))
    res = cur.fetchall()
    if len(res) != 0:
        print("\nLogin Successful. Redirecting shortly...")
        time.sleep(3)
        user_menu()
    else:
        print("\nWrong User Name or Password entered. Redirecting back...")
        time.sleep(3)
        home()
  
        
def add_member():
    user_id = input("Enter a user ID: ")
    cur.execute("""select * from Member where user_id = :1 and deleted = 'N'""",(user_id,))
    res = cur.fetchall()
    if len(res) == 0:
        password = input("Enter a password: ")
        member_name = input("Enter the name: ")
        member_phone_no = input("Enter the phone number: ")
        m = Member(user_id,member_name,member_phone_no,0,'N',password)
        m.add_member_to_db()
        print("\nMember has been added successful. Login now from Main Menu. Redirecting shortly...")
        time.sleep(3)
        home()
    else:
        print("\nUser ID already exists. Try another User ID. Redirecting back...")
        time.sleep(3)
        home()


def admin_login():
    aid = input("ADMIN ID: ")
    password = input("PASSWORD: ")
    cur.execute("""select * from Lib_admin where aid = :1 and password = :2""",(aid,password))
    res = cur.fetchall()
    if len(res) != 0:
        print("\nLogin successful. Redirecting shortly...")
        time.sleep(3)
        admin_menu()
    else:
        print("\nWrong Admin ID or Password entered. Redirecting back shortly...")
        time.sleep(3)
        home()
        

        
def user_menu():
    c = 0
    os.system('CLS')
    while(c != 6):
        print("WELCOME MEMBER")
        print("1. SEARCH FOR A BOOK")
        print("2. ISSUE A BOOK")
        print("3. RETURN A BOOK")
        print("4. CHECK FINE")
        print("5. CHECK ISSUE HISTORY")
        print("6. EXIT")
        c = int(input("\nEnter your choice (1-6): "))
        if c == 1:
            os.system('CLS')
            search_book()
        elif c == 2:
            os.system('CLS')
            issue_book()
        elif c == 3:
            os.system('CLS')
            return_book()
        elif c == 4:
            os.system('CLS')
            check_fine()
        elif c == 5:
            os.system('CLS')
            check_issue()
        elif c == 6:
            home()
        else:
            print("\nInvalid choice made.")
            time.sleep(2)
            os.system('CLS')
            
            
def search_book():
    bname = input("Enter the name of the book to be searched: ")
    cur.execute("""select title from Book where deleted = 'N'""")
    res = cur.fetchall()
    res2 = [x for t in res for x in t]
    if bname in res2:
        cur.execute("""select * from Book where title = :1 and deleted = 'N'""",(bname,))
        res3 = cur.fetchall()
        res4 = [x for t in res3 for x in t]
        print("\nNAME:",res4[0])
        print("AUTHOR:",res4[1])
        print("PUBLICATION:",res4[2])
        print("YEAR PUBLISHED:",res4[3])
        print("BOOK ID:",res4[4])
        print("STATUS:",res4[5])
        a = int(input("\nEnter 0 to go back to the Main Menu"))
        if a == 0:
            user_menu()
        else:
            user_menu()
    else:
        print("\nSorry. This book is not present in the library. Redirecting back...")
        time.sleep(3)
        user_menu()
            
        
def issue_book():
    bid = int(input("Enter the book ID to be issued: "))
    cur.execute("""select bookid from Book where deleted = 'N'""")
    res = cur.fetchall()
    res2 = [x for t in res for x in t]
    if bid in res2:
        uid = input("Enter the ID of the member: ")
        cur.execute("""select user_id from Member where deleted = 'N'""")
        res3 = cur.fetchall()
        res4 = [x for t in res3 for x in t]
        if uid in res4:
            idate = input("Enter the issue date (dd/mm/yyyy): ")
            issue_date = datetime.strptime(idate, "%d/%m/%Y")
            rdate = input("Enter the return date (dd/mm/yyyy): ")
            return_date = datetime.strptime(rdate, "%d/%m/%Y")
            if issue_date > return_date:
                print ("\nIssuing date cannot be after return date.")
                time.sleep(3)
                user_menu()
            else:
                iid = str(bid) + uid
                issue = Issue_history(uid,bid,idate,rdate,iid,'N')
                issue.add_issue_to_db()
                cur.execute("""update Book set current_status = 'Issued' where bookid = :1""",(bid,))
                con.commit()
                print("\nYour issue has been made. Your return date is:",return_date.date())
                print("Your Issue ID is", iid)
                print("Remember your Issue ID for returning the book.")
                time.sleep(3)
                user_menu()
        else:
            print("\nWrong Member ID entered. Redirecting back...")
            time.sleep(3)
            user_menu()
    else:
        print("\nWrong Book ID entered. Redirecting back...")
        time.sleep(3)
        user_menu()
    
    
def return_book():
    iid = input("Enter the Issue ID given: ")
    cur.execute("""select issue_id from Issue_history where deleted = 'N'""")
    res = cur.fetchall()
    res2 = [x for t in res for x in t]
    if iid in res2:
        bid = int(input("Enter the Book ID: "))
        uid = input("Enter the member ID: ")
        cur.execute("""select return_date from Issue_history where issue_id = :1""",(iid,))
        res3 = cur.fetchall()
        res4 = [x for t in res3 for x in t]
        x = res4[0].date()
        y = (datetime.today()).date()
        if (x == y or x > y):
            cur.execute("""update Book set current_status = 'Available' where bookid = :1""",(bid,))
            con.commit()
            cur.execute("""update Issue_history set deleted = 'Y' where issue_id = :1""",(iid,))
            con.commit()
            print("\nBook returned successfully. Redirecting back...")
            time.sleep(3)
            user_menu()
        else:
            fd = (y-x).days
            fine = 5 * fd
            print("\nYour fine is Rs.",fine)
            cur.execute("""update Book set current_status = 'Available' where bookid = :1""",(bid,))
            con.commit()
            cur.execute("""update Issue_history set deleted = 'Y' where issue_id = :1""",(iid,))
            con.commit()
            cur.execute("""update Member set fine = :1 where user_id = :2""",(fine,uid))
            con.commit()
            print("\nBook returned successfully. Redirecting back...")
            time.sleep(3)
            user_menu()
    else:
        print("\nIssue ID does not exist. Make sure you are entering the correct Issue ID. Redirecting back...")
        time.sleep(3)
        user_menu()

    
def check_fine():
    uid = input("Enter the user ID: ")
    cur.execute("""select user_id from Member where deleted = 'N'""")
    res = cur.fetchall()
    res2 = [x for t in res for x in t]
    if uid in res2:
        cur.execute("""select fine from Member where user_id = :1""",(uid,))
        res3 = cur.fetchall()
        res4 = [x for t in res3 for x in t]
        print("\nYour fine is Rs.",res4[0])
        print("Kindly deposit your fine ASAP.")
        print("Redirecting back...")
        time.sleep(3)
        user_menu()
    else:
        print("\nWrong user ID entered. Check the user ID. Redirecting back...")
        time.sleep(3)
        user_menu()
        
        
def check_issue():
    uid = input("Enter the user ID: ")
    cur.execute("""select user_id from Member where deleted = 'N'""")
    res = cur.fetchall()
    res2 = [x for t in res for x in t]
    if uid in res2:
        cur.execute("""select * from Issue_history where user_id = :1""",(uid,))
        res3 = cur.fetchall()
        for x in res3:
            print("\n",x)
        a = int(input("\nEnter 0 to go back to menu. "))
        if a == 0:
            print("Redirecting back...")
            time.sleep(2)
            user_menu()
        else:
            user_menu()
    else:
        print("Wrong user ID entered. Check the user ID. Redirecting back...")
        time.sleep(3)
        user_menu()
        


def admin_menu():
    c = 0
    os.system('CLS')
    while(c != 5):
        print("WELCOME ADMIN")
        print("1. ADD A BOOK IN LIBRARY")
        print("2. REMOVE A BOOK FROM LIBRARY")
        print("3. REMOVE A MEMBER")
        print("4. SEARCH FOR A BOOK")
        print("5. EXIT")
        c = int(input("\nEnter your choice (1-5): "))
        if c == 1:
            os.system('CLS')
            add_book()
        elif c == 2:
            os.system('CLS')
            remove_book()
        elif c == 3:
            os.system('CLS')
            remove_user()
        elif c == 4:
            os.system('CLS')
            search_book_admin()
        elif c == 5:
            home()
        else:
            print("\nInvalid choice made.")
            time.sleep(2)
            os.system('CLS')
    
   
def add_book():
    book_id = int(input("Enter the ID of book: "))
    cur.execute("""select * from Book where bookid = :1 and deleted = 'N'""",(book_id,))
    res = cur.fetchall()
    if len(res) == 0:
        book_title = input("Enter the book title: ")
        book_author = input("Enter the book author: ")
        book_publication = input("Enter the book publication: ")
        book_pub_year = int(input("Enter the year of publication of book: "))        
        b = Book(book_title,book_author,book_publication,book_pub_year,book_id,'Available','N')
        b.add_book_to_db()
        print("\nBook has been added to the library. Redirecting back...")
        time.sleep(3)
        admin_menu()
    else:
        print("\nThis book ID already exists. Please use a new ID. Redirecting back...")
        time.sleep(3)
        admin_menu()


def remove_book():
    bid = int(input("Enter the book ID to be removed: "))
    cur.execute("""select bookid from Book where deleted = 'N'""")
    res = cur.fetchall()
    res2 = [x for t in res for x in t]
    if bid in res2:
        cur.execute("""update Book set deleted = 'Y' where bookid = :1""",(bid,))
        con.commit()
        print("\nBook has been removed. Redirecting back...")
        time.sleep(3)
        admin_menu()
    else:
        print("\nWrong book ID entered. Check the book ID. Redirecting back...")
        time.sleep(3)
        admin_menu()
    
    
def remove_user():
    uid = input("Enter the user ID to be removed: ")
    cur.execute("""select user_id from Member where deleted = 'N'""")
    res = cur.fetchall()
    res2 = [x for t in res for x in t]
    if uid in res2:
        cur.execute("""update Member set deleted = 'Y' where user_id = :1""",(uid,))
        con.commit()
        print("\nMember has been removed. Redirecting back...")
        time.sleep(3)
        admin_menu()
    else:
        print("\nWrong user ID entered. Check the user ID. Redirecting back...")
        time.sleep(3)
        admin_menu()
        
        
def search_book_admin():
    bname = input("Enter the name of the book to be searched: ")
    cur.execute("""select title from Book where deleted = 'N'""")
    res = cur.fetchall()
    res2 = [x for t in res for x in t]
    if bname in res2:
        cur.execute("""select * from Book where title = :1 and deleted = 'N'""",(bname,))
        res3 = cur.fetchall()
        res4 = [x for t in res3 for x in t]
        print("\nNAME:",res4[0])
        print("AUTHOR:",res4[1])
        print("PUBLICATION:",res4[2])
        print("YEAR PUBLISHED:",res4[3])
        print("BOOK ID:",res4[4])
        print("STATUS:",res4[5])
        a = int(input("\nEnter 0 to go back to the Main Menu"))
        if a == 0:
            admin_menu()
        else:
            admin_menu()
    else:
        print("\nSorry. This book is not present in the library. Redirecting back...")
        time.sleep(3)
        admin_menu()
    
    
    

####Execution will start from here####

home()
con.close()


