from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json
import os
from datetime import datetime

app = Flask(__name__)

with open("data/lessons.json") as f:
	lessons = json.load(f)

with open("data/quiz.json") as f:
	quiz = json.load(f)

user_log = []
app.secret_key = os.urandom(24)
@app.route("/")
def home():
	log_event("Entered home page")
	return render_template("home.html")

@app.route("/learn")
def learn_overview():
	log_event("Visited learn overview page")
	return render_template("learn_overview.html")

@app.route("/learn/<topic>")
def learn(topic):
	topic = topic.lower()
	topic_map = {
		"iso": 0,
		"shutter": 1,
		"aperture": 2
	}

	if topic not in topic_map:
		# TODO include some kind of error message
		return redirect(url_for("home"))

	lesson_id = topic_map[topic] + 1
	lesson = lessons[topic_map[topic]]
	log_event(f"Entered lesson: {topic}")
	return render_template("learn.html", lesson=lesson, lesson_id=lesson_id, topic=topic)


@app.route("/quiz/<int:question_id>", methods=["GET", "POST"])
def quiz_page(question_id):
    if question_id == 1:
        session["answers"] = [] 
        
    elif "answers" not in session:
        session["answers"] = []

    if request.method == "POST":
        answer = request.form.get("answer")
        log_event(f"Answered question {question_id} with {answer}")
        session["answers"].append(answer)
        session.modified = True

        if question_id < len(quiz):
            return redirect(url_for("quiz_page", question_id=question_id + 1))
        else:
            return redirect(url_for("result"))

    if question_id < 1 or question_id > len(quiz):
        return redirect(url_for("quiz_page", question_id=1))
    question = quiz[question_id - 1]
    return render_template("quiz.html", question=question, question_id=question_id, total=len(quiz))


@app.route("/result")
def result():
	# log_event("Reached quiz result page")
    answers = session.get("answers", [])
    all_questions = []

    for idx, q in enumerate(quiz):
        user_ans = answers[idx] if idx < len(answers) else None
        all_questions.append({
            "prompt": q["prompt"],
            "user_answer": user_ans,
            "correct_answer": q["answer"],
            "explanation": q.get("explanation", "")
        })

    score = sum(1 for q in all_questions if q["user_answer"] == q["correct_answer"])
    total = len(quiz)

    return render_template("result.html", score=score, total=total, all_questions=all_questions)


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

@app.route("/about")
def about():
	log_event("Visited about page")
	return render_template("about.html")

@app.route("/interact/<interaction_type>")
def interact(interaction_type):
	log_event(f"Visited interact page for {interaction_type}")

	settings = {
		"iso": {
			"title": "Adjust the ISO",
			"options": ["100", "400", "1600", "6400", "25600"],
			"image_prefix": "iso_"
		},
		"shutter": {
			"title": "Adjust the Shutter",
			"options": ["1/250", "1/125", "1/60", "1/30", "1/15"],
			"image_prefix": "shutter_"
		},
		"aperture": {
			"title": "Adjust the Aperture",
			"options": ["f/22", "f/16", "f/11", "f/8", "f/4"],
			"image_prefix": "aperture_"
		}
	}

	config = settings.get(interaction_type)
	if not config:
		return redirect(url_for("home"))

	return render_template("interact.html", interaction=config, interaction_type=interaction_type)


if __name__ == "__main__":
	app.run(debug=True, port=5001)