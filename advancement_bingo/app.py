import os
import json
import tempfile
from zipper import generate_zip, generate_random_zip
from advancement_parser import advancements
from flask import Flask, current_app, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/api/advancements')
def get_advancements():
	return json.dumps(advancements)

@app.route('/generate/random')
def generate_random():
	def stream_and_remove_file():
		with tempfile.SpooledTemporaryFile() as fp:
			generate_random_zip(fp)
			fp.seek(0)
			yield from fp

	return current_app.response_class(
		stream_and_remove_file(),
		headers={'Content-Disposition': 'attachment', 'filename': 'hunt.zip'},
		mimetype='application/zip'
	)

@app.route('/generate/custom')
def generate_custom():
	selected_advancements = json.loads(request.args.get('selected'))
	print(selected_advancements)

	def stream_and_remove_file():
		with tempfile.SpooledTemporaryFile() as fp:
			generate_zip(fp, selected_advancements)
			fp.seek(0)
			yield from fp

	return current_app.response_class(
		stream_and_remove_file(),
		headers={'Content-Disposition': 'attachment', 'filename': 'hunt.zip'},
		mimetype='application/zip'
	)

if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))