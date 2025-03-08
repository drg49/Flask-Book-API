from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

app = Flask(__name__)

# The load_dotenv() function will load the environmental variables from the .env file into the os.environ dictionary. 
# You can then access the environmental variables using os.environ.get('MY_VARIABLE').
load_dotenv()

database_uri = os.environ.get('DATABASE_URI')
port = int(os.environ.get('FLASK_RUN_PORT', 5000))  # Default to 5000 if not set

# Configure database connection
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = SQLAlchemy(app)

# Define a model for the database
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(75), nullable=False)
    author = db.Column(db.String(255))
    published_date = db.Column(db.Date)
    genre = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2))


@app.get('/')
def index():
    return 'The server is running.'

# Create a new book
@app.post('/create')
def create():
    data = request.get_json()
    book = Book(title = data.get('title'))
    db.session.add(book)
    db.session.commit()
    return jsonify({ 'message': 'The book was successfully created.' })

# Get all books
@app.get('/get-all')
def get_all():
    query_params = request.args
    query = Book.query

    # Check if the query parameters are present and filter the query accordingly
    if 'id' in query_params:
        query = query.filter(Book.id == query_params.get('id'))
    if 'title' in query_params:
        query = query.filter(Book.title.ilike(f"%{query_params.get('title')}%"))
    if 'author' in query_params:
        query = query.filter(Book.author.ilike(f"%{query_params.get('author')}%"))
    if 'published_date' in query_params:
        query = query.filter(Book.published_date == query_params.get('published_date'))
    if 'genre' in query_params:
        query = query.filter(Book.genre.ilike(f"%{query_params.get('genre')}%"))
    if 'price' in query_params:
        query = query.filter(Book.price == query_params.get('price'))

    books = query.all()
    output = []
    for book in books:
        output.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'published_date': book.published_date,
            'genre': book.genre,
            'price': book.price
        })
    return jsonify(output)

# Find a book by ID
@app.get('/find/<int:book_id>')
def findBook(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'published_date': book.published_date,
            'genre': book.genre,
            'price': book.price
        })
    else:
        return jsonify({ 'message': 'The book does not exist.' })

# Delete a book by ID
@app.delete('/delete/<int:book_id>')
def delete(book_id):
    try:
        print(f'Attempting to delete book by ID: {book_id}')
        Book.query.filter(Book.id == book_id).delete()
        db.session.commit()
        return jsonify({ 'message': 'The book was successfully deleted.' })
    except Exception as e:
        print(f'An exception occured: {e}')
        return jsonify({ 'message': 'The book failed to delete.' })
    
# Update a book by ID
@app.patch('/update')
def update():
    try:
        data = request.get_json()
        book = Book.query.get_or_404(data.get('id'))
        book.title = data.get('title')
        db.session.commit()
        return jsonify({ 'message': 'The book was successfully updated.' })
    except Exception as e:
        print(f'An exception occured: {e}')
        return jsonify({ 'message': 'The book failed to update.' })
    
if __name__ == '__main__':
    app.run(debug=True, port=port)
