from typing import List
import os
import tensorflow as tf
import numpy as np
from core.settings import settings, spacy_model
import string

class MLService:
    def __init__(self):
        if not os.path.exists(settings.models_dir):
            os.mkdir(settings.models_dir)
        self.spacy_model = spacy_model
    
    """
    Предварительная обработка текстовых данных
    """
    def __prepare_data(self, X: List[str]) -> List[List[float]]:
        return [[token.vector for token in self.spacy_model(x) \
            if token.lemma_ not in string.punctuation] for x in X]
    
    """
    Построение модели
    """
    def __build_model(self, output_dim: int, learning_rate: float = 0.0005) -> tf.keras.Model:
        input_tokens = tf.keras.layers.Input(name='Input', shape=(None, 300))
        gru = tf.keras.layers.Bidirectional(tf.keras.layers.GRU(32,
                                                                 dropout=0.1,
                                                                 recurrent_dropout=0.1,
                                                                ), name = 'BiGRU')(input_tokens)
        den1 = tf.keras.layers.Dense(32, activation='relu', name = 'DenseHidden1')(gru) 
        den2 = tf.keras.layers.Dense(16, activation="relu", name = 'DenseHidden2')(den1)
        den3 = tf.keras.layers.Dense(output_dim, activation='softmax', name = 'Output')(den2)
        model = tf.keras.Model(input_tokens, den3)
        model.compile(loss='sparse_categorical_crossentropy',
            optimizer=tf.optimizers.Adam(learning_rate=learning_rate))
        return model

    """
    Получение предсказания
    """
    async def predict(self, bot_guid: str, message: str) -> int:
        if os.path.exists(f'{settings.models_dir}/{bot_guid}.h5'):
            model = tf.keras.models.load_model(f'{settings.models_dir}/{bot_guid}.h5')
        else:
            model = self.__build_model(1)
        x = self.__prepare_data([message])[0]
        pred = model.predict(np.array([x]))
        return np.argmax(pred).item()
        
    """
    Обучение модели с нуля (создание нового файлы)
    """
    async def train(self, bot_guid: str, X: List[str], y: List[int], epochs: int = 15) -> None:
        X = self.__prepare_data(X)
        model = self.__build_model(output_dim=np.unique(y).shape[0])
        for _ in range(epochs):
            for i in range(len(X)):
                model.fit(np.array([X[i]]), np.array(y[i]).reshape(1,1))
        model.save(f'{settings.models_dir}/{bot_guid}.h5')

    """
    Шаг обучения
    """
    async def step(self, bot_guid: str, x: str, y: int) -> None:
        x = self.__prepare_data([x])[0]
        model = tf.keras.models.load_model(f'{settings.models_dir}/{bot_guid}.h5')
        model.fit(np.array([x]), np.array(y).reshape(1,1))
    
    """
    Создание дефолтной модели по количеству интентов
    """
    async def create_default_model(self, bot_guid: str, intents_count: int) -> None:
        model = self.__build_model(output_dim=intents_count)
        model.save(f'{settings.models_dir}/{bot_guid}.h5')
