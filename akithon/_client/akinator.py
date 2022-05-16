from .constants import Constant
from .session import get_session
from .functions import get_server,request
import time

class Akinator:

	current_step = None
	region = None
	uri = None
	url_api_ws = None
	uri_obj = None
	no_uri = None
	no_session = None
	session = None
	progress = None
	child_mode = None
	answers = None
	uid = None
	frontaddr = None
	signature = None
	question = None
	challenge_auth = None
	guess_count = None
	config = None     
 
	def __init__(self, region, child_mode = True):

		if region is None or region not in Constant.REGIONS:
			raise Exception("Please specify a correct region. You can import regions I support or view docs. Then use it like so: new Aki({ region })")

		self.current_step = 0
		self.region = region
		self.uri = None
		self.url_api_ws = None
		self.no_uri = 'Could not find the uri or UrlApiWs. This most likely means that you have not started the game!'
		self.no_session = 'Could not find the game session. Please make sure you have started the game!'
		self.progress = 0.00
		self.guess_count = 0

		self.child_mode = {
			'child_mod': 'true' if child_mode else 'false',
			'soft_constraint': 'ETAT%3D%27EN%27' if child_mode else '',
			'question_filter': 'cat%3D1' if child_mode else ''
		}

		self.question = ''
		self.answers = []

	def start(self):
		server = get_server(self.region)
		
		if server is None:
			raise Exception("Could not find a server matching the region " + self.region)

		self.uri = server['url']
		self.url_api_ws = server['url_ws']
		self.uri_obj = get_session()
		
		if self.uri_obj is None:
			raise Exception("Cannot find the uid and frontaddr")

		self.uid = self.uri_obj['uid']
		self.frontaddr = self.uri_obj['frontaddr']

		timestamp = round(time.time() * 1000)

		url = self.uri + "/new_session?callback=jQuery" + str(timestamp) + "&urlApiWs="+self.url_api_ws+"&partner=1&childMod="+str(self.child_mode['child_mod'])+"&player=website-desktop&uid_ext_session="+self.uid+"&frontaddr="+self.frontaddr+"&constraint=ETAT<>'AV'&soft_constraint="+self.child_mode['soft_constraint']+"&question_filter="+self.child_mode['question_filter']
		result = request(url, 'identification')
		if result:
			self.session = result['identification']['session'];
			self.signature = result['identification']['signature']
			self.question = result['step_information']['question']
			self.challenge_auth = result['identification']['challenge_auth']
			self.answers = [ans['answer'] for ans in result['step_information']['answers']]

	def step(self, answer_id):
		if self.uri is None or self.url_api_ws is None:
			raise Exception(self.no_uri)

		if self.uri_obj is None:
			raise Exception(self.no_session)

		timestamp = round(time.time() * 1000)
		url = self.uri + "/answer_api?callback=jQuery" + str(timestamp) + "&urlApiWs=" + self.url_api_ws + "&childMod="+str(self.child_mode['child_mod'])+"&session="+ self.session + "&signature=" + self.signature + "&step=" + str(self.current_step) + "&answer=" + str(answer_id) + "&frontaddr=" + self.frontaddr + "&question_filter=" + self.child_mode['question_filter']

		result = request(url, 'answers')
		if result:
			self.current_step += 1
			self.progress = float(result['progression'])
			self.question = result['question']
			self.answers = [ans['answer'] for ans in result['answers']]
			print(result)
			print(self.progress)

	def back(self):
		if self.uri is None or self.url_api_ws is None:
			raise Exception(self.no_uri)

		if self.uri_obj is None:
			raise Exception(self.no_session)

		timestamp = round(time.time() * 1000)
		url = self.url_api_ws + "/cancel_answer?callback=jQuery" + str(timestamp) + "&childMod="+str(self.child_mode['child_mod'])+"&session="+ self.session + "&signature=" + self.signature + "&step=" + str(self.current_step) + "&answer=-1&question_filter=" + self.child_mode['question_filter']

		result = request(url, 'answers')
		if result:
			self.current_step -= 1
			self.progress = float(result['progression'])
			self.question = result['question']
			self.answers = [ans['answer'] for ans in result['answers']]

			print(result)
			print(self.progress)
			print(self.answers)

	def win(self):
		if self.uri is None or self.url_api_ws is None:
			raise Exception(self.no_uri)

		if self.uri_obj is None:
			raise Exception(self.no_session)

		timestamp = round(time.time() * 1000)
		temp_child_mode = str(self.child_mode['child_mod']) if self.child_mode['child_mod'] == 'true' else ''
		url = self.url_api_ws + "/list?callback=jQuery" + str(timestamp) + "&childMod="+ temp_child_mode +"&session="+ self.session + "&signature=" + self.signature + "&step=" + str(self.current_step)

		result = request(url, 'elements')
		print(result)
		if result:
			self.guess_count = int(result['NbObjetsPertinents'])
			self.answers = [ans['element'] for ans in result['elements']]
