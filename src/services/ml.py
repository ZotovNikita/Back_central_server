import os
import string
from typing import List
import numpy as np
import tensorflow as tf
from src.core.settings import settings, spacy_model


class MLService:
    def __init__(self):
        if not os.path.exists(settings.models_dir):
            os.makedirs(settings.models_dir)
        self.spacy_model = spacy_model

    async def __prepare_data(self, X: List[str]) -> List[List[float]]:
        """
        Предварительная обработка текстовых данных
        """
        return [[token.vector for token in self.spacy_model(x)
                 if token.lemma_ not in string.punctuation] for x in X]

    async def __build_model(self, output_dim: int, learning_rate: float = 0.0005) -> tf.keras.Model:
        """
        Построение модели
        """
        input_tokens = tf.keras.layers.Input(name='Input', shape=(None, 300))
        gru = tf.keras.layers.Bidirectional(
            tf.keras.layers.GRU(32, dropout=0.1, recurrent_dropout=0.1,),
            name='BiGRU')(input_tokens)
        den1 = tf.keras.layers.Dense(32, activation='relu', name='DenseHidden1')(gru)
        den2 = tf.keras.layers.Dense(16, activation="relu", name='DenseHidden2')(den1)
        den3 = tf.keras.layers.Dense(output_dim, activation='softmax', name='Output')(den2)
        model = tf.keras.Model(input_tokens, den3)

        model.compile(loss='sparse_categorical_crossentropy',
                      optimizer=tf.optimizers.Adam(learning_rate=learning_rate))
        return model

    async def predict(self, bot_guid: str, message: str) -> int:
        """
        Получение предсказания
        """
        if os.path.exists(f'{settings.models_dir}/{bot_guid}.h5'):
            model = tf.keras.models.load_model(f'{settings.models_dir}/{bot_guid}.h5')
        else:
            model = await self.__build_model(1)
        x = (await self.__prepare_data([message]))[0]
        pred = model.predict(np.array([x]))
        return np.argmax(pred).item()

    async def train(self, bot_guid: str, X: List[str], y: List[int], epochs: int = settings.epochs) -> None:
        """
        Обучение модели с нуля (создание нового файла)
        """
        X = await self.__prepare_data(X)
        model = await self.__build_model(output_dim=np.unique(y).shape[0])
        for i in range(len(X)):
            model.fit(np.array([X[i]]), np.array(y[i]).reshape(1, 1), epochs=epochs, verbose=False)
        model.save(f'{settings.models_dir}/{bot_guid}.h5')

    async def step(self, bot_guid: str, x: str, y: int, epochs: int = settings.epochs) -> None:
        """
        Шаг обучения
        """
        x = (await self.__prepare_data([x]))[0]
        model: tf.keras.Model = tf.keras.models.load_model(f'{settings.models_dir}/{bot_guid}.h5')
        model.fit(np.array([x]), np.array(y).reshape(1, 1), epochs=epochs, verbose=False)
        model.save(f'{settings.models_dir}/{bot_guid}.h5')

    async def create_default_model(self, bot_guid: str, intents_count: int) -> None:
        """
        ? Создание дефолтной модели по количеству интентов
        """
        model = await self.__build_model(output_dim=intents_count)
        model.save(f'{settings.models_dir}/{bot_guid}.h5')
