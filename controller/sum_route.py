from app import app, login_is_required
from flask import render_template, redirect, session, jsonify, url_for, make_response
from flask import request as req
from .yt_transcript import transcript
from .pegasus import pegasus
from .punctuation import punctuation
from .chunking import chunking
from .wikip import wiki_sum, wiki_trans



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
        size = int(requ.get('size'))
        print(size)
        print(url)
        text = transcript(url)['transcript']
        print(len(text))
        chunks = chunking(text)
        output = ""
        for i, _ in enumerate(chunks):
            #punctuated = punctuation(chunk)
            temp_out = pegasus(chunks[i])
            output += temp_out 
            if(len(output)>900):
                output: pegasus(output, size + 15, size - 15)
            print("------------------")
        print("done")
        summary = pegasus(output, size + 15, size - 15)
        summary = summary.replace('<n>', ' ')
        summary = summary.replace(' .', '.')
        return jsonify({"summary": summary}), 200
    else:
        return render_template('summary.html', summary_area="Not a POST request!!")


@app.route('/yt_save', methods=['GET', 'POST'])
def yt_save():
    if req.method == 'POST':
        requ = req.get_json()
        url = requ.get('yt_url')
        summary = requ.get('summary')
        print(url)
        print(summary)
        return render_template('save_links.html', link = url, summary = summary)
    else:
        return render_template('save_links.html', summary_area="Not a POST request!!")


@app.route('/txt_summarize', methods=['GET', 'POST'])
def txt_summarize():
    if req.method == 'POST':
        requ = req.get_json()
        text = requ.get('txtTranscript')
        chunks = chunking(text)
        output = ""
        for i, _ in enumerate(chunks):
            temp_out = pegasus(chunks[i])
            output += temp_out
        summary = pegasus(output)
        return jsonify({"summary": summary}),200
    else:
        return render_template('summary.html', summary_area="Not a POST request!!")    



@app.route('/wiki_summarize', methods=['GET', 'POST'])
def wiki_summarize():
    if req.method == 'POST':
        requ = req.get_json()
        url = requ.get('wiki_url')
        print(url)
        temp = wiki_sum(url)
        summary = pegasus(temp)
        return jsonify({"summary": summary}),200
    else:
        return render_template('summary.html', summary_area="Not a POST request!!")

@app.route('/wiki_transcript', methods=['GET', 'POST'])
def wiki_transcript():
    if req.method == 'POST':
        requ = req.get_json()
        url = requ.get('wiki_url')
        print(url)
        transcript = wiki_trans(url)
        return jsonify({"transcript": transcript}),200
    else:
        print("Not a POST request!!")
        return render_template('summary.html', summary_area="Not a POST request!!")