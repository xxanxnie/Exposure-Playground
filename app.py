from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
from datetime import datetime

app = Flask(__name__)

with open("data/lessons.json") as f:
    lessons = json.load(f)

with open("data/quiz.json") as f:
    quiz = json.load(f)

user_log = []

@app.route("/")
def home():
    log_event("Entered home page")
    return render_template("home.html")

@app.route("/learn/<int:lesson_id>")
def learn(lesson_id):
    if lesson_id < 1 or lesson_id > len(lessons):
        return redirect(url_for("home"))
    lesson = lessons[lesson_id - 1]
    log_event(f"Entered lesson {lesson_id}")
    return render_template("learn.html", lesson=lesson, lesson_id=lesson_id)

@app.route("/quiz/<int:question_id>", methods=["GET", "POST"])
def quiz_page(question_id):
    if request.method == "POST":
        answer = request.form.get("answer")
        log_event(f"Answered question {question_id} with {answer}")
    if question_id < 1 or question_id > len(quiz):
        return redirect(url_for("result"))
    question = quiz[question_id - 1]
    return render_template("quiz.html", question=question, question_id=question_id)

@app.route("/result")
def result():
    log_event("Reached quiz result page")
    return render_template("result.html")

@app.route("/log_event", methods=["POST"])
def log_event_api():
    data = request.json
    log_event(data.get("event"))
    return jsonify({"status": "ok"})

def log_event(event):
    timestamp = datetime.now().isoformat()
    user_log.append({"event": event, "time": timestamp})
    with open("logs/user_log.json", "w") as f:
        json.dump(user_log, f, indent=2)

if __name__ == "__main__":
    app.run(debug=True, port=5001)