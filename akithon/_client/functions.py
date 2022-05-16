import requests
import re
import json

def get_server(region):
	try:
		split = region.split('_');
		language = split[0]
		theme_name = 'characters'
		if len(split) > 1:
			theme_name = split[1]

		url = 'https://'+language+'.akinator.com'
		data = requests.get(url)
		str_data = data.text

		regex = '\[{"translated_theme_name":"[\s\S]*","urlWs":"https:\\\/\\\/srv[0-9]+\.akinator\.com:[0-9]+\\\/ws","subject_id":"[0-9]+"}\]'
		
		find_reg = re.findall(regex, str_data)
		if len(find_reg) > 0:
			list_theme = json.loads(find_reg[0])
			if theme_name != 'characters':
				theme_name = theme_name.capitalize()

			for theme in list_theme:
				if theme['translated_theme_name'] == theme_name:
					return {
						'url': url,
						'url_ws': theme['urlWs']
					}

	except Exception as e:
		print('loi roi')
	return None

def request(url, check_param_property):
	headers = {
	  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
	  'x-requested-with': 'XMLHttpRequest'
	}
	res = requests.get(url, headers=headers)
	#jQuery1652629641011({"completion":"OK","parameters":{"identification":{"channel":0,"session":"409","signature":"1510740159","challenge_auth":"253a63ce-4477-4c54-aa0b-1ebce4306400"},"step_information":{"question":"Is your character real?","answers":[{"answer":"Yes"},{"answer":"No"},{"answer":"Don't know"},{"answer":"Probably"},{"answer":"Probably not"}],"step":"0","progression":"0.00000","questionid":"1549","infogain":"0.612287"}}})
	if res.status_code != 200:
		raise Exception("A problem occurred with making the request.")
	data = res.text
	beginning = data.index('(')
	json_string = data[beginning + 1:len(data) - 1]
	result = json.loads(json_string)

	if check_param_property in result['parameters']:
		return result['parameters']

	return None










