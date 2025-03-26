from ege_classification.huggingface import HuggingFace
from ege_classification.model import TaskClassifier

model = TaskClassifier()

while True:
    print(model.predict(input("Введите текст: ")))