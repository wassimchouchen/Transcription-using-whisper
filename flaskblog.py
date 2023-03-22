# from flask import Flask, render_template, url_for, request, flash, redirect
# from forms import RegistrationForm, LoginForm
# from flask_sqlalchemy import SQLAlchemy
# # import base64
# # from http.client import HTTPResponse
# # from sympy import sfield
# app = Flask(__name__)


# app.config['SECRET_KEY'] = '11ab30d464afbda875b611732c2de12e'

# posts = [
#     {
#         'author': 'Corey Schafer',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'April 20, 2018'
#     },
#     {
#         'author': 'Jane Doe',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'April 21, 2018'
#     }
# ]
# @app.route("/")
# @app.route("/home")
# def home():
#     return render_template('home.html', posts=posts)


# @app.route("/about")
# def about():
#     return render_template('about.html', title='About')

# @app.route("/register", methods=['GET','POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         flash(f'Acount created for {form.username.data}!', 'success')
#         return redirect(url_for('home'))
#     return render_template('register.html', title='Register', form=form)

# @app.route("/login", methods=['GET','POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.email.data== 'admin@blog.com' and form.password.data =='password':
#             flash ('You have been logged in!', 'success')
#             return redirect(url_for('home'))
#         else:
#             flash('Login Unsuccessful. Please check username and password', 'danger')
#     return render_template('login.html', title='Login', form=form)
# # @app.route("/recieve_audio", methods=['GET','POST'])
# # def receive_audio(request):
# #     # Handle the POST request and access the audio data here
# #     if request.method == 'POST':
# #         audio_data = request.body
# #         print("received body")
# #         audio_data_decoded = base64.b64decode(audio_data)
# #         print("received decode")
# #         audio_data_info = sfield.info(audio_data_decoded)
# #         sfield.write("audio_file.wav", audio_data_decoded, audio_data_info.samplerate)
# #         print("audio_data_info")
# #         return HTTPResponse("Audio received")
# # def ASR_WHISPER(payload) :
# #         file = open(payload, "rb")
# #         response = openai.Audio.transcribe("whisper-1", file)
# #         return (response["text"])
# if __name__ == '__main__':
#     app.run(debug=True)