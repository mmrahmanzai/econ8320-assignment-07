#si-exercise

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import time


def collectLegoSets(url):
  myPage = requests.get(url)
  parsed = BeautifulSoup(myPage.text, 'html.parser')

  articles = parsed.find_all('article')


  data = []
  for a in articles:

    row = []

    #sets/titles
    try:
      row.append(a.h1.text)
    except:
      row.append('')

    #price
    try:
      row.append(float(re.search(r'(\u20AC)(\d+[.]\d{2})', a.find('dt', text="RRP").find_next_sibling().text).groups()[1]))
    except:
      row.append(np.nan)

    #pieces
    try:
      row.append(int(re.search(r'(\d+)', a.find('dt', text="Pieces").find_next_sibling().text).groups()[0]))
    except:
      row.append(np.nan)

    #minifigs
    try:
      row.append(int(re.search(r'(\d+)', a.find('dt', text="Minifigs").find_next_sibling().text).groups()[0]))
    except:
      row.append(np.nan)

    data.append(row)
  newData = pd.DataFrame(data, columns = ['set', 'price_euro', 'pieces', 'minifigs'])

  try:
    nextPage = parsed.find('li', class_="next").a['href']
  except:
    nextPage = None

  if nextPage:
    time.sleep(1)
    return pd.concat([newData, collectLegoSets(nextPage)]).reset_index(drop=True)
  else:
    return newData

lego2019 = collectLegoSets("https://brickset.com/sets/year-2019")

lego2019.to_csv('lego2019.csv', index=False)
