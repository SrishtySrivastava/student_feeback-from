from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# ----------------- DATABASE -----------------
def init_db():
    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS feedback
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  student TEXT NOT NULL,
                  comment TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# ----------------- ROUTES -----------------
@app.route("/")
def index():
    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    c.execute("SELECT * FROM feedback")
    rows = c.fetchall()
    conn.close()
    return render_template("index.html", feedbacks=rows)

@app.route("/add", methods=["POST"])
def add_feedback():
    student = request.form["student"]
    comment = request.form["comment"]

    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    c.execute("INSERT INTO feedback (student, comment) VALUES (?, ?)", (student, comment))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

@app.route("/delete/<int:feedback_id>")
def delete_feedback(feedback_id):
    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    c.execute("DELETE FROM feedback WHERE id=?", (feedback_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/update/<int:feedback_id>", methods=["POST"])
def update_feedback(feedback_id):
    student = request.form["student"]
    comment = request.form["comment"]

    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    c.execute("UPDATE feedback SET student=?, comment=? WHERE id=?",
              (student, comment, feedback_id))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

# ----------------- AI FEATURE -----------------
@app.route("/summarize", methods=["POST"])
def summarize():
    comment = request.form["comment"]

    # Simple rule-based summarizer (replace with AI API if you like)
    summary = comment[:50] + "..." if len(comment) > 50 else comment

    return {"summary": summary}


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
