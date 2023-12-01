from app import app, login_is_required
from flask import render_template, redirect, session, jsonify, url_for, make_response
from flask import request as req
from controller import google_auth
from .yt_transcript import transcript
from .pegasus import pegasus
from .punctuation import punctuation
from .chunking import chunking


@app.route('/')
def index():
    return render_template('index.html')


#For Google Login. -Saugata
@app.route('/google_login')
def google_login():
    return google_auth.google_login(google_auth.setup_google_auth())

@app.route('/callback')
def callback():
    google_auth.google_callback(google_auth.setup_google_auth())
    return redirect("/dashboard")

#For Google Login. -Saugata




@app.route('/summary')
@login_is_required
def summary():
    return render_template('summary.html')


@app.route('/dashboard')
@login_is_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/show_items')
@login_is_required
def show_items():
    return render_template('show_items.html')


@app.route('/edit_items')
@login_is_required
def edit_items():
    return render_template('edit_items.html')


@app.route('/open_items')
@login_is_required
def open_items():
    return render_template('open_items.html')


@app.route('/save_links')
@login_is_required
def savelinks():
    return render_template('save_links.html')


@app.route('/settings')
@login_is_required
def settings():
    return render_template('settings.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")



#For Testing Purpose. Delete this later. -Saugata

@app.route('/protected_area')
@login_is_required
def protected_area():
    return "<a href = '/logout'>Logout</a> <br> <h4> Hello, your email is {} and <br> your name is {}.<\h4>".format(session['email'], session['name']) #This is just a test. You can delete or use this. -Saugata
#The protected area is not done yet. I will do it later. Let me know the info from the gmail. -Saugata


#For the Input and Ouput in the html general.
"""
@app.route('/yt', methods=['GET', 'POST'])
def yt():
    print("Hello World")
    if req.method == 'POST':
        url = req.form['ytURL']
        if 'transcript' in req.form:
            data = req.get.json('yt_url')
            url = data.get('url')
            transcript_output = transcript(url)['transcript']
            return render_template('summary.html', transcript_area=transcript_output)
            #return redirect(url_for('yt_transcript', yt_url=url))
        elif 'summary' in req.form:
            return redirect(url_for('yt_summarize', yt_url=url))
        else: 
            return render_template('summary.html', transcript_area="Not a POST request!!", summary_area="Not a POST request")
    else:
        return render_template('summary.html', transcript_area="kill me", summary_area="gese atleast")

"""
@app.route('/yt_transcript', methods=['GET', 'POST'])
def yt_transcript():
    if req.method == 'POST':
        requ = req.get_json()
        url = requ.get('yt_url')
        transcript_output = transcript(url)['transcript']
        #print(transcript_output)
        #res = make_response(jsonify({"message": "OK"}), 200)
        #return res
        return jsonify({"transcript": transcript_output}),200
    else:
        return render_template('summary.html', transcript_area="Not a POST request!!")

@app.route('/yt_summarize', methods=['GET', 'POST'])
def yt_summarize():
    if req.method == 'POST':
        requ = req.get_json()
        url = requ.get('yt_url')
        text = transcript(url)['transcript']
        chunks = chunking(text)
        output = ""
        for i, _ in enumerate(chunks):
            temp_out = pegasus(chunks[i])
            output += temp_out
        summary = pegasus(output)
        return jsonify({"summary": summary}),200
    else:
        return render_template('summary.html', summary_area="Not a POST request!!")
    



@app.route("/guestbook")
def guestbook():
    return render_template("summary.html")

@app.route("/guestbook/create", methods=["GET","POST"])
def create_entry():
    requ = req.get.json()
    print(requ)
    res = make_response(jsonify({"message": "OK"}), 200)
    return "Thanks"
    