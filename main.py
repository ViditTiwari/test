import webapp2
import json
import requests
import requests_toolbelt.adapters.appengine
import os

from sqlhelper import DBHelper

from reservation_bot import handle_updates

requests_toolbelt.adapters.appengine.monkeypatch()

def make_requests(update=None):
	if not update:
		text = chat_id = None
	else:
		text = update["message"]["text"]
		chat_id = update["message"]["chat"]["id"]

	my_json = {"text":text, "chat_id": chat_id}
	url = "https://posthere.io/e8e4-49fa-aea4"
	r = requests.post(url, json = my_json)


class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Bot Initialized\n')

		db = DBHelper()
		db.setup()
		cursor = db.conn.cursor()

		cursor.execute('SHOW DATABASES')
		self.response.write('\nDATABASES\n')

		for r in cursor.fetchall():
			self.response.write('{}\n'.format(r))

		cursor.execute('SHOW TABLES')
		self.response.write('\nTABLES\n')

		for r in cursor.fetchall():
			self.response.write('{}\n'.format(r))

		cursor.execute('SELECT * FROM bookings')

		for r in cursor.fetchall():
			self.response.write('{}\n'.format(r))


class WebHookHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write("hey")

	def post(self):
		json_content = json.loads(self.request.body)
		make_requests(json_content)
		handle_updates(json_content)


app = webapp2.WSGIApplication([
	('/', MainPage),
	('/webhook/bot427284879:AAG5eLO4geFp5QpqujEC9SpHiGmZE108Hvs', WebHookHandler),
], debug=True)
