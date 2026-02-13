"""
Простой запрос get_chem_gene_interaction_actions по документации PyCTD
"""

import numpy as np

# Фиксы совместимости numpy для разных версий
try:
    # Для numpy < 2.0
    if not hasattr(np, 'unicode'):
        if hasattr(np, 'unicode_'):
            np.unicode = np.unicode_
        else:
            np.unicode = np.str_
    if not hasattr(np, 'float'): np.float = float
    if not hasattr(np, 'int'): np.int = int
    if not hasattr(np, 'bool'): np.bool = bool
except AttributeError:
    # Для numpy >= 2.0
    np.unicode = np.str_
    np.float = float
    np.int = int
    np.bool = bool

import pyctd

def main():
    print("🔬 Настройка PyCTD и выполнение запроса...")
    
    # 1. Настройка соединения с SQLite (как в документации)
    pyctd.set_connection("sqlite:///pyctd.db")
    print("✅ Соединение настроено")
    
    # 2. Создание объекта query (как в примере)
    query = pyctd.query()
    print("✅ Объект query создан")
    
    # 4. Проверка - есть ли данные?
    print("\n🔍 Проверка данных в базе...")
    try:
        # Точно как в документации
        results = query.get_chem_gene_interaction_actions(gene_name='APP', interaction_action='meman%', limit=1)
        
        if results:
            print(f"🎉 Найдено результатов: {len(results)}")
            for r in results:
                print(f"   Химическое вещество: {r.chemical}")
                print(f"   PubMed IDs: {r.pubmed_ids}")
                if hasattr(r.chemical, 'drugbank_ids'):
                    print(f"   DrugBank IDs: {r.chemical.drugbank_ids}")
        else:
            print("⚠️ Данных нет. Нужно выполнить pyctd.update()")
            print("\n📥 Загрузка данных CTD:")
            
            choice = input("Загрузить данные CTD? (~1.5GB, 2 часа) [y/N]: ").lower()
            if choice == 'y':
                try:
                    print("🔄 Загрузка данных CTD...")
                    pyctd.update(force_download=force_download)
                    print("✅ Данные загружены!")
                except Exception as e:
                    print(f"❌ Ошибка загрузки: {e}")
                    import traceback
                    traceback.print_exc()
                    return
            else:
                print("💡 Для загрузки данных выполни: pyctd.update()")
    
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")

if __name__ == "__main__":
    main()
