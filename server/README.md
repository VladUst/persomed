# PersoMed — сервер

Бэкенд интеллектуальной персонализированной медицинской информационной системы **PersoMed**.

Сервер хранит цифровой профиль пациента — показатели здоровья и медицинские документы — и анализирует его:

- извлекает медицинские сущности из текста (MedCAT, UMLS);
- предсказывает заболевания по симптомам (ML-модель и онтология);
- выявляет факторы риска;
- подбирает лекарственные препараты;
- формирует сводный статус пациента.

Клиентское приложение находится в соседней папке [`../client`](../client).

## Стек

| Назначение | Технологии |
|---|---|
| Веб-фреймворк | FastAPI, Uvicorn |
| Валидация | Pydantic v2 |
| БД и ORM | SQLite, SQLAlchemy 2.0 (async, `aiosqlite`) |
| Миграции | Alembic |
| NLP | MedCAT (модель UMLS) |
| ML | scikit-learn (MultinomialNB), pandas, numpy |
| Онтология | owlready2, SPARQL по `diseases.owl` |
| Перевод RU↔EN | deep-translator (Google Translate) и встроенный медицинский словарь |
| Генетика (эксперимент) | PyVCF3, MyVariant.info, PGS Catalog |

## Требования

- **Python 3.11.8**, версия закреплена в `.python-version`.
- **Доступ в интернет.** Русские тексты переводятся на английский через Google Translate. Без сети перевод не выполняется, и сервисы получают исходный текст.
- **Модель MedCAT UMLS.** Она не хранится в репозитории (см. ниже). Без неё не работают извлечение сущностей и статус пациента.
- По желанию: Docker.

## Быстрый старт

### 1. Установка зависимостей

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

В `requirements.txt` перечислены и зависимости сервера, и зависимости скриптов анализа генетического профиля.

### 2. Модель MedCAT

Положите пакет модели UMLS в одно из мест:

```
src/services/text_processing/models/umls_small_model/      # распакованная папка
src/services/text_processing/models/umls_small_model.zip   # или архив
```

Папка `models/` указана в `.gitignore`. Модель загружается один раз, при первом запросе к сервису обработки текстов, и эта загрузка занимает заметное время.

### 3. Переменные окружения

Переменные окружения не нужны: сервер не читает ни `.env`, ни `os.environ`. Все настройки заданы в коде:

| Параметр | Где задаётся | Значение |
|---|---|---|
| Строка подключения к БД | `src/database.py`, `alembic.ini` | `sqlite+aiosqlite:///persomed.db` |
| Порт (Docker) | `Dockerfile` | `80` |

Путь к БД относительный, поэтому **все команды запускайте из корня папки `server/`**.

### 4. База данных и миграции

```bash
alembic upgrade head              # создать или обновить схему в persomed.db
python scripts/fill_database.py   # заполнить тестовыми данными (пациент id=1, «Иван Петров»)
```

Работа с миграциями:

```bash
alembic revision --autogenerate -m "описание"   # создать миграцию по изменениям моделей
alembic downgrade -1                             # откатить последнюю миграцию
```

Новую модель нужно импортировать в `src/models/__init__.py`, иначе Alembic её не увидит.

### 5. Запуск dev-сервера

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

После запуска доступны:

- Swagger UI — http://localhost:8000/docs
- ReDoc — http://localhost:8000/redoc

В VS Code можно запустить конфигурацию **Launch Debug** из `.vscode/launch.json`.

### Запуск в Docker

```bash
docker build -t persomed-server .
docker run -p 80:80 persomed-server
```

Внутри контейнера сервер слушает порт **80**. Перед сборкой положите модель MedCAT на своё место (см. шаг 2): `COPY . .` копирует её в образ.

## Структура проекта

```
server/
├── src/
│   ├── main.py              # создание приложения FastAPI
│   ├── database.py          # async-движок, сессии, Base, PRAGMA foreign_keys=ON
│   ├── db_depends.py        # зависимость get_async_db() для роутов
│   ├── api/                 # роутеры FastAPI (по модулю на домен)
│   ├── schemas/             # Pydantic-схемы запросов и ответов
│   ├── repositories/        # доступ к данным, общий BaseRepository[T]
│   ├── models/              # ORM-модели SQLAlchemy
│   └── services/            # бизнес-логика и анализ
│       ├── text_processing/ # MedCAT, извлечение сущностей (singleton)
│       ├── diagnostic/      # ML-модель и онтологический вывод
│       ├── recommendation/  # подбор препаратов по онтологии
│       ├── risk_analysis/   # отклонения показателей, хронические заболевания
│       ├── patient_status/  # сводный статус пациента
│       ├── translate/       # перевод RU↔EN
│       └── ontology/        # diseases.owl
├── migrations/              # миграции Alembic
├── scripts/
│   ├── fill_database.py     # тестовые данные (dummy.json)
│   ├── genes_analysis/      # анализ генетического профиля по VCF (эксперимент)
│   └── pyctd/               # эксперименты с базой CTD
├── alembic.ini
├── Dockerfile
└── requirements.txt
```

Запрос проходит слои **API → Repository → Model → БД**:

- схемы (`schemas/`) валидируют вход и выход;
- сервисы (`services/`) выполняют анализ;
- CRUD-роуты обращаются к репозиториям напрямую.

## Основные эндпоинты

Все пути начинаются с префикса `/api`. Полное описание с примерами есть в Swagger (`/docs`).

### Пациенты

| Метод | Путь | Описание |
|---|---|---|
| GET, POST | `/api/patients/` | Список пациентов, создание пациента |
| GET, PUT, DELETE | `/api/patients/{patient_id}` | Получение, изменение и удаление пациента |

При удалении пациента каскадно удаляются все его данные.

### Показатели здоровья

Базовый путь: `/api/patients/{patient_id}/health-indicators/{тип}`.

| Тип | Описание |
|---|---|
| `general` | Базовая информация |
| `laboratory` | Лабораторные измерения |
| `vaccinations` | Прививки и профилактика |
| `allergies` | Аллергии |
| `family-history` | Семейный анамнез |
| `lifestyle` | Образ жизни |

Для каждого типа есть `GET /` и `POST /` для коллекции, а также `GET`, `PUT` и `DELETE` на `/{id}`. Признак `target_reached` (значение входит в целевой диапазон) сервер вычисляет сам.

### Медицинские документы

Базовый путь: `/api/patients/{patient_id}/medical-documents/{тип}`.

| Тип | Описание |
|---|---|
| `diseases-history` | История болезней и анамнезы |
| `analyzes` | Документы анализов |
| `recommendations` | Рекомендации и назначения врачей |
| `other` | Прочие документы |

Набор CRUD-операций такой же, как у показателей здоровья. У `diseases-history` и `recommendations` дополнительно есть детали документа: `GET`, `POST`, `PUT` и `DELETE` на `/{document_id}/details`.

### Аналитика

| Метод | Путь | Описание |
|---|---|---|
| GET | `/api/patients/{patient_id}/risk-analysis/risk-factors` | Факторы риска: показатели ниже и выше нормы, хронические заболевания |
| GET | `/api/patients/{patient_id}/patient-status/` | Сводный статус: симптомы, заболевания, подозрения, риски, препараты, рекомендации |
| POST | `/api/diagnostic/diseases` | Предсказание заболеваний по списку симптомов (ML и онтология) |
| POST | `/api/recommendations/drugs` | Препараты для лечения заболевания |
| POST | `/api/text-processing/extract-entities` | Извлечение медицинских сущностей из текста |

Примеры тел запросов:

```json
// POST /api/diagnostic/diseases
{ "symptoms": ["кашель", "охриплость", "стридор"] }

// POST /api/recommendations/drugs
{ "disease": "Пневмония" }

// POST /api/text-processing/extract-entities
{ "text": "У пациента наблюдаются покашливание, хриплость и стридор." }
```

Статус пациента опирается на значения поля `type` у документов:

| Значение `type` | Что с ним делает сервер |
|---|---|
| `Анамнез` (история болезней) | Извлекает симптомы из текста анамнеза |
| `хроническое` (история болезней) | Учитывает как хроническое заболевание |
| `Назначения` (рекомендации) | Извлекает препараты |
| `Рекомендации` (рекомендации) | Формирует список рекомендаций |

Блок оценок рисков (`rates`) пока возвращает фиксированные значения-заглушки.

## Анализ генетического профиля (эксперимент)

Это отдельный скрипт, к API он не подключён. Скрипт читает VCF-файл и проходит пять стадий:

1. аннотирует варианты через MyVariant.info (ClinVar, dbSNP, GWAS, CADD);
2. оставляет клинически значимые варианты;
3. применяет правила для комплексных генотипов из `complex_genotypes.yaml` (APOE, Factor V Leiden и др.);
4. считает полигенные шкалы риска по PGS Catalog;
5. выводит отчёт в консоль.

```bash
python scripts/genes_analysis/analysis.py [путь/к/файлу.vcf]
python scripts/genes_analysis/check_pgs_candidates.py   # проверка PGS-скоров на наличие EAF
```
