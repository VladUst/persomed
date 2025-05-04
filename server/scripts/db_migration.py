import sqlite3
import os
import asyncio
from pathlib import Path

# Путь к базе данных (предполагаем, что она в корне проекта)
DB_PATH = Path(__file__).parent.parent / "persomed.db"

async def migrate_diseases_history_doc_details():
    """
    Миграция таблицы diseases_history_doc_details:
    - Изменение колонок clinical_findings, diagnosis, treatment_plan, conclusion 
      для поддержки NULL значений
    """
    if not os.path.exists(DB_PATH):
        print(f"База данных не найдена по пути: {DB_PATH}")
        return False
    
    print(f"Начинаем миграцию базы данных: {DB_PATH}")
    
    # Подключаемся к базе данных
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Получаем данные из существующей таблицы
        cursor.execute("SELECT * FROM diseases_history_doc_details")
        rows = cursor.fetchall()
        
        # Получаем информацию о колонках
        cursor.execute("PRAGMA table_info(diseases_history_doc_details)")
        columns_info = cursor.fetchall()
        column_names = [col[1] for col in columns_info]
        
        # Создаем временную таблицу с теми же колонками, но без NOT NULL ограничений
        # для нужных полей
        create_temp_table_query = """
        CREATE TABLE temp_diseases_history_doc_details (
            id INTEGER PRIMARY KEY,
            document_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            icd_code TEXT NOT NULL,
            diagnosis_date TEXT NOT NULL,
            doctor TEXT NOT NULL,
            specialty TEXT NOT NULL,
            nosology TEXT NOT NULL,
            disease_type TEXT NOT NULL,
            clinic_name TEXT NOT NULL,
            anamnesis TEXT NOT NULL,
            clinical_findings TEXT,
            diagnosis TEXT,
            treatment_plan TEXT,
            conclusion TEXT,
            FOREIGN KEY (document_id) REFERENCES diseases_history_docs(id) ON DELETE CASCADE
        )
        """
        cursor.execute(create_temp_table_query)
        
        # Копируем данные в временную таблицу
        placeholders = ", ".join(["?" for _ in column_names])
        insert_query = f"INSERT INTO temp_diseases_history_doc_details VALUES ({placeholders})"
        for row in rows:
            cursor.execute(insert_query, row)
        
        # Удаляем старую таблицу и переименовываем временную
        cursor.execute("DROP TABLE diseases_history_doc_details")
        cursor.execute("ALTER TABLE temp_diseases_history_doc_details RENAME TO diseases_history_doc_details")
        
        # Фиксируем изменения
        conn.commit()
        print("Миграция успешно выполнена!")
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при выполнении миграции: {e}")
        return False
        
    finally:
        conn.close()

async def main():
    success = await migrate_diseases_history_doc_details()
    if success:
        print("Миграция базы данных успешно завершена")
    else:
        print("Не удалось выполнить миграцию базы данных")

if __name__ == "__main__":
    asyncio.run(main()) 