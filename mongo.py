from pymongo import MongoClient
from enum import Enum
import os, utils

cluster = MongoClient(os.getenv("mongo"))
database = cluster[f"{os.getenv('WordleBot')}"]
recordCollection = database['WordleRecords']
userCollection = database['WordleUsers']

class State(Enum):
  DEFAULT = 0
  ANSWERED = 1
  RECORDED = 2

def insert_wordle_record(ctx, word):
  if recordCollection.find_one({"user_id": ctx.author.id, "date": utils.now().date()}) != None:
    return
  record = {
    "user_id": ctx.author.id, 
    "user_name": ctx.author.name, 
    "guild_id": ctx.guild.id, 
    "guild_name": ctx.guild.name,
    "word": word,
    "date": utils.now().date(),
    "state": State.ANSWERED.value,
    "guesses": None
    }
  recordCollection.insert_one(record)

def record_to_wordle_record(ctx, date):
  record = recordCollection.find_one_and_update({"user_id": ctx.author.id, "date": date}, {"$set": {"state": State.RECORDED.value, ""}})
  return record

def get_all_user_wordle_records(userid):
  record = recordCollection.find({"user_id": userid})
  return record