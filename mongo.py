from ast import Num
from pymongo import MongoClient
from enum import Enum
import os, utils

cluster = MongoClient(os.getenv("MONGO"))
database = cluster['WordleBot']
recordCollection = database['WordleRecords']
userCollection = database['WordleUsers']

class State(Enum):
  DEFAULT = 0
  ANSWERED = 1
  RECORDED = 2

def insert_wordle_record(ctx, answer):
  if recordCollection.find_one({"user_id": ctx.author.id, "date": str(utils.now().date())}) != None:
    return
  record = {
    "user_id": ctx.author.id, 
    "user_name": ctx.author.name, 
    "guild_id": ctx.guild.id, 
    "guild_name": ctx.guild.name,
    "word": answer[0],
    "wordle_num": answer[1],
    "date": str(utils.now().date()),
    "state": State.ANSWERED.value,
    "trinary": None,
    "num_guesses": None,
    }
  recordCollection.insert_one(record)

def record_to_wordle_record(ctx, tri, num, date):
  record = recordCollection.find_one_and_update({"user_id": ctx.author.id, "date": str(date), "state": State.ANSWERED.value}, {
    "$set": {
      "state": State.RECORDED.value, 
      "trinary": tri, 
      "num_guesses": num
      }})
  return record

def get_all_user_wordle_records(userid):
  query = {"user_id": userid, "state": State.RECORDED.value}
  if recordCollection.count_documents(query) == 0:
    return None
  records = recordCollection.find(query)
  return records

def get_average_num_guesses(user):
  records = get_all_user_wordle_records(user.id)
  if records == None:
    return None
  sum = 0
  count = 0
  for record in records:
    sum += record["num_guesses"]
    count += 1
  return sum / count