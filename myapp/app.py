from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy user credentials (replace with your authentication logic)
users = {
    'admin': 'password',
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/index', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #print(username,password)
        if (username in users) and (users[username] == password):
            session['username'] = username
            return redirect(url_for('upload'))

        else:
            return render_template('index.html', message='Invalid username or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Implement your signup logic here
        username = request.form['username']
        password = request.form['password']
        users[username]=password
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' in session:
        if request.method == 'POST':
            # Handle file upload logic here
            # Save uploaded image to the server
            f = request.files['file']
            f.save(os.path.join('uploads', f.filename))
            return redirect(url_for('display_image', filename=f.filename))
        return render_template('upload.html')
    else:
        return redirect(url_for('login'))

@app.route('/display/<filename>')
def display_image(filename):
    if 'username' in session:
        return render_template('display.html', filename=filename)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
