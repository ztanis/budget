import pandas as pd

from budget.context import db
from budget.models.record import Record
from budget.models.category import Category
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import tensorflow_hub as hub



import tensorflow as tf

class Classifier:
    def estimate(self, df):
        filtered = self.filter(df)
        ds = self.preprocess(filtered)

        model = self.build_model()
        train_dataset = ds.shuffle(len(filtered)).batch(1)
        model.fit(train_dataset, epochs=5)

    def build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(6, activation='relu'),
            tf.keras.layers.Dense(16, activation='softmax')
        ])

        model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])
        return model

    def load(self):
        return pd.read_sql(
            Record.query.filter(Record.category_id != None).statement,
            db.engine
        )


    def preprocess_clean_row(self, row):
        words = row.strip('\"')
        words = words.split("//", 1)[0]
        return words.split("End-to-End-Ref", 1)[0]


    def filter(self, df):
        #TODO: add to config
        return df[(df['category_id'] > 0) & (df['category_id'] != 4) & (df['category_id'] != 5)]

    def preprocess(self, data):
        data['name'] = data['name'].map(lambda r: self.preprocess_clean_row(r))
        df = data
        multilabel_binarizer = preprocessing.LabelBinarizer()
        df['category_id'] = multilabel_binarizer.fit_transform(df['category_id'])


        vectorizer = CountVectorizer(min_df=0)
        X_vec = vectorizer.fit_transform(df['name'])
        print("----Res")
        print(X_vec)
        df['name'] = X_vec.toarray()
        return tf.data.Dataset.from_tensor_slices((df['name'].values, df['category_id'].values))

classifier = Classifier()
classifier.estimate(classifier.load())
