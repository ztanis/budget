import pandas as pd
import tensorflow as tf
from keras import utils as np_utils
from keras_preprocessing import sequence
from keras_preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from budget.context import db
from budget.models.record import Record
import os.path as op
# it is not referenced directly, however it is necessary for loading as Record relation
from budget.models.category import Category


class Classifier:
    def __init__(self):
        self.model = None
        self.preparation = Preparation()

    def train(self, df):
        filtered = self.preparation.filter(df)
        train, test = train_test_split(filtered, test_size=0.33, random_state=42)

        self.preparation.fit(train)
        self.model = self.build_model(self.preparation.num_classes, self.preparation.vocab_size(), self.preparation.max_sequence_length)

        train_X, train_y = self.preparation.transform(train)
        test_X, test_y = self.preparation.transform(test)

        self.model.fit(
            train_X,
            train_y,
            epochs=30,
            validation_data=(test_X, test_y)
        )

        train['predicted'] = self.preparation.inverse_transform_y(self.model.predict_classes(train_X))
        test['predicted'] = self.preparation.inverse_transform_y(self.model.predict_classes(test_X))

    def build_model(self, num_classes, vocab_size, maxlen):
        model = tf.keras.Sequential([
            tf.keras.layers.Embedding(input_dim=vocab_size,
                      output_dim=64,
                      input_length=maxlen),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
            #tf.keras.layers.Dropout(0.1),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(num_classes, activation='softmax')
        ])

        model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['categorical_accuracy'])
        return model

    def load(self):
        records = pd.read_sql(
            Record.query.statement,
            db.engine
        )
        return (
            records[records['category_id'].notnull() & records['is_confirmed']],
            records[records['category_id'].isnull() | ~records['is_confirmed']]
        )

    def estimate(self, df):
        X = self.preparation.transform_features(df)
        return self.preparation.inverse_transform_y(self.model.predict_classes(X))

    def save(self, df):
        for index, row in df.iterrows():
            Record.query.filter_by(id=row['id']).update({
                'category_id': row['predicted'],
                'is_confirmed': False
            })

        db.session.commit()


class Preparation:
    def filter(self, df):
        return df[(df['category_id'] > 0) & (~df['category_id'].isin(self.excluded_category_ids))]

    def __init__(self):
        self.encoder = LabelEncoder()
        self.tk = Tokenizer(lower=True, split=" ")
        self.num_classes = None
        self.excluded_category_ids = []
        self.max_sequence_length = 10

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

    def transform_features(self, df):
        text = df['name'].map(lambda r: self.clean_name(r))
        text = self.tk.texts_to_sequences(text)
        return sequence.pad_sequences(text, padding='post', maxlen=self.max_sequence_length)

    def transform(self, df):
        target = self.encoder.transform(df['category_id'])
        y = np_utils.to_categorical(target, num_classes=self.num_classes)
        return self.transform_features(df), y

    def inverse_transform_y(self, y):
        return self.encoder.inverse_transform(y)

    def vocab_size(self):
        return len(self.tk.word_index) + 1


def classify_unknown():
    classifier = Classifier()
    known, unknown = classifier.load()
    classifier.train(known)

    unknown['predicted'] = classifier.estimate(unknown)
    classifier.save(unknown)
