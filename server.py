from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL
from flask_restful import Resource, Api
from json import dumps
import requests
import datetime


app = Flask(__name__)


nyt_key ='qNS0aG1k1DENr5O8JbPEyJXnc9yP6tEA'

@app.route("/")
def index():
    return render_template('index.html')
    
@app.route('/')
def landing():
    pass
    return redirect('/books')

@app.route('/books')


def fetch_books():
    # This query will UPSERT NYT NonFiction Best Sellers- Not the "nonfinction" in she api key This query happens when the pasge is loaded and the route can be changed.
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
        mysql = connectToMySQL("comfort_zone")
        query = "REPLACE INTO books(id, isbn, title, author, description, img_url, category) VALUES (%(id)s, %(isbn)s, %(title)s, %(au)s, %(desc)s, %(img)s, %(cat)s);"

        data = {
            "id": isbn,
            "isbn": isbn,
            "title": title,
            "au": author,
            "desc": description,
            "img": img_url,
            "cat": category
        }
        nonfiction_book_id = mysql.query_db(query,data)


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
        mysql = connectToMySQL("comfort_zone")
        query = "REPLACE INTO books(id, isbn, title, author, description, img_url, category) VALUES (%(id)s, %(isbn)s, %(title)s, %(au)s, %(desc)s, %(img)s, %(cat)s);"

        data = {
            "id": isbn,
            "isbn": isbn,
            "title": title,
            "au": author,
            "desc": description,
            "img": img_url,
            "cat": category
        }
        fiction_book_id = mysql.query_db(query,data)

    #Query to fetch all books and make data available to the render books.html template

    mysql=connectToMySQL("comfort_Zone")
    query='SELECT * From books'
    all_books = mysql.query_db(query,data)
        
    return render_template('books.html', all_books = all_books)



if __name__ == "__main__":
    app.run(debug=True)
