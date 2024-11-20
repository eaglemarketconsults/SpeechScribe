from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

@app.route('/')
def feedback_form():
    return '''
    <!DOCTYPE html>
        <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Feedback</title>
      <style>
      @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300..700&display=swap');

* {
  padding: 0;
  font-family: "Fredoka", sans-serif;
  margin: 0;
  font-optical-sizing: auto;
  font-style: normal;
  list-style: none;
  font-variation-settings:
    "wdth" 100;
  -webkit-tap-highlight-color: transparent;
  box-sizing: border-box;
  transition: .3s ease 0s;
  scrollbar-width: none;
  text-decoration: none;
  color: #000000;
}

/* color syntax */
:root {
  --faintBlue: #ADBBDA5E;
  --borderLineWidth: 1px;
  --borderRadius: 10px;
  --dimBlue: #4F2FE8FC;
  --lightBlue: #7091E6;
  --darkBlue: #8697CA;
  --faintBlack: #6B6B6B;
  --pageBackgroundColor: #EDE8F5;
  --paddingSmall: 10px;
  --paddingBig: 20px;
}
.feedbackHeader{
  width: 100%;
  background: var(--faintBlue);
  padding: var(--paddingBig);
  display: flex;
  position: relative;
  justify-content: center;
  font-weight:500;
}
.feedbackHeader  i{
  position: absolute;
  left: 20px;
}
#feedbackContainer{
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  height: 100%;
  background:  whitesmoke;
  width: 100vw;
  display: none;
  gap: 15px;
  flex-direction: column;
  justify-content: center;
}
#closeFeedbackButton {
  position: absolute;
  top:10px;
  left: 10px;
}
form{
  overflow: hidden;
  padding: 10px;
  width: auto;
  display: grid;
}
.feedbackImg{
  margin:0 auto;
  width: 14rem;
}
.feedbackDiv1{
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.buttonDivs{
  display:grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}
.buttonDivs div{
  display: flex;
  align-items: center;
  gap: 10px;
}
label{
  font-size: 14px;
}
input{
  outline: none;
  border: none;
}
.textareaDiv{
  display: block;
  text-align: right;
}
textarea{
  height: 7rem;
  border: none;
  padding: var(--paddingSmall);
  outline: none;
  width: 100%;
  max-width: 100%;
}
.textareaDiv p{
  font-size:10px;
}
#email {
  height: 2rem;
  padding: var(--paddingSmall);
}
button{
  border: none;
  font-size:16px;
  background: var(--dimBlue);
  color: #FFFFFF;
  margin-top:15px;
  display: flex;
  place-self: center;
  justify-self: center;
  padding: var(--paddingBig);
}
@media(min-width:768px) {
  #feedbackContainer{
    flex-direction:row;
    padding: 20px;
    justify-content: right;
    align-items: center;
    width: 100%;
    height: 100%;
    padding-top:60px;
  }
  .feedbackImg{
    order: 2;
    width: 50%;
    height: auto;
  }
  form{
    flex-direction: column;
    display: flex;
  }
}
      </style>
    </head>
    <body>
      <form id="feedbackForm" action="/submit-feedback" method="POST" accept-charset="utf-8">
        <div>
          <strong>Feedback</strong>
          <div>
            <input type="radio" name="feedback" id="VSBQuality" value="VSBQuality" />
            <label for="VSBQuality">VSB Quality</label>
            <input type="radio" name="feedback" id="userInterface" value="userInterface" />
            <label for="userInterface">User Interface</label>
            <input type="radio" name="feedback" id="userExperience" value="userExperience" />
            <label for="userExperience">User Experience</label>
          </div>
          <div>
            <textarea placeholder="Tell us your thoughts" name="textArea" maxlength="1000"></textarea>
          </div>
          <div>
            <input placeholder="Email address" type="email" name="email" />
          </div>
        </div>
        <button type="submit">Send</button>
      </form>
    </body>
    </html>
    '''

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    feedback_type = request.form.get('feedback')
    feedback_text = request.form.get('textArea')
    email_address = request.form.get('email')

    sender_email = "stathamruss.co.uk@gmail.com"
    sender_password = "kvrm orbd zydq nwsu"  # Use an environment variable for security
    recipient_email = "stathamruss.co.uk@gmail.com"  # The company email receiving feedback

    subject = f"Feedback: {feedback_type}"
    body = f"""
    Feedback Type: {feedback_type}
    Feedback: {feedback_text}
    Sender Email: {email_address}
    """

    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

        return "Feedback sent successfully!"
    except Exception as e:
        return f"Failed to send feedback: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
