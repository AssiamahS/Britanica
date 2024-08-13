from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('britannia.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    definitions = conn.execute('SELECT * FROM definitions ORDER BY upvotes DESC').fetchall()
    conn.close()
    return render_template('index.html', definitions=definitions)

@app.route('/definition/<int:id>', methods=['GET', 'POST'])
def definition(id):
    conn = get_db_connection()
    definition = conn.execute('SELECT * FROM definitions WHERE id = ?', (id,)).fetchone()
    comments = conn.execute('SELECT * FROM comments WHERE definition_id = ?', (id,)).fetchall()
    if request.method == 'POST':
        comment = request.form['comment']
        conn.execute('INSERT INTO comments (definition_id, content) VALUES (?, ?)', (id, comment))
        conn.commit()
        conn.close()
        return redirect(url_for('definition', id=id))
    conn.close()
    return render_template('definition.html', definition=definition, comments=comments)

@app.route('/add_definition', methods=['GET', 'POST'])
def add_definition():
    if request.method == 'POST':
        term = request.form['term']
        definition = request.form['definition']
        conn = get_db_connection()
        conn.execute('INSERT INTO definitions (term, definition) VALUES (?, ?)', (term, definition))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_definition.html')

@app.route('/upvote/<int:id>')
def upvote(id):
    conn = get_db_connection()
    conn.execute('UPDATE definitions SET upvotes = upvotes + 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('definition', id=id))

if __name__ == '__main__':
    app.run(debug=True)
