from flask import render_template, Flask, request, redirect, url_for
from threading import Lock
from flask_socketio import SocketIO
from database import load_data, save_data
from user import find_user
from user import find_event

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

thread = None
thread_lock = Lock()

data = load_data()

# import cv2
# import mediapipe as mp
# import numpy as np
# import urllib.request

# def url_to_image(url):
#     # download the image, convert it to a NumPy array, and then read
#     # it into OpenCV format
#     resp = urllib.request.urlopen(url)
#     image = np.asarray(bytearray(resp.read()), dtype="uint8")
#     image = cv2.imdecode(image, cv2.IMREAD_COLOR)
#     # return the image
#     return image

# class HandDetector():
#     def __init__(self):
#         self.mpHands = mp.solutions.hands
#         self.hands = self.mpHands.Hands(False,2,min_detection_confidence=0.1,min_tracking_confidence=0.1)

#     def findPosition(self, img):
#         self.results = self.hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

#         lmList = []
#         if self.results.multi_hand_landmarks:
#             myHand = self.results.multi_hand_landmarks[0]
#             for id, lm in enumerate(myHand.landmark):
#                 h, w, c = img.shape
#                 cx, cy = int(lm.x * w), int(lm.y * h)
#                 lmList.append([id, cx, cy])

#         if(len(lmList) > 9):
#             return True

# detector = HandDetector()


# For adding static links use {{ url_for('static', filename='path') }}
# For redirecting use {{ url_for('page') }}
@socketio.on('connect')
def connect():
  print('Client connected')


@socketio.on('disconnect')
def disconnect():
  print('Client disconnected', request.sid)


@socketio.on('image')
def receive_image(data):
  print('Tracking image received')
  #print(data["url"])

  # result = detector.findPosition(url_to_image(data["url"]))

  socketio.emit('plastic', {'plastic': False})


def get_context():
  username = request.args.get("context")
  if username:
    return username

  return None


def get_message():
  message = request.args.get("message")
  if message:
    return message

  return None


@app.route("/signin", methods=["GET", "POST"])
def signin():
  username = request.form.get("username")
  password = request.form.get("password")

  print(username, password)

  if username and password:
    user = find_user(data, username)
    if user and user["password"] == password:
      return redirect(url_for("home", context=username))
    else:
      return render_template("signin.html",
                             message="Invalid username or password")
  else:
    return render_template("signin.html")


@app.route("/events", methods=["GET", "POST"])
def events():
  context = get_context()

  if request.method == "POST":
    event = {
        "name": request.form['name'],
        "date": request.form['date'],
        "numUsers": 0
    }

    data["events"].append(event)
    save_data(data)

  allEvents = data["events"]
  print(context)

  return render_template("events.html",
                         data=data,
                         context=context,
                         allEvents=allEvents)


@app.route("/tracker")
def tracker():
  context = get_context()
  message = get_message()
  return render_template("tracker.html", context=context, message=message)


@app.route("/challenges")
def challenges():
  context = get_context()
  return render_template("challenges.html", context=context)


@app.route("/")
@app.route("/index")
def home():
  context = get_context()

  return render_template("index.html", context=context)


@app.route("/contact")
def contact():
  context = get_context()

  return render_template("contact.html", context=context)


@app.route("/addUser")
def addUser():
  name = request.args.get("name")
  context = get_context()
  redirectURL = request.args.get("redirectURL")

  if name and (event := find_event(data, name)):
    event["numUsers"] += 1
    save_data(data)

  return redirect(url_for(redirectURL, context=context))


@app.route("/add/<int:value>")
def add(value):
  context = get_context()

  if context and (user := find_user(data, context)):
    user["points"] += value
    save_data(data)

  return redirect(url_for("dashboard", context=context))


@app.route("/dashboard")
def dashboard():
  context = get_context()

  allUsers = sorted(data["users"],
                    key=lambda user: user["points"],
                    reverse=True)

  return render_template("dashboard.html",
                         data=data,
                         context=context,
                         allUsers=allUsers)


app.run(host='0.0.0.0', debug=True, port=8080)

# sum(1 for user in data["users"] if user.event == "eventname")
