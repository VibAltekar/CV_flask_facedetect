from flask import Flask, request, jsonify,render_template, Response
import cv2
from datetime import datetime
import json
app = Flask(__name__)
cascPath = "/Users/vibhav/Workspace_8_17/CV_flask/Webcam-Face-Detect/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

'''
@app.route('/',methods=["GET"])
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")
    x = (request.environ)
    if "HTTP_X_FORWARDED_FOR" in x.keys():
        reldat = " you are accessing from " + x["HTTP_USER_AGENT"] + " \n \n     your current ip address is: " + x["HTTP_X_FORWARDED_FOR"]
    else:
        reldat = " u r accessing from " + x["HTTP_USER_AGENT"]
    #print(x.keys())
    print(reldat)
    x2 = json.dumps(str(reldat), sort_keys = True, indent = 4, separators = (',', ': '))
    #if request.method == "GET":
        #return jsonify("hello")
    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>
    <img src="http://loremflickr.com/600/400"/>
    <h3> data {data} </h3>
    <br><br>
    """.format(time=the_time,data=x2,d2=x)
'''

@app.route('/sample',methods=["GET","POST"])
def return_str():
    if request.method == "POST":
        return jsonify("jared")
    if request.method == "GET":
        if int(str(datetime.now())[-8]) < 3:
            return jsonify("11111")
        if int(str(datetime.now())[-8]) > 2 and int(str(datetime.now())[-8]) < 7:
            return jsonify("22222")
        if int(str(datetime.now())[-8]) > 6:
            return jsonify("33333")



@app.route('/jsstream',methods=["GET","POST"])
def hi2():
    return render_template("index.html")

@app.route("/",methods=["GET","POST"])
def streamer():
    camera=cv2.VideoCapture(0)
    def gen():
        while True:
            rval, frame = camera.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.imwrite('t.jpg', frame)
            #run_inference("./t.jpg")
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
