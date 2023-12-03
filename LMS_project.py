import os
import csv
from datetime import datetime, timedelta

user_credentials = {'admin': '1234'}

def handle_login():
    print("1. Login")
    print("2. Change Password")

    choice = 0
    while choice != 1 and choice != 2:
        choice = int(input("Enter your choice: "))

        if choice == 1:
            username = input("Enter Username: ")
            password = input("Enter Password: ")

            if username in user_credentials and user_credentials[username] == password:
                dashboard()
            else:
                print('Error', 'Invalid username or password')
        elif choice == 2:
            change_password()
        else:
            print("Invalid choice")

def change_password():
    username = input("Enter username: ")
    old_password = input("Enter old password: ")

    if username in user_credentials and user_credentials[username] == old_password:
        new_password = input("Enter new password: ")
        user_credentials[username] = new_password  
        print("Password changed successfully!")
        handle_login()
    else:
        print("Incorrect old password or username")

def addBook():
    print("Add a new Book Record")
    print("=====================")
    f=open('library.csv','a',newline='\r\n')
    s=csv.writer(f)
    bookid=int(input('Enter book id='))
    bookname=input('Enter book name=')
    bookauthor=input('Enter author name=')
    rec=[bookid,bookname,bookauthor]
    s.writerow(rec)
    f.close()
    print("Book Record Saved")
    input("Press any key to continue..")

def editBook():
    print("Modify a Book Record")
    print("====================")
    f=open('library.csv','r',newline='\r\n') 
    f1=open('temp.csv','w',newline='\r\n')
    f1=open('temp.csv','a',newline='\r\n')
    r=input('Enter bookid whose record you want to modify=')
    s=csv.reader(f)
    s1=csv.writer(f1)
    for rec in s:
        if rec[0]==r:
            print("-------------------------------")
            print("Book id=",rec[0])
            print("Book Name=",rec[1])
            print("Author=",rec[2])
            print("-------------------------------")
            
            choice=input("Do you want to modify this Book Record(y/n)=")
            if choice=='y' or choice=='Y':
                bookid=int(input('Enter new book id='))
                bookname=input('Enter new book name=')
                bookauthor=input('Enter new author name=')
                rec=[bookid,bookname,bookauthor]
                s1.writerow(rec)
                print("Book Record Modified")
            else:
                s1.writerow(rec)
        else:
            s1.writerow(rec)
    f.close()   
    f1.close()
    os.remove("library.csv")
    os.rename("temp.csv","library.csv")
    
    input("Press any key to continue..")

def deleteBook():
    f=open('library.csv','r',newline='\r\n') 
    f1=open('temp.csv','w',newline='\r\n')
    f1=open('temp.csv','a',newline='\r\n')
    r=input('Enter bookid whose record you want to delete')
    s=csv.reader(f)
    s1=csv.writer(f1)
    for rec in s:
        if rec[0]==r:
            print("-------------------------------")
            print("Book id=",rec[0])
            print("Book Name=",rec[1])
            print("Author=",rec[2])
            print("-------------------------------")
            choice=input("Do you want to delete this Book Record(y/n)")
            if choice=='y' or choice=='Y':
                pass
                print("Book Record Deleted....")
            else:
                s1.writerow(rec)
        else:
            s1.writerow(rec)
    f.close()
    f1.close()
    os.remove("library.csv")
    os.rename("temp.csv","library.csv")
    
    input("Press any key to continue..")

def searchbook():
    print("Search a Book Record")
    print("=====================")
    f=open('library.csv','r',newline='\r\n')  #Remove new line character from output
    r=input('Enter bookid you want to search')
    s=csv.reader(f)
    for rec in s:
        if rec[0]==r:
            print("-------------------------------")
            print("Book id=",rec[0])
            print("Book Name=",rec[1])
            print("Author=",rec[2])
            print("-------------------------------")
    f.close()
    input("Press any key to continue..")
def showallbooks():
    print("List of All Books")
    print("========================")
    f=open('library.csv','r',newline='\r\n')  #Remove new line character from output
    s=csv.reader(f)
    i=1
    for rec in s:
        print(rec[0],end="\t\t")
        print(rec[1],end="\t\t")
        print(rec[2])
        i+=1
    f.close()
    print("-------------------------------")
    input("Press any key to continue..")

def issueBook():
    print("Issue a Book")
    print("=====================")
    book_id = input("Enter book id to issue: ")

    with open('library.csv', 'r', newline='\r\n') as f:
        reader = csv.reader(f)
        library_data = list(reader)

    issued_book = None
    for book in library_data:
        if book[0] == book_id:
            issued_book = book
            library_data.remove(book)
            break

    if issued_book:
        with open('issued_books.csv', 'a', newline='\r\n') as f_issued:
            writer = csv.writer(f_issued)
            issued_book.append(get_due_date())  # Add due date to the issued book record
            writer.writerow(issued_book)
        with open('library.csv', 'w', newline='\r\n') as f_library:
            writer = csv.writer(f_library)
            writer.writerows(library_data)
        print("Book issued successfully!")
    else:
        print("Book not found in the library.")

    input("Press any key to continue..")

def returnIssuedBook():
    print("Return Issued Book")
    print("=====================")
    book_id = input("Enter book ID to return: ")

    with open('issued_books.csv', 'r', newline='\r\n') as f_issued:
        reader = csv.reader(f_issued)
        issued_books_data = list(reader)

    returned_book = None
    for book in issued_books_data:
        if book[0] == book_id:
            returned_book = book
            issued_books_data.remove(book)
            break

    if returned_book:
        fine = calculate_fine(returned_book)
        print(f"Book returned successfully! Fine: ${fine}")
        with open('issued_books.csv', 'w', newline='\r\n') as f_issued:
            writer = csv.writer(f_issued)
            writer.writerows(issued_books_data)

        with open('library.csv', 'a', newline='\r\n') as f_library:
            writer = csv.writer(f_library)
            returned_book.pop()  # Remove the due date before returning to the library
            writer.writerow(returned_book)
    else:
        print("Book not found in the issued books records.")

    input("Press any key to continue..")


def calculate_fine(returned_book):
    due_date_str = returned_book[-1]  # Last element is the due date
    due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
    return max(0, (datetime.now() - due_date).days) * 5  # $5 fine for each delayed day

def get_due_date():
    return (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

def dashboard():
    choice=0
    while choice!=8:
        print(" ")
        print("\n")
        print("|--------------------------|")
        print("| Libary Management System |")
        print("| -------------------------|")
        print(datetime.now())
        print('\n')
        print("########################")
        print("        Dashboard")
        print("       Welcome Admin")
        print("########################")
        print("1. Add a new Book Record")
        print("2. Edit Existing Book Record")
        print("3. Delete Existing Book Record")
        print("4. Search a Book")
        print("5. Show all Books")
        print("6. Issue Book")
        print("7. Return Issued Book")
        print("8. Log out")
        print("-------------------------------")
        choice=int(input('Enter your choice:'))
        if choice==1:
            addBook()
        elif choice==2:
            editBook()
        elif choice==3:
            deleteBook()
        elif choice==4:
            searchbook()
        elif choice==5:
            showallbooks()
        elif choice==6:
            issueBook()
        elif choice==7:
            returnIssuedBook()
        elif choice==8:
            print("You are logged out.......")
            break
handle_login()
