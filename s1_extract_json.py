import argparse

import slimit
from slimit.parser import Parser as JsParser
from slimit.visitors import nodevisitor as jsnodevisitor
import jsonlines
from bs4 import BeautifulSoup

js_parser = JsParser()
prefix = 'Kaggle.State.push('
def get_competition_json(js_code):
  tree = js_parser.parse(js_code)

  for node in jsnodevisitor.visit(tree):
    if isinstance(node, slimit.ast.FunctionCall):
      ecma = node.to_ecma()
      if ecma.startswith(prefix):
        return ecma[len(prefix):-1]

def get_js_code_with_data_json(body):
  bs = BeautifulSoup(body, features='lxml').body
  x = bs.find('div', attrs={'id': 'site-body'})
  x = x.find('script')
  return x.text

def extract(input, output):
  with jsonlines.Reader(input) as reader, jsonlines.Writer(output) as writer:
    for obj in reader:
      js_code = get_js_code_with_data_json(obj['body'])
      json = get_competition_json(js_code)
      writer.write({'url': obj['url'], 'json': json})

if __name__ == '__main__':
  parser = argparse.ArgumentParser('Extract jsons from competition htmls')
  parser.add_argument('input', type=argparse.FileType('r'))
  parser.add_argument('output', type=argparse.FileType('w'))
  args = parser.parse_args()
  extract(args.input, args.output)