import argparse
import json

import jsonlines


def extract(input, output):
  output.write('Url\tCompetitionId\tDiscussionId\n')
  with jsonlines.Reader(input) as reader:
    for obj in reader:
      url = obj['url']
      comp_json = json.loads(obj['json'])
      competitionId = comp_json['competitionId']
      discussion = comp_json['discussion']
      if discussion:
        discussionId = discussion['id']
      else:
        print('No discussion for ' + url)
        discussionId = -1
      output.write('%s\t%d\t%d\n' % (url, competitionId, discussionId))

if __name__ == '__main__':
  parser = argparse.ArgumentParser('Extract kernel ids')
  parser.add_argument('input', type=argparse.FileType('r'))
  parser.add_argument('output', type=argparse.FileType('w'))
  args = parser.parse_args()
  extract(args.input, args.output)