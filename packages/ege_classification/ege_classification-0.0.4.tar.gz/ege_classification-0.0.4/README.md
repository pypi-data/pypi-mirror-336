
# EGE Classification

Этот проект предназначен для классификации задач из профильного ЕГЭ по математике. Модель предсказывает номер задачи с точностью 98.6%.

## Установка

Вы можете самостоятельно собрать библиотеку

```bash
poetry build
pip install ПУТЬ_К_АРХИВУ
```

Или воспользоваться pypi.org

```bash
pip install ege-classification
```

## Использование

### Обучение модели

Для обучения модели используйте следующий код:

```python
from ege_classification.model import TaskClassifier

classifier = TaskClassifier()
classifier.train('path/to/dataset.csv')
classifier.save()
```

### Тестирование модели

Для тестирования модели используйте следующий код:

```python
classifier.test('path/to/dataset.csv')
```

### Предсказание

Для предсказания номера задачи используйте следующий код:

```python
predicted_class = classifier.predict("Текст задачи")
print(f"Предсказанный номер задачи: {predicted_class}")
```

### Загрузка и сохранение модели

Для сохранения модели:

```python
classifier.save('path/to/save/model')
```

Для загрузки модели:

```python
classifier.load('path/to/saved/model')
```


## Лицензия

Этот проект лицензирован под лицензией MIT.
