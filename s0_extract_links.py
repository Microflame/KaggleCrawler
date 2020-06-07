import argparse
import re

from bs4 import BeautifulSoup

def extract(input, output):
  bs = BeautifulSoup(input, features='lxml')
  sc = bs.body.find(text=re.compile('All Competitions')).parent.parent
  for li in sc.find_all('li', attrs={'class': 'mdc-list-item'}):
    href = li.find('a')['href']
    output.write(href + '\n')

if __name__ == '__main__':
  parser = argparse.ArgumentParser('Extract list of competitions from https://www.kaggle.com/competitions')
  parser.add_argument('input', type=argparse.FileType('r'))
  parser.add_argument('output', type=argparse.FileType('w'))
  args = parser.parse_args()
  extract(args.input, args.output)