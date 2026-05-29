from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
import os
from database.db_config import get_connection
from ai.ethics_api import evaluate_ethics
import fitz  # PyMuPDF
from flask import make_response

app = Flask(__name__)
bcrypt = Bcrypt(app)

#Config
app.secret_key = 'AIzaSyBOu0Zd7YWZMlxRh97x_lV_fWeUMg1x'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


#Landing
@app.route('/')
def landing():
    return render_template('landing.html')


#Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                           (username, email, hashed_password))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/login')
        except Exception as e:
            return f"Signup error: {str(e)}"

    return render_template('signup.html')


#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (user_input, user_input))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect('/dashboard')
        else:
            return "Invalid username/email or password"

    return render_template('login.html')


#Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


#Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])


#Submit Prompt or PDF
@app.route('/submit', methods=['POST'])
def submit():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    ethics_type = request.form.get("ethics_type", "professional")

    text = request.form.get("prompt", "").strip()
    file = request.files.get("pdf_file")

    if file and file.filename.endswith(".pdf"):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        extracted_text = ""
        try:
            with fitz.open(filepath) as doc:
                for page in doc:
                    extracted_text += page.get_text()
            text = extracted_text.strip()
        except Exception as e:
            return f"Error processing PDF: {str(e)}"

    if not text:
        return "No prompt or PDF content found."

    try:
        full_prompt = f"This is a {ethics_type} ethics question: {text}"

        data = evaluate_ethics(full_prompt)

        session['last_score'] = data["score"]
        session['last_suggestion'] = data["suggestion"]
        session['last_input'] = text

    except Exception as e:
        return f"Error from AI evaluation: {str(e)}"

# Passing all fields to the template
    return render_template(
        "result.html",
        score=data["score"],
        suggestion=data["suggestion"],
        input_text=text,
        insights=data["insights"],
        score_json=int(data["score"]) if isinstance(data.get("score"), (int, float)) else 0
    )


@app.route('/download_result')
def download_result():
    score = request.args.get('score', 'N/A')
    suggestion = request.args.get('suggestion', 'N/A')
    input_text = request.args.get('input_text', 'N/A')

    content = (
        f"Ethical Score Report\n\n"
        f"Score: {score}/10\n\n"
        f"AI Suggestion:\n{suggestion}\n\n"
        f"Your Input:\n{input_text}\n"
    )

    response = make_response(content)
    response.headers["Content-Disposition"] = "attachment; filename=Ethical_Result.txt"
    response.headers["Content-Type"] = "text/plain"
    return response

#Running 
if __name__ == '__main__':
    app.run(debug=True)
