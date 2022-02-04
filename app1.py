
from flask import Flask,render_template,request
from flask_mail import Mail,Message
from flask import Flask, request, jsonify
from flask import render_template
from flask_cors import CORS, cross_origin
import pickle
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from flask_mail import Mail
from flask_mail import Message



app=Flask(__name__)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='pythonfabhost2021@gmail.com'
app.config['MAIL_PASSWORD']='skive@123'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

mail=Mail(app)

@app.route('/')
def index():

    return render_template("home.html")
def clean_text(a):
    text = re.sub('[^a-zA-Z0-9]', ' ', a)
    text = text.lower()
    text = nltk.word_tokenize(text)
    text = [WordNetLemmatizer().lemmatize(word) for word in text if word not in (stopwords.words('english'))]
    text = ' '.join(text)
    return text

@app.route('/base',methods=['GET','POST'])
def base():
    if request.method=="POST":

        email=request.form["email"]
        subject=request.form["subject"]
        msg=request.form["message"]

        messag=Message(subject,sender="pythonfabhost2021@gmail.com",recipients=[email])

        messag.body=msg
        message = request.form.get('message')
    with open('../Model/spamClassifier.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('../Model/count_vect', 'rb') as f:
        vectorizer = pickle.load(f)
    if model.predict(vectorizer.transform([clean_text(message)])):
        a='Spam Message '
        #return jsonify({'data': 'Spam Message!!', 'code': 1})
        return render_template('end.html',a=a)
        
    else:
        mail.send(messag)
        b='NON spam message'
        #return jsonify({'data': 'Non Spam Message!!', 'code': 0})
        return render_template('success.html',b=b)
         
        
        #return render_template("end.html")
         












if __name__ == "__main__":

    app.run(debug=True)