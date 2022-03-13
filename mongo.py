from ast import Num
from pymongo import MongoClient
from enum import Enum
import os, utils

cluster = MongoClient(os.getenv("MONGO"))
database = cluster["WordleBot"]
recordCollection = database["WordleRecords"]
userCollection = database["WordleUsers"]


class State(Enum):
    DEFAULT = 0
    ANSWERED = 1
    RECORDED = 2


def insert_wordle_record(guild, answer, tri, num, date, user):
    if recordCollection.find_one({"user_id": user.id, "date": str(date)}) is not None:
        return None
    record = {
        "user_id": user.id,
        "user_name": user.name,
        "guild_id": guild.id,
        "guild_name": guild.name,
        "word": answer[1],
        "wordle_num": answer[2],
        "date": str(answer[0]),
        "state": State.RECORDED.value,
        "trinary": tri,
        "num_guesses": num,
    }
    return recordCollection.insert_one(record)


def get_user_list(guild):
    return recordCollection.distinct("user_id", {"guild_id": guild.id})


def get_answer_count(user_id):
    query = {"user_id": user_id, "state": State.RECORDED.value}
    return recordCollection.count_documents(query)


def get_all_user_wordle_records(user_id):
    query = {"user_id": user_id, "state": State.RECORDED.value}
    if recordCollection.count_documents(query) == 0:
        return None
    return recordCollection.find(query)


def get_average_num_guesses(user_id):
    records = get_all_user_wordle_records(user_id)
    if records is None:
        return None
    total = sum(record["num_guesses"] for record in records)
    return total / len(records)
