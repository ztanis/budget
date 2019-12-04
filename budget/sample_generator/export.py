import itertools
import random
import string

import pandas as pd
from budget.context import db
from budget.models.record import Record
import re
import uuid
from budget.models.category import Category

records = pd.read_sql(
    Record.query.filter(Record.category_id.in_((1, 8, 9, 12))).statement,
    db.engine
)

print(records)
names = records['name'].tolist()
category_ids = records['category_id'].tolist()
print('bla')

name_words = [
    re.findall(r"[\w']+", name)
    for name in names]

words = list(itertools.chain(*name_words))
print(words)

def random_str():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))

dictionary = { w: random_str() for w in words }

anonymised = []
for i, ws in name_words:
    name = [dictionary[w] for w in ws]
    record = {
        "name": name,
        "category_id": category_ids[i]
    }
    anonymised.append(" ".join(aw))

import json
#with open('data.json', 'w') as f:
#    json.dump(data, f)

