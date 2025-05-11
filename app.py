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
	number_of_pages_iso = len(lessons[0]['pages'])
	number_of_pages_shutter = len(lessons[1]['pages'])
	number_of_pages_aperture = len(lessons[2]['pages'])
	return render_template("home.html", number_of_pages_iso=number_of_pages_iso,
						   number_of_pages_shutter=number_of_pages_shutter,
						   number_of_pages_aperture=number_of_pages_aperture)

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
		return redirect(url_for("home"))

	number_of_pages = len(lessons[topic_map[topic]]['pages'])
	log_event(f"Entered lesson: {topic}")
	return render_template("learn.html", topic=topic, number_of_pages=number_of_pages)

@app.route("/learn/<topic>/<page>")
def learn_page(topic, page):
	topic = topic.lower()
	topic_map = {
		"iso": 0,
		"shutter": 1,
		"aperture": 2
	}

	if topic not in topic_map:
		return jsonify({"error": "Invalid topic"}), 404
	
	if page not in lessons[topic_map[topic]]['pages']:
		return jsonify({"error": "Page not found"}), 404

	lesson = lessons[topic_map[topic]]['pages'][page]
	log_event(f"Enter lesson: {topic}, Page: {page}")
	return jsonify(lesson)


SECTION_MAP = {
	"shutter":  (0, 5),
	"iso":      (5, 10),
	"aperture": (10, 15)
}

@app.route("/quiz")
def quiz_overview():
	return render_template("quiz_overview.html")



@app.route("/quiz_iso/<int:qid>", endpoint="quiz_iso_section", methods=["GET","POST"])
def quiz_iso_section(qid):
	start, total = 5, 5
	if qid == 1:
		session["answers_iso"] = []
	if request.method == "POST":
		ans = request.form.get("answer")
		session["answers_iso"].append(ans)
		session.modified = True
		if qid < total:
			return redirect(url_for("quiz_iso_section", qid=qid+1))
		else:
			return redirect(url_for("result_iso_section"))
	if qid < 1 or qid > total:
		return redirect(url_for("quiz_iso_section", qid=1))
	question = quiz[start + qid - 1]
	return render_template("quiz.html",
						   question=question,
						   question_id=qid,
						   total=total)

@app.route("/quiz_shutter/<int:qid>", endpoint="quiz_shutter_section", methods=["GET","POST"])
def quiz_shutter(qid):
	start, total = 0, 5
	if qid == 1:
		session["answers_shutter"] = []
	if request.method == "POST":
		ans = request.form.get("answer")
		session["answers_shutter"].append(ans)
		session.modified = True
		if qid < total:
			return redirect(url_for("quiz_shutter_section", qid=qid+1))
		else:
			return redirect(url_for("result_shutter_section"))
	if qid < 1 or qid > total:
		return redirect(url_for("quiz_shutter_section", qid=1))
	question = quiz[start + qid - 1]
	return render_template("quiz.html",
						   question=question,
						   question_id=qid,
						   total=total)

@app.route("/quiz_aperture/<int:qid>",endpoint="quiz_aperture_section", methods=["GET","POST"])
def quiz_aperture(qid):
	start, total = 10, 5
	if qid == 1:
		session["answers_aperture"] = []
	if request.method == "POST":
		ans = request.form.get("answer")
		session["answers_aperture"].append(ans)
		session.modified = True
		if qid < total:
			return redirect(url_for("quiz_aperture_section", qid=qid+1))
		else:
			return redirect(url_for("result_aperture_section"))
	if qid < 1 or qid > total:
		return redirect(url_for("quiz_aperture_section", qid=1))
	question = quiz[start + qid - 1]
	return render_template("quiz.html",
						   question=question,
						   question_id=qid,
						   total=total)

@app.route("/result_iso", endpoint="result_iso_section")
def result_iso_section():
	start, total = 5, 5
	answers = session.get("answers_iso", [])
	all_questions = []
	for i in range(total):
		q = quiz[start + i]
		user_ans = answers[i] if i < len(answers) else None
		all_questions.append({
			"prompt":          q["prompt"],
			"user_answer":     user_ans,
			"correct_answer":  q["answer"],
			"explanation":     q.get("explanation", "")
		})
	score = sum(1 for q in all_questions if q["user_answer"] == q["correct_answer"])
	session.pop("answers_iso", None)
	return render_template(
		"result.html",
		score=score,
		total=total,
		section="ISO",
		all_questions=all_questions
	)

@app.route("/result_shutter", endpoint="result_shutter_section")
def result_shutter_section():
	start, total = 0, 5
	answers = session.get("answers_shutter", [])
	all_questions = []
	for i in range(total):
		q = quiz[start + i]
		user_ans = answers[i] if i < len(answers) else None
		all_questions.append({
			"prompt":          q["prompt"],
			"user_answer":     user_ans,
			"correct_answer":  q["answer"],
			"explanation":     q.get("explanation", "")
		})
	score = sum(1 for q in all_questions if q["user_answer"] == q["correct_answer"])
	session.pop("answers_shutter", None)
	return render_template(
		"result.html",
		score=score,
		total=total,
		section="Shutter",
		all_questions=all_questions
	)

@app.route("/result_aperture", endpoint="result_aperture_section")
def result_aperture_section():
	start, total = 10, 5
	answers = session.get("answers_aperture", [])
	all_questions = []
	for i in range(total):
		q = quiz[start + i]
		user_ans = answers[i] if i < len(answers) else None
		all_questions.append({
			"prompt":          q["prompt"],
			"user_answer":     user_ans,
			"correct_answer":  q["answer"],
			"explanation":     q.get("explanation", "")
		})
	score = sum(1 for q in all_questions if q["user_answer"] == q["correct_answer"])
	session.pop("answers_aperture", None)
	return render_template(
		"result.html",
		score=score,
		total=total,
		section="Aperture",
		all_questions=all_questions
	)

@app.route("/quiz/<int:question_id>", methods=["GET", "POST"])
def quiz_page(question_id):
	total = len(quiz)

	if "answers" not in session:
		session["answers"] = [None] * total

	answers = session["answers"]

	if request.method == "POST":
		ans = request.form.get("answer")
		answers[question_id - 1] = ans
		session["answers"] = answers
		session.modified = True


		if question_id < total:
			return redirect(url_for("quiz_page", question_id=question_id + 1))
		else:
			return redirect(url_for("result"))

	if question_id < 1 or question_id > total:
		return redirect(url_for("quiz_page", question_id=1))

	question = quiz[question_id - 1]
	selected = answers[question_id - 1]

	return render_template(
		"quiz.html",
		question=question,
		question_id=question_id,
		total=total,
		selected_answer=selected
	)
@app.route("/result")
def result():
	log_event("Reached quiz result page")
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

@app.route("/learn/random")
def learn_random():
	import random
	topics = ["iso", "shutter", "aperture"]
	return redirect(url_for("learn", topic=random.choice(topics)))


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