import requests
import re
from .constants import Constant

def get_session():
	data = requests.get('https://en.akinator.com/game')
	str_data = data.text
	find_reg = re.findall(Constant.PATTERN_SESSION, str_data)
	if len(find_reg) > 0:
		return {
			'uid': find_reg[0][0],
			'frontaddr': find_reg[0][1]
		}

	return None