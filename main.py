from flask import Flask, request
import pymongo
from pymongo import MongoClient, collection
import json
from bson import json_util

client = pymongo.MongoClient("mongodb+srv://test:test@cluster0.uzqnj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.test

db  = client["test"]
collection = db["seeds"]

app = Flask(__name__)


@app.route("/seeds", methods=["GET"])
def get_seeds():
    all_seeds = list(collection.find({}))
    return json.dumps(all_seeds, default=json_util.default)


@app.route("/addseed", methods=["POST"])
def add_seeds():
    request_payload = request.json
    seed = request_payload['seed']
    existing_seed  = collection.find({"_id": seed["name"]})

    if existing_seed.count>0:
        for ex_seed in existing_seed:
            old_count = int(ex_seed["seed_count"])
            addition = int(seed['count'])
            updated_seeds = addition+old_count
        collection.find_one_update({"_id":seed["name"]}, {"$set": {"seed_count": updated_seeds}},upsert=True)
    else:
        collection.insert_one({"_id":seed["name"],"seed_count":seed["count"]})
    return f"Thank you for adding {addition} seeds, the total count of {seed['name']} seeds have now {updated_seeds}!"

@app.route("/buyseed", methods =["POST"])
def buy_seeds():
    request_payload = request.json
    seed = request_payload['seed']
    existing_seed = collection.find({"_id": seed["name"]})
    if existing_seed:
        for ex_seed in existing_seed:
            old_count = int(ex_seed["seed_count"])
            requirement = int(seed['count'])
            if requirement>old_count:
                return f"only {old_count} seeds left you shold buy a lil less."
            else:
                 remaining_seeds = old_count-requirement
                 collection.find_one_and_update({"_id":seed["name"]}, {"$set": {"seed_count":remaining_seeds}},upsert=True)
            return f"Thank you for buing seeds {requirement} seeds, the total count of {seed['name']} seeds is now {remaining_seeds}!"
        else:
            return f"{seed['name']} seed is not in the inverntory. please try buing another"
    if __name__ == "__main__":
        app.run(debug=True, port=5000, host="0..0.0.0")



