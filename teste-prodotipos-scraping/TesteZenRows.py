# pip install requests
import requests

url = '' # Site a ser feito o scraping
apikey = '' # Chave da API zenrows
params = {
    'url': url,
    'apikey': apikey,
	'js_render': 'true',
	'premium_proxy': 'true',
	'proxy_country': 'br',
    "js_instructions": """[
        {"wait": 3000},
        {"solve_captcha": {"type": "recaptcha"}},
        {"wait": 3000},
        {"click": "#submitBtn"},
        {"wait": 10000}
    ]"""
}
response = requests.get('https://api.zenrows.com/v1/', params=params)
print(response.text)