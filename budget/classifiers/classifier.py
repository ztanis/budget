from typing import Dict

import pandas as pd
import numpy as np
import tensorflow as tf
from keras import utils as np_utils
from keras_preprocessing import sequence
from keras_preprocessing.text import Tokenizer
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from budget.context import db
from budget.models.record import Record
import os.path as op
from budget.models.category import Category

class Classifier:
    data_path = op.join(op.dirname(__file__), '../data')

    def estimate(self, df):
        preparation = Preparation()
        filtered = preparation.filter(df)
        train, test = train_test_split(filtered, test_size=0.33, random_state=42)

        preparation.fit(train)
        model = self.build_model(preparation.num_classes)

        train_X, train_y = preparation.transform(train)
        test_X, test_y = preparation.transform(test)

        #for t in train_X:
        #    print(t)
        model.fit(
            train_X,
            train_y,
            epochs=30,
            validation_data=(test_X, test_y)
        )

        train['predicted'] = preparation.inverse_transform_y(model.predict_classes(train_X))
        test['predicted'] = preparation.inverse_transform_y(model.predict_classes(test_X))
        train.to_csv(f"{self.data_path}/train.csv")
        test.to_csv(f"{self.data_path}/test.csv")


    def build_model(self, num_classes):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(512, activation='relu'),
            #tf.keras.layers.Dropout(0.1),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dense(num_classes, activation='softmax')
        ])

        model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['categorical_accuracy'])
        return model

    def load(self):
        return pd.read_sql(
            Record.query.filter(Record.category_id != None).statement,
            db.engine
        )



class Preparation:
    def filter(self, df):
        return df[(df['category_id'] > 0) & (~df['category_id'].isin(self.excluded_category_ids))]

    def __init__(self):
        self.encoder = LabelEncoder()
        self.tk = Tokenizer(num_words=1000, lower=True, split=" ")
        self.num_classes = None
        self.excluded_category_ids = [1, 5, 17]

    @staticmethod
    def clean_name(row):
        words = row.strip('\"')
        words = words.split("//", 1)[0]
        return words.split("End-to-End-Ref", 1)[0]

    def fit(self, df):
        text = df['name'].map(lambda r: self.clean_name(r))
        self.tk.fit_on_texts(text)
        self.encoder.fit(df['category_id'])
        self.num_classes = df['category_id'].nunique()

    def transform(self, df):
        text = df['name'].map(lambda r: self.clean_name(r))
        target = self.encoder.transform(df['category_id'])

        y = np_utils.to_categorical(target, num_classes=self.num_classes)
        text = self.tk.texts_to_sequences(text)
        print(len(self.tk.index_word))
        X = sequence.pad_sequences(text, maxlen=1000)
        return X, y

    def inverse_transform_y(self, y):
        return self.encoder.inverse_transform(y)


classifier = Classifier()
classifier.estimate(classifier.load())
