import requests
import os
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv

def create_short_link(key, long_url):
  url = 'https://api-ssl.bitly.com/v4/bitlinks'
  headers = {'Authorization': 'Bearer {}'.format(key)}
  body = {'long_url': long_url}
  response = requests.post(url, headers=headers, json=body)
  if not response.ok:
    return None
  return response.json()

def get_clicks(key, short_url):
  bitlink = '{}{}'.format(urlparse(short_url).netloc, urlparse(short_url).path)
  headers = {'Authorization': 'Bearer {}'.format(key)}
  payload = {
    'unit': 'day',
    'units': '-1'
  }
  response = requests.get('https://api-ssl.bitly.com/v4/bitlinks/{}/clicks'.format(bitlink), headers=headers, params=payload)
  if not response.ok:
    return None
  return response.json()['link_clicks']

if __name__ == "__main__":
  load_dotenv() 
  key = os.getenv("TOKEN")
  
  parser = argparse.ArgumentParser(description='Доступны следующие функции. Елси введена обычная ссылка, то скрипт выдает сокращенную ссылку. Если введена сокращенная ссылка, то скрипт выдает количество кликов по ссылке')
  parser.add_argument('link', help='Введенная ссылка')
  args = parser.parse_args()
  url = args.link
  
  shorted_link = create_short_link(key, url)
  click_count = 0
  if shorted_link is None:
    click_count = get_clicks(key, url)
    if click_count is None:
      print('Ошибка! Введены не коректные данные.')
    else:
      print('\n\nКоличество кликов по ссылке:\n')
      for item in click_count:
        print(item)
  else:
    print('\n\nКороткая ссылка получена:\n{}'.format(shorted_link['link']))
  
  
