import asyncio
import json
import sys
import os

# Добавляем корневую директорию в путь импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Используем патч с правильным путем к БД вместо стандартного модуля
from scripts.db_patch import new_session, create_tables
from src.models.health_indicators import (
    GeneralInfo,
    LaboratoryInfo,
    AllergiesInfo,
    FamilyHistoryInfo,
    PreventiveInfo,
    LifestyleInfo
)
# Добавляем импорты для медицинских документов
from src.models.medical_documents import (
    DiseasesHistoryDoc,
    AnalyzesDoc,
    RecommendationsDoc,
    OtherDoc
)

def calculate_target_reached(value, min_level, max_level):
    if min_level is None or max_level is None:
        return None
    
    try:
        value_float = float(value)
        return min_level <= value_float <= max_level
    except (ValueError, TypeError):
        return None

async def insert_general_info(session, items):
    for item in items:
        # Convert TypeScript property names to Python model field names
        model = GeneralInfo(
            name=item.get('name'),
            canonical_name=item.get('canonicalName'), 
            value=item.get('value', ''),
            unit=item.get('unit'),
            date=item.get('date'),
            target_level_min=item.get('targetLevelMin'),
            target_level_max=item.get('targetLevelMax')
        )
        
        # Calculate target_reached based on value and target levels
        if model.target_level_min is not None and model.target_level_max is not None:
            model.target_reached = calculate_target_reached(
                model.value, model.target_level_min, model.target_level_max
            )
        
        session.add(model)
    
    await session.commit()
    print(f"Added {len(items)} general health indicators")

async def insert_detailed_info(session, items):
    for item in items:
        try:
            # For DetailedInfo, value must be float
            value = float(item.get('value', 0))
            
            model = LaboratoryInfo(
                name=item.get('name'),
                canonical_name=item.get('canonicalName'),
                value=value,
                unit=item.get('unit'),
                date=item.get('date'),
                target_level_min=item.get('targetLevelMin'),
                target_level_max=item.get('targetLevelMax')
            )
            
            # Calculate target_reached based on value and target levels
            if model.target_level_min is not None and model.target_level_max is not None:
                model.target_reached = calculate_target_reached(
                    model.value, model.target_level_min, model.target_level_max
                )
            
            session.add(model)
        except ValueError:
            print(f"Skipping detailed info with invalid numeric value: {item.get('name')}")
    
    await session.commit()
    print(f"Added {len(items)} detailed health indicators")

async def insert_allergies_info(session, items):
    for item in items:
        model = AllergiesInfo(
            name=item.get('name'),
            canonical_name=item.get('canonicalName'),
            value=item.get('value', '')
        )
        session.add(model)
    
    await session.commit()
    print(f"Added {len(items)} allergy records")

async def insert_family_history_info(session, items):
    for item in items:
        model = FamilyHistoryInfo(
            name=item.get('name'),
            canonical_name=item.get('canonicalName'),
            value=item.get('value', '')
        )
        session.add(model)
    
    await session.commit()
    print(f"Added {len(items)} family history records")

async def insert_preventive_info(session, items):
    for item in items:
        model = PreventiveInfo(
            name=item.get('name'),
            canonical_name=item.get('canonicalName'),
            value=item.get('value', '')
        )
        session.add(model)
    
    await session.commit()
    print(f"Added {len(items)} preventive measure records")

async def insert_lifestyle_info(session, items):
    for item in items:
        model = LifestyleInfo(
            name=item.get('name'),
            canonical_name=item.get('canonicalName'),
            value=item.get('value', '')
        )
        session.add(model)
    
    await session.commit()
    print(f"Added {len(items)} lifestyle records")

# Простые функции для добавления документов
async def insert_diseases_history_docs(session, items):
    for item in items:
        model = DiseasesHistoryDoc(
            name=item.get('name'),
            type=item.get('type'),
            date=item.get('date'),
            icd_code=item.get('icdCode', '')
        )
        session.add(model)
    
    await session.commit()
    print(f"Added {len(items)} disease history documents")

async def insert_analyzes_docs(session, items):
    for item in items:
        model = AnalyzesDoc(
            name=item.get('name'),
            type=item.get('type'),
            date=item.get('date')
        )
        session.add(model)
    
    await session.commit()
    print(f"Added {len(items)} analysis documents")

async def insert_recommendations_docs(session, items):
    for item in items:
        model = RecommendationsDoc(
            name=item.get('name'),
            type=item.get('type'),
            date=item.get('date'),
            specialty=item.get('specialty', '')
        )
        session.add(model)
    
    await session.commit()
    print(f"Added {len(items)} recommendation documents")

async def insert_other_docs(session, items):
    for item in items:
        model = OtherDoc(
            name=item.get('name'),
            type=item.get('type'),
            date=item.get('date')
        )
        session.add(model)
    
    await session.commit()
    print(f"Added {len(items)} other documents")

async def fill_database():
    # Создаем таблицы, используя правильный путь к БД
    print("Инициализация таблиц в базе данных в корне проекта...")
    await create_tables()
    print("Таблицы инициализированы")
    
    # Путь к файлу JSON относительно текущего скрипта
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'dummy.json')
    
    # Read the JSON file with data
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Create a database session
    async with new_session() as session:
        # Insert data into respective tables
        await insert_general_info(session, data['general'])
        await insert_detailed_info(session, data['detailed'])
        await insert_allergies_info(session, data['allergies'])
        await insert_family_history_info(session, data['family_history'])
        await insert_preventive_info(session, data['preventive'])
        await insert_lifestyle_info(session, data['lifestyle'])
        
        # Добавляем медицинские документы
        await insert_diseases_history_docs(session, data['diseases_history'])
        await insert_analyzes_docs(session, data['analyzes'])
        await insert_recommendations_docs(session, data['recommendations'])
        await insert_other_docs(session, data['other_docs'])
    
    print("Database filled successfully!")

if __name__ == "__main__":
    asyncio.run(fill_database()) 
