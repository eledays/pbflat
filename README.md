## Запуск

1. Создайте виртуальное окружение:

```bash
python3 -m venv venv
```

2. Активируйте виртуальное окружение:

```bash
source venv/bin/activate
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Заполните файл .env согласно образцу `.env.example`

## Настройка навыка

1. Переходим в [Консоль Яндекс Диалогов](https://dialogs.yandex.ru/developer)
2. На вкладке [Умный дом](https://dialogs.yandex.ru/developer/smart-home) выбираем "Создать навык умного дома" 


## Схема работы 

### 1. Авторизация

1. Когда пользователь в приложении УДЯ (умный дом Яндекса) нажимает кнопку "Подключить устройства", Яндекс перенаправляет его на `API authorization endpoint`, указанный в настройках навыка: `example.com/authorize`

