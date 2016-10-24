from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient


app = Flask(__name__)


client = MongoClient()
db = client.newDB


@app.route('/')
@app.route('/members/', methods=['POST', 'GET'])
def members():

	#register
	if request.method == 'POST':
		m_list = db.member_list
		existing_member = m_list.find_one({'first_name': request.form['first_name']})

		if existing_member is None:
			m_list.insert({'first_name': request.form['first_name'], 'last_name': request.form['last_name']})
			return redirect(url_for('members'))
	
		return 'Member already registered.'

	#members
	cursor = db.member_list.find()
	m_list = []
	for item in cursor:
		m_list.append(item['first_name'] + ' ' + item['last_name'])

	return render_template("members.html", m_list=m_list, item=item)


if __name__ == '__main__':
    app.run(debug=True)
