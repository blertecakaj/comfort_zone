from flask import Flask, render_template, request, redirect, session, flash, jsonify
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import requests
import re
import stripe

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = 'secret'
bcrypt = Bcrypt(app)


nyt_key ='qNS0aG1k1DENr5O8JbPEyJXnc9yP6tEA'

stripe_secret_key = 'sk_test_KDY2ZBNJ6ZMA9a46g7WjkaaI007e1tqiAv'
stripe_publishable_key= 'pk_test_8yq5ZQ4KcAYogMhiZNzQEsii00SJEAvZP5' 


stripe.api_key = stripe_secret_key
 

@app.route('/login_register')
def login_register():
    return render_template("registerlogin.html")

@app.route('/register', methods=['POST'])
def register_user():
    is_valid = True

    if len(request.form['first_name']) < 2:
        is_valid = False
        flash("First name must be at least 2 characters long!")
    if len(request.form['last_name']) < 2:
        is_valid = False
        flash("Last name must be at least 2 characters long!")
    if len(request.form['password']) < 8:
        is_valid = False
        flash("Password must be at least 8 characters long!")
    if request.form['c_password'] != request.form['password']:
        is_valid = False
        flash("Passwords must match!")
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Please use a valid email address!")

    if not is_valid:
        return redirect('/login_register')
    else:
        mysql = connectToMySQL('comfort_zone')
        query = "INSERT into users (first_name, last_name, email, password, user_level, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(em)s, %(pw)s, 1, NOW(), NOW())"
        data = {
            'fn': request.form['first_name'],
            'ln': request.form['last_name'],
            'em': request.form['email'],
            'pw': bcrypt.generate_password_hash(request.form['password'])
        }
        user_id = mysql.query_db(query, data)
        session['user_id'] = user_id
        session['user_level'] = 1

        return redirect('/')

@app.route('/login', methods=['POST'])
def login_user():

    is_valid = True

        
    if len(request.form['password']) < 1:
        is_valid = False
        flash("Please enter your password!")
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Please enter a valid email address!")

    if not is_valid:
        return redirect('/login_register')
    else:
        mysql = connectToMySQL('comfort_zone')
        query = "SELECT * from users where users.email = %(em)s"
        data = {
            'em': request.form['email']
        }
        user = mysql.query_db(query, data)
        if user:
            hashed_password = user[0]['password']
            if bcrypt.check_password_hash(hashed_password, request.form['password']):
                session['user_id'] = user[0]['user_id']
                session['user_level'] = user[0]['user_level']
                return redirect("/")
            else:
                flash("Invalid password!")
                return redirect('/login_register')

        else:
            flash("Please use a valid email address!")
            return redirect('/login_register')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/')
def fetch_books():

    # This query will UPSERT NYT NonFiction Best Sellers- Not the "nonfinction" in she api key This query happens when the page is loaded and the route can be changed.
    result = requests.get(f'https://api.nytimes.com/svc/books/v3/lists/current/hardcover-nonfiction.json?api-key={nyt_key}')
    result.status_code
    result.text
    json_results= result.json()

    books=json_results['results']['books']

    for val in books:
        isbn = val['primary_isbn13']
        title = val['title']
        author = val['author']
        description= val['description']
        img_url = val['book_image']
        category="Nonfiction"
        price =20.35
        mysql = connectToMySQL("comfort_zone")
        query = "REPLACE INTO books(id, isbn, title, author, description, img_url, category, price) VALUES (%(id)s, %(isbn)s, %(title)s, %(au)s, %(desc)s, %(img)s, %(cat)s, %(up)s);"

        data = {
            "id": isbn,
            "isbn": isbn,
            "title": title,
            "au": author,
            "desc": description,
            "img": img_url,
            "cat": category,
            "up": price
            
        }
        nonfiction_book_id = mysql.query_db(query,data)

    # This query will UPSERT NYT Advice How To And Miscellaneous Best Sellers- This query happens when the page is loaded and the route can be changed.
    result = requests.get(f'https://api.nytimes.com/svc/books/v3/lists/current/advice-how-to-and-miscellaneous.json?api-key={nyt_key}')
    result.status_code
    result.text
    json_results= result.json()

    books=json_results['results']['books']

    for val in books:
        isbn = val['primary_isbn13']
        title = val['title']
        author = val['author']
        description= val['description']
        img_url = val['book_image']
        category="advice_how_to_miscellaneous"
        price=11.99
        mysql = connectToMySQL("comfort_zone")
        query = "REPLACE INTO books(id, isbn, title, author, description, img_url, category, price) VALUES (%(id)s, %(isbn)s, %(title)s, %(au)s, %(desc)s, %(img)s, %(cat)s, %(up)s);"

        data = {
            "id": isbn,
            "isbn": isbn,
            "title": title,
            "au": author,
            "desc": description,
            "img": img_url,
            "cat": category,
            "up": price
        }
        advice_how_to_miscellaneous_book_id = mysql.query_db(query,data)

    # This query will UPSERT NYT Children's Series This query happens when the page is loaded and the route can be changed.
    result = requests.get(f'https://api.nytimes.com/svc/books/v3/lists/current/series-books.json?api-key={nyt_key}')
    result.status_code
    result.text
    json_results= result.json()

    books=json_results['results']['books']

    for val in books:
        isbn = val['primary_isbn13']
        title = val['title']
        author = val['author']
        description= val['description']
        img_url = val['book_image']
        category="Childrens_Series"
        price=15.43
        mysql = connectToMySQL("comfort_zone")
        query = "REPLACE INTO books(id, isbn, title, author, description, img_url, category, price) VALUES (%(id)s, %(isbn)s, %(title)s, %(au)s, %(desc)s, %(img)s, %(cat)s, %(up)s);"

        data = {
            "id": isbn,
            "isbn": isbn,
            "title": title,
            "au": author,
            "desc": description,
            "img": img_url,
            "cat": category,
            "up": price
        }
        childrens_series_book_id = mysql.query_db(query,data)

    # This query will UPSERT NYT Young Adults This query happens when the page is loaded and the route can be changed.
    result = requests.get(f'https://api.nytimes.com/svc/books/v3/lists/current/young-adult-hardcover.json?api-key={nyt_key}')
    result.status_code
    result.text
    json_results= result.json()

    books=json_results['results']['books']

    for val in books:
        isbn = val['primary_isbn13']
        title = val['title']
        author = val['author']
        description= val['description']
        img_url = val['book_image']
        category="Young_Adult"
        price=18.65
    
        mysql = connectToMySQL("comfort_zone")
        query = "REPLACE INTO books(id, isbn, title, author, description, img_url, category, price) VALUES (%(id)s, %(isbn)s, %(title)s, %(au)s, %(desc)s, %(img)s, %(cat)s, %(up)s);"

        data = {
            "id": isbn,
            "isbn": isbn,
            "title": title,
            "au": author,
            "desc": description,
            "img": img_url,
            "cat": category,
            "up": price
        }
        young_adult_book_id = mysql.query_db(query,data)

    # This query will UPSERT NYT Graphic Books and Manga This query happens when the page is loaded and the route can be changed.
    result = requests.get(f'https://api.nytimes.com/svc/books/v3/lists/current/graphic-books-and-manga.json?api-key={nyt_key}')
    result.status_code
    result.text
    json_results= result.json()

    books=json_results['results']['books']

    for val in books:
        isbn = val['primary_isbn13']
        title = val['title']
        author = val['author']
        description= val['description']
        img_url = val['book_image']
        category="graphic_manga"
        price=15.88

        mysql = connectToMySQL("comfort_zone")
        query = "REPLACE INTO books(id, isbn, title, author, description, img_url, category, price) VALUES (%(id)s, %(isbn)s, %(title)s, %(au)s, %(desc)s, %(img)s, %(cat)s, %(up)s);"

        data = {
            "id": isbn,
            "isbn": isbn,
            "title": title,
            "au": author,
            "desc": description,
            "img": img_url,
            "cat": category,
            "up": price
        }
        graphic_manga_book_id = mysql.query_db(query,data)


    # This query will UPSERT NYT NonFiction Best Sellers- Not the "finction" in she api key This query happens when the pasge is loaded and the route can be changed.
    result = requests.get(f'https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?api-key={nyt_key}')
    result.status_code
    result.text
    json_results= result.json()

    books=json_results['results']['books']
    for val in books:
        isbn = val['primary_isbn13']
        title = val['title']
        author = val['author']
        description= val['description']
        img_url = val['book_image']
        category="Fiction"
        price=19.99
        mysql = connectToMySQL("comfort_zone")
        query = "REPLACE INTO books(id, isbn, title, author, description, img_url, category, price) VALUES (%(id)s, %(isbn)s, %(title)s, %(au)s, %(desc)s, %(img)s, %(cat)s, %(up)s);"

        data = {
            "id": isbn,
            "isbn": isbn,
            "title": title,
            "au": author,
            "desc": description,
            "img": img_url,
            "cat": category,
            "up": price
        }
        fiction_book_id = mysql.query_db(query,data)
    
    #Query to fetch all books and make data available to the render books.html template

    mysql=connectToMySQL("comfort_zone")
    query='SELECT * From books'
    all_books = mysql.query_db(query,data)

    mysql=connectToMySQL("comfort_zone")
    query='SELECT category,img_url From books group by category'
    cat = mysql.query_db(query,data)

    return render_template('index.html', all_books = all_books, category=cat)

@app.route('/add_to_cart/<users_id>/<books_id>')
def add_to_cart(users_id, books_id):
    if 'user_id' not in session:
        return redirect('/')
        flash("You have to login in order to add a book to cart!")
    mysql = connectToMySQL('comfort_zone')
    query = "INSERT into cart (user_id, books_id) VALUES (%(uid)s, %(bid)s)"
    data = {
        'uid': session['user_id'],
        'bid': books_id
    }
    mysql.query_db(query, data)
    return redirect('/book_details/{}'.format(books_id))


@app.route('/remove_from_cart/<users_id>/<books_id>')
def  remove_from_cart(users_id, books_id):
    if 'user_id' not in session:
        return redirect('/')
        flash("You have to login in order to remove a book from your cart!")
    mysql = connectToMySQL('comfort_zone')
    query = "DELETE from cart where user_id=%(uid)s and books_id=%(bid)s"
    data = {
        'uid': session['user_id'],
        'bid': books_id
    }
    mysql.query_db(query, data)
    return redirect('/cart')

@app.route('/cart')
def cart():
    mysql = connectToMySQL('comfort_zone')
    query = "SELECT * from cart join books on cart.books_id=books.id where user_id=%(rid)s"
    data = {
        'rid': session['user_id']
    }
    cart = mysql.query_db(query, data)
    return render_template('cart.html',cart=cart)


@app.route('/book_details/<id>')
def book_details(id):

    if 'user_id' not in session:
        return redirect('/login_register')

    mysql = connectToMySQL('comfort_zone')
    query = "select books.id, books.isbn,books.description, books.title, wishlist_books.books_id, wishlist_books.users_id, books.author, books.img_url, books.price FROM wishlist_books right JOIN books ON books.id = wishlist_books.books_id left join users on wishlist_books.users_id = users.user_id where books.id = %(bid)s"
    data = {
        'bid':id
    }
    book = mysql.query_db(query, data)

    mysql = connectToMySQL('comfort_zone')
    query = "SELECT books_id from wishlist_books where users_id=%(uid)s"
    data = {
        'uid': session['user_id']
    }
    liked_books_ids = [data['books_id'] for data in mysql.query_db(query, data)]

    mysql = connectToMySQL('comfort_zone')
    query = "SELECT books_id from cart where user_id=%(uid)s"
    cart_id = [data['books_id'] for data in mysql.query_db(query, data)]
 
    mysql = connectToMySQL('comfort_zone')
    query = "select * from reviews left join users on users.user_id = reviews.author right join books on books.id = reviews.book_id where books.id= %(bid)s"
    data = {
        'bid':id
    }
    reviews = mysql.query_db(query, data)

    if reviews[0]['content'] is None:
        return render_template("book_details.html", book=book[0], liked_books_ids=liked_books_ids, reviews=[],cart_id=cart_id)

    return render_template("book_details.html", book=book[0], liked_books_ids=liked_books_ids, reviews=reviews,cart_id=cart_id)

@app.route('/book_category/<category>')
def book_category(category):
    mysql = connectToMySQL('comfort_zone')
    query = "SELECT * from books where books.category = %(ctg)s;"
    data = {
        'ctg': category
    }
    books = mysql.query_db(query, data)
    return render_template("book_category.html", books=books)

@app.route('/add_review/<id>', methods=['POST'])
def add_review(id):
    if 'user_id' not in session:
        return redirect('/')
        flash("You have to login to post a review!")
    is_valid = True
    mysql = connectToMySQL('comfort_zone')
    if len(request.form['content']) < 5:
        is_valid = False
        flash("Your review must contain at least 5 characters!")
    if len(request.form['content']) > 255:
        is_valid = False
        flash("Your review cannot be more than 255 characters!")

    if is_valid:
        mysql = connectToMySQL('comfort_zone')
        query = "INSERT into reviews (content, author, book_id, created_at, updated_at) VALUES (%(con)s, %(uid)s, %(bid)s, NOW(), NOW())"
        data = {
            'con': request.form['content'],
            'uid': session['user_id'],
            'bid': id
        }
        review = mysql.query_db(query, data)

        return redirect('/book_details/{}'.format(id))

@app.route('/edit_review/<review_id>')
def edit_review(review_id):
    if 'user_id' not in session:
        return redirect('/')
    mysql = connectToMySQL('comfort_zone')
    query = "SELECT * from reviews where review_id=%(rid)s"
    data = {
        'rid': review_id
    }
    review = mysql.query_db(query, data)
    
    return render_template('edit_review.html', review=review[0])


@app.route('/update_review/<review_id>', methods=['POST'])
def update_review(review_id):
    if 'user_id' not in session:
        return redirect('/')
    is_valid = True
    if len(request.form['content']) < 5:
        is_valid = False
        flash("Your review must contain at least 5 characters!")
    if len(request.form['content']) > 255:
        is_valid = False
        flash("Your review cannot be longer than 255 characters!")

    if is_valid:
        mysql = connectToMySQL("comfort_zone")
        query = "UPDATE reviews SET reviews.content=%(con)s, reviews.updated_at=NOW() WHERE reviews.review_id = %(rid)s"
        data = {
            'con': request.form['content'],
            'rid': review_id
        }
        mysql.query_db(query,data)
        flash('Your review has been updated successfully!')
        return redirect("/edit_review/{}".format(review_id))

    return redirect("/edit_review/{}".format(review_id))

@app.route('/delete_review/<review_id>')
def delete_review(review_id):
    if 'user_id' not in session:
        return redirect('/')
    mysql = connectToMySQL('comfort_zone')
    query = "DELETE from reviews where review_id = %(rid)s"
    data = {
        'rid': review_id
    }
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/add_to_wishlist/<users_id>/<books_id>')
def add_to_wishlist(users_id, books_id):
    if 'user_id' not in session:
        return redirect('/')
        flash("You have to login in order to add a book from your wishlist!")
    mysql = connectToMySQL('comfort_zone')
    query = "INSERT into wishlist_books (users_id, books_id) VALUES (%(uid)s, %(bid)s)"
    data = {
        'uid': session['user_id'],
        'bid': books_id
    }
    mysql.query_db(query, data)
    return redirect('/book_details/{}'.format(books_id))

@app.route('/remove_from_wishlist/<users_id>/<books_id>')
def  remove_from_wishlist(users_id, books_id):
    if 'user_id' not in session:
        return redirect('/')
        flash("You have to login in order to remove a book from your wishlist!")
    mysql = connectToMySQL('comfort_zone')
    query = "DELETE from wishlist_books where users_id=%(uid)s and books_id=%(bid)s"
    data = {
        'uid': session['user_id'],
        'bid': books_id
    }
    mysql.query_db(query, data)
    return redirect('/book_details/{}'.format(books_id))

@app.route('/users')
def users():
    if 'user_id' not in session:
        return redirect('/')
    if session['user_level'] != 9:
        return redirect('/')
    else:
        mysql = connectToMySQL('comfort_zone')
        query = "SELECT users.user_id, users.first_name, users.last_name, users.email, users.user_level from users"
        users = mysql.query_db(query)
        return render_template('users.html', users=users)

@app.route('/make_admin/<user_id>')
def make_admin(user_id):
    if 'user_id' not in session:
        return redirect('/')
    if session['user_level'] != 9:
        return redirect('/')
    else:
        mysql = connectToMySQL('comfort_zone')
        query = "UPDATE users SET users.user_level = 9 where users.user_level=1 and users.user_id=%(uid)s"
        data = {
            'uid': user_id
        }
        mysql.query_db(query, data)
        return redirect('/users')

@app.route('/remove_admin/<user_id>')
def remove_admin(user_id):
    if 'user_id' not in session:
        return redirect('/')
    if session['user_level'] != 9:
        return redirect('/')
    else:
        mysql = connectToMySQL('comfort_zone')
        query = "UPDATE users SET users.user_level = 1 where users.user_level=9 and users.user_id=%(uid)s"
        data = {
            'uid': user_id
        }
        mysql.query_db(query, data)
        return redirect('/users')

@app.route("/user_profile")
def on_profile():

    if 'user_id' not in session:
        flash("You must be loged in")
        return redirect('login_register')

    mysql = connectToMySQL('comfort_zone')
    query="SELECT * FROM users WHERE user_id = %(id)s"
    data={
        'id': session['user_id']
    }
    result = mysql.query_db(query,data)

    mysql = connectToMySQL('comfort_zone')
    query = "SELECT books.img_url, users.user_id FROM users JOIN wishlist_books ON users.user_id=wishlist_books.users_id JOIN books on books.id =wishlist_books.books_id "
    images = mysql.query_db(query)

    return render_template('userProfile.html',users=result,images=images)



@app.route("/on_book_details")
def on_book_details():
    return render_template("bookdetail.html")

#*********BEGIN STRIPE API PAYMENT**************************************
@app.route("/payment/<books_id>")
def payment_details(books_id):
    mysql=connectToMySQL('comfort_zone')
    query= "Select cart.books_id, books.price, user_id FROM cart join books on cart.books_id = books.id where user_id = %(uid)s and books.id = %(bid)s"
    data= {
        'uid': session['user_id'],
        'bid': books_id
    }

    result= mysql.query_db(query, data)
    total = result[0]
   
    return render_template('checkout.html',key=stripe_publishable_key, total = total)

@app.route('/charge/<books_id>', methods=['POST'])
def charge(books_id):
    mysql=connectToMySQL('comfort_zone')
    query= "Select cart.books_id, books.price, cart.user_id, users.email FROM cart join books on cart.books_id = books.id join users on cart.user_id= users.user_id where cart.user_id = %(uid)s and books.id = %(bid)s"
    data= {
        'uid': session['user_id'],
        'bid': books_id
    }

    result= mysql.query_db(query, data)
    charge = result[0]

    # amount in cents
    amount = charge['price']
    f_amount = int(amount)*100
    email = charge['email']
    print(amount)
    print(email)

    customer = stripe.Customer.create(
        email= email,
        source=request.form['stripeToken']
    )

    stripe.Charge.create(
        customer=customer.id,
        amount=f_amount,
        currency='usd',
        description='Flask Charge'
    )
    #this will delete the book that was just paid for.  Same code just moved it down so it runs after card is successful
    mysql = connectToMySQL('comfort_zone')
    query="DELETE from cart where user_id=%(uid)s and books_id=%(bid)s"
    data = {
        'uid': session['user_id'],
        'bid': books_id
    }
    mysql.query_db(query, data)

    return render_template('charge.html', amount=amount, charge=charge)

if(__name__) =="__main__":
    app.run(debug=True)
