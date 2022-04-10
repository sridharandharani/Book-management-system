from flask import Flask, request, render_template
import sqlite3

from werkzeug.utils import redirect

folder = sqlite3.connect("books.db",check_same_thread=False)

listoftables1 = folder.execute("select * from sqlite_master where type = 'table' and name = 'mybook'").fetchall()
listoftables2 = folder.execute("select * from sqlite_master where type = 'table' and name = 'myuser'").fetchall()

if listoftables1 != []:
    print("Table already exists !")
else:
    folder.execute('''create table mybook(
                       id integer primary key autoincrement,
                       name text,
                       author text,
                       category text,
                       price integer,
                       publisher text
                       );''')
    print("Table created sucessfully ")

if listoftables2 != []:
    print("Table already exists !")
else:
    folder.execute('''create table myuser(
                       id integer primary key autoincrement,
                       name text,
                       address text,
                       email text,
                       phone integer,
                       pass text
                       );''')
    print("Table created sucessfully ")

books = Flask(__name__)

@books.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        getUsername = request.form["uname"]
        getPassword = request.form["pass"]
        print(getUsername)
        print(getPassword)
        if getUsername == "admin" and getPassword == "9875":
            return redirect('/admindashboard')
        else:
            return redirect('/register')
    return render_template("login.html")

@books.route('/admindashboard',methods=['GET','POST'])
def admin_dashboard():
    if request.method == 'POST':
        getBookName = request.form["bname"]
        getAuthor = request.form["author"]
        getCategory = request.form["category"]
        getPrice = request.form["price"]
        getPublisher = request.form["publisher"]
        print(getBookName)
        print(getAuthor)
        print(getCategory)
        print(getPrice)
        print(getPublisher)

        try:
            folder.execute("insert into mybook(name,author,category,price,publisher) \
            values('"+getBookName+"','"+getAuthor+"','"+getCategory+"',"+getPrice+",'"+getPublisher+"')")
            folder.commit()
            print("Inserted sucessfully")
            return redirect('/viewall')
        except Exception as error:
            print(error)
    return render_template("admindashboard.html")

@books.route('/viewall')
def viewall():
    cursor = folder.cursor()
    cursor.execute("select * from mybook")
    result = cursor.fetchall()
    return render_template("viewall.html", book = result)

@books.route('/search',methods=['GET','POST'])
def search():
    cursor = folder.cursor()
    if request.method == 'POST':
        getBookname = request.form["bname"]
        cursor.execute("select * from mybook where name= '"+getBookname+"'")
        result = cursor.fetchall()
        if result is None:
            print("Book name not exists ")
        else:
            return render_template("search.html",search=result,status=True)
    else:
        return render_template("search.html", search=[], status=False)

@books.route('/up', methods=['GET', 'POST'])
def update():
    global getBookname
    folder.cursor()
    if request.method == "POST":
        getBookname = request.form["bname"]
        return redirect('/update')

    return render_template("update.html")

@books.route('/update', methods=['GET', 'POST'])
def updation():
    if request.method == "POST":
        getBookName = request.form["bname"]
        getAuthor = request.form["author"]
        getCategory = request.form["category"]
        getPrice = request.form["price"]
        getPublisher = request.form["publisher"]

        folder.execute("update mybook set name='"+getBookName+"',author='"+getAuthor+"',category='"+getCategory+"',price="+getPrice+",publisher='"+getPublisher+"' ")
        folder.commit()
        print("Updated Successfully......")

        return redirect('/viewall')

    return render_template("updation.html")

@books.route('/delete', methods=['GET', 'POST'])
def deletion():
    if request.method == "POST":
        getBookname = request.form["bname"]
        folder.execute("delete from mybook where name='" + getBookname + "'")
        folder.commit()
        print("Deleted Successfully")
        return redirect('/viewall')
    return render_template("delete.html")

@books.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        getName = request.form["name"]
        getAddress = request.form["add"]
        getEmail = request.form["email"]
        getPhone = request.form["phone"]
        getPassword = request.form["pass"]
        print(getName)
        print(getAddress)
        print(getEmail)
        print(getPhone)
        print(getPassword)

        try:
            folder.execute("insert into myuser(name,address,email,phone,pass) \
            values('" + getName + "','" + getAddress + "','" + getEmail + "'," + getPhone + ",'" + getPassword + "')")
            folder.commit()
            print("Inserted sucessfully")
            return redirect('/userlogin')

        except Exception as error:
            print(error)
    return render_template("register.html")

@books.route('/userlogin',methods=['GET','POST'])
def userlogin():
    if request.method == 'POST':
        getEmail = request.form["email"]
        getpass = request.form["pass"]
        print(getEmail)
        print(getpass)
        return redirect('/userview')
    return render_template("userlogin.html")

@books.route('/userview')
def userview():
    cursor = folder.cursor()
    cursor.execute("select * from mybook")
    result = cursor.fetchall()
    return render_template("userview.html", book=result)


@books.route('/usersearch',methods=['GET','POST'])
def usersearch():
    cursor = folder.cursor()
    if request.method == 'POST':
        getBookname = request.form["bname"]
        cursor.execute("select * from mybook where name= '" + getBookname + "'")
        result = cursor.fetchall()
        if result is None:
            print("Book name not exists ")
        else:
            return render_template("usersearch.html", search=result, status=True)
    else:
        return render_template("usersearch.html", search=[], status=False)








if __name__ == "__main__":
    books.run()