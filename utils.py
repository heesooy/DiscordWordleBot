from datetime import datetime, date
from pytz import timezone

def get_answer_list():

  answer_list = {}

  with open('./not_bot/answer_list.txt', 'r') as answers:
    for line in answers:
      line = line.strip()
      line = line.split(' ')
      date = datetime.strptime(line[0], "%Y-%m-%d")

      answer_list[date.date()] = line[1]
  
  return answer_list