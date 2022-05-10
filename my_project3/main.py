from flask import Flask, render_template, request
import sqlite3

app = Flask('Library')


@app.route('/')
@app.route('/index', methods=["GET", "POST"])
def index():
    con = sqlite3.connect("books.sqlite")
    cur = con.cursor()
    books = cur.execute("""SELECT * FROM books""").fetchall()
    au = cur.execute("""SELECT * FROM authors""").fetchall()
    authors = {}
    for a in au:
        authors[a[0]] = a[1]
    for i in range(len(books)):
        books[i] = list(books[i])
        books[i][2] = authors[books[i][2]]
    return render_template('index.html', books=books)


@app.route('/add_book', methods=["GET", "POST"])
def add_book():
    con = sqlite3.connect("books.sqlite")
    cur = con.cursor()
    books = cur.execute("""SELECT * FROM books""").fetchall()
    au = cur.execute("""SELECT * FROM authors""").fetchall()
    if request.method == 'POST':
        book = request.form.get('book')
        author = request.form.get('author')
        if book:
            for i in au:
                if i[1] == author:
                    author = i[0]
            cur.execute("""INSERT INTO books (title, author) 
            VALUES (?, ?)""", (book, author))
            con.commit()
        author1 = request.form.get('author1')
        if author1:
            cur.execute("""INSERT INTO authors (title) 
            VALUES (?)""", (author1,))
            con.commit()
    con.close()
    return render_template('add.html', authors=au)


@app.route('/delete_book', methods=["GET", "POST"])
def delete_book():
    con = sqlite3.connect("books.sqlite")
    cur = con.cursor()
    books = cur.execute("""SELECT * FROM books""").fetchall()
    au = cur.execute("""SELECT * FROM authors""").fetchall()
    authors = {}
    for a in au:
        authors[a[0]] = a[1]
    for i in range(len(books)):
        books[i] = list(books[i])
        books[i][2] = authors[books[i][2]]
    if request.method == 'POST':
        b = request.form.get('book')
        if b:
            book = b.split('"')[1]
            author = b.split('"')[0][:-1]
            print(book)
            print(author)
            cur.execute("""DELETE FROM books 
            WHERE title = ? AND author = 
            (SELECT id FROM authors WHERE title = ?)""", (book, author))
            con.commit()
        author1 = request.form.get('author')
        print(author1)
        if author1:
            cur.execute("""DELETE FROM books 
            WHERE author = (SELECT id FROM authors WHERE title = ?)""", (author1,))
            cur.execute("""DELETE FROM authors WHERE title = ?""", (author1,))
            con.commit()
    con.close()
    return render_template('delete.html', books=books, authors=au)



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')