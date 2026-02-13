import numpy as np

if not hasattr(np, 'unicode'): np.unicode = np.str_
if not hasattr(np, 'float'): np.float = float
if not hasattr(np, 'int'): np.int = int
if not hasattr(np, 'bool'): np.bool = bool

import pyctd
from sqlalchemy import text

pyctd.set_connection("sqlite:///pyctd.db")
query = pyctd.query()

chemical_count = query.session.execute(text("SELECT COUNT(*) FROM pyctd_chemical")).fetchone()[0]
gene_count = query.session.execute(text("SELECT COUNT(*) FROM pyctd_gene")).fetchone()[0]
disease_count = query.session.execute(text("SELECT COUNT(*) FROM pyctd_disease")).fetchone()[0]
interaction_count = query.session.execute(text("SELECT COUNT(*) FROM pyctd_chem_gene_ixn")).fetchone()[0]

print(f"📊 Химических веществ: {chemical_count:,}")
print(f"📊 Генов: {gene_count:,}")
print(f"📊 Заболеваний: {disease_count:,}")
print(f"📊 Взаимодействий: {interaction_count:,}")

# 1. Поиск конкретного химического вещества
""" try:
    chemicals = query.get_chemical('Memantine')
    print(f"1. Химическое вещество Memantine: {len(chemicals)} найдено")
    if chemicals:
        c = chemicals[0]
        print(f"   {c.chemical_name} ({c.chemical_id})")
        print(f"   CAS: {c.cas_rn}")
    else:
        print("   Не найдено")
except Exception as e:
    print(f"1. Ошибка поиска химического вещества: {e}")

# 2. Поиск гена
try:
    gene = query.get_gene('APP')
    print(f"2. Ген APP:")
    if gene:
        print(f"   {gene.gene_name} ({gene.gene_symbol})")
    else:
        print("   Не найдено")
except Exception as e:
    print(f"2. Ошибка поиска гена: {e}")

# 3. Поиск заболевания
try:
    disease = query.get_disease('MESH:D000544')
    print(f"3. Заболевание MESH:D000544:")
    if disease:
        print(f"   {disease.disease_name} ({disease.disease_id})")
    else:
        print("   Не найдено")
except Exception as e:
    print(f"3. Ошибка поиска заболевания: {e}")

# 4. Связи химическое вещество-заболевание
try:
    chem_diseases = query.get_chemical_diseases(limit=5)
    print(f"4. Связи химическое вещество-заболевание: {len(chem_diseases)}")
    for cd in chem_diseases[:3]:
        print(f"   {cd.chemical} -> {cd.disease}")
except Exception as e:
    print(f"4. Ошибка поиска связей химическое вещество-заболевание: {e}")

# 5. Связи ген-заболевание
try:
    gene_disease = query.get_gene_disease(limit=5)
    print(f"5. Связи ген-заболевание: {len(gene_disease)}")
    for gd in gene_disease[:3]:
        print(f"   {gd.gene} -> {gd.disease}")
except Exception as e:
    print(f"5. Ошибка поиска связей ген-заболевание: {e}")

# 6. Поиск путей (pathways)
try:
    pathway = query.get_pathway('hsa04010')
    print(f"6. Pathway hsa04010:")
    if pathway:
        print(f"   {pathway.pathway_name} ({pathway.pathway_id})")
    else:
        print("   Не найдено")
except Exception as e:
    print(f"6. Ошибка поиска pathway: {e}")

# 7. Взаимодействия химическое вещество-ген
try:
    interactions = query.get_chem_gene_interaction_actions(limit=5)
    print(f"7. Взаимодействия химическое вещество-ген: {len(interactions)}")
    for i in interactions[:3]:
        print(f"   {i.chemical} -> {i.gene}")
except Exception as e:
    print(f"7. Ошибка поиска взаимодействий: {e}")

# 8. Поиск химических веществ по заболеванию
try:
    chems_by_disease = query.get_chemical__by__disease('Alzheimer Disease')
    print(f"8. Химические вещества для Alzheimer Disease: {len(chems_by_disease)}")
    for cbd in chems_by_disease[:100]:
        print(f"   {cbd.chemical}")
except Exception as e:
    print(f"8. Ошибка поиска химических веществ по заболеванию: {e}") """

print("\n🔍 Поиск маркерных связей для APOE:")

# 1. Сначала проверим структуру таблицы gene__disease
print("\n1. Структура таблицы pyctd_gene__disease:")
try:
    columns = query.session.execute(text("PRAGMA table_info(pyctd_gene__disease)")).fetchall()
    print("   Колонки в таблице:")
    for col in columns:
        print(f"     {col[1]} ({col[2]})")
except Exception as e:
    print(f"   Ошибка: {e}")

# 2. Проверим есть ли поле для типа связи
print("\n2. Образец данных из таблицы:")
try:
    sample_data = query.session.execute(text("SELECT * FROM pyctd_gene__disease LIMIT 3")).fetchall()
    for row in sample_data:
        print(f"   {row}")
except Exception as e:
    print(f"   Ошибка: {e}")

# 3. Уникальные заболевания для APOE (без дубликатов)
print("\n3. Уникальные заболевания для APOE (gene_symbol):")
try:
    # Получаем все связи APOE
    apoe_diseases_all = query.get_gene_disease(gene_symbol='APOE', limit=1000)
    
    # Создаем словарь уникальных заболеваний
    unique_diseases = {}
    for gd in apoe_diseases_all:
        disease_name = gd.disease.disease_name
        if disease_name not in unique_diseases:
            unique_diseases[disease_name] = {
                'disease': gd.disease,
                'evidence': getattr(gd, 'direct_evidence', 'N/A'),
                'pubmed_count': len(gd.pubmed_ids) if gd.pubmed_ids else 0
            }
    
    print(f"   APOE связан с {len(unique_diseases)} уникальными заболеваниями:")
    
    # Сортируем по количеству PubMed статей (больше статей = более изученная связь)
    sorted_diseases = sorted(unique_diseases.items(), 
                           key=lambda x: x[1]['pubmed_count'], reverse=True)
    
    for i, (disease_name, info) in enumerate(sorted_diseases[:15]):
        print(f"     {i+1}. {disease_name}")
        print(f"        Доказательства: {info['evidence']}")
        print(f"        PubMed статей: {info['pubmed_count']}")
        
except Exception as e:
    print(f"   Ошибка: {e}")

# 4. Поиск конкретно болезни Альцгеймера
print("\n4. Фильтр по Alzheimer/нейродегенеративным заболеваниям:")
try:
    alzheimer_related = []
    neurological_keywords = ['alzheimer', 'dementia', 'cognitive', 'brain', 'neural', 'neuro']
    
    for disease_name, info in unique_diseases.items():
        for keyword in neurological_keywords:
            if keyword.lower() in disease_name.lower():
                alzheimer_related.append((disease_name, info))
                break
    
    # Сортируем по количеству статей
    alzheimer_related.sort(key=lambda x: x[1]['pubmed_count'], reverse=True)
    
    print(f"   Найдено {len(alzheimer_related)} нейродегенеративных заболеваний:")
    for disease_name, info in alzheimer_related[:10]:
        print(f"     ✓ {disease_name} ({info['pubmed_count']} статей)")
        
except Exception as e:
    print(f"   Ошибка: {e}")

# 5. Проверяем есть ли прямая информация о типе связи в базе
print("\n5. Поиск маркерной информации через SQL:")
try:
    # Ищем таблицы которые могут содержать информацию о типе связи
    marker_tables = query.session.execute(text("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND (
            name LIKE '%marker%' OR 
            name LIKE '%biomarker%' OR
            name LIKE '%evidence%'
        )
    """)).fetchall()
    
    print(f"   Таблицы с маркерной информацией: {[t[0] for t in marker_tables]}")
    
    # Проверяем есть ли поле inference_score или similar
    gene_disease_columns = query.session.execute(text("PRAGMA table_info(pyctd_gene__disease)")).fetchall()
    relevant_columns = [col[1] for col in gene_disease_columns if any(keyword in col[1].lower() 
                       for keyword in ['score', 'evidence', 'marker', 'inference', 'direction'])]
    
    print(f"   Релевантные колонки: {relevant_columns}")
    
except Exception as e:
    print(f"   Ошибка: {e}")

# 6. Альтернатива - используем метод get_marker_chemical__by__disease_name
print("\n6. Проверка обратной связи - маркеры для Alzheimer Disease:")
try:
    alzheimer_markers = query.get_marker_chemical__by__disease_name('Alzheimer Disease')
    print(f"   Химических маркеров для Alzheimer Disease: {len(alzheimer_markers)}")
    
    for marker in alzheimer_markers[:5]:
        print(f"     Маркер: {marker.chemical.chemical_name}")
        
    # Проверим есть ли аналогичный метод для генов
    print("\n   Проверка методов для генетических маркеров:")
    methods = [method for method in dir(query) if 'marker' in method.lower() and 'gene' in method.lower()]
    print(f"   Методы с 'marker' и 'gene': {methods}")
    
except Exception as e:
    print(f"   Ошибка: {e}")

print("\n✅ Анализ маркерных связей завершен!")