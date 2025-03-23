from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import new_session
from src.schemas import (
    GeneralInfo, GeneralInfoCreate,
    DetailedInfo, DetailedInfoCreate,
    PreventiveInfo, PreventiveInfoCreate,
    AllergiesInfo, AllergiesInfoCreate,
    FamilyHistoryInfo, FamilyHistoryInfoCreate,
    LifestyleInfo, LifestyleInfoCreate
)
from src.repositories import (
    GeneralInfoRepository,
    DetailedInfoRepository,
    PreventiveInfoRepository,
    AllergiesInfoRepository,
    FamilyHistoryInfoRepository,
    LifestyleInfoRepository
)


async def get_session():
    async with new_session() as session:
        yield session


# Создаем роутер для базовой информации о здоровье
general_router = APIRouter(
    prefix="/general",
    tags=["Общая информация о здоровье"]
)

# Создаем роутер для лабораторных измерений
detailed_router = APIRouter(
    prefix="/detailed",
    tags=["Лабораторные измерения"]
)

# Создаем роутер для прививок и профилактических мероприятий
preventive_router = APIRouter(
    prefix="/preventive",
    tags=["Вакцинации и профилактические мероприятия"]
)

# Создаем роутер для аллергий
allergies_router = APIRouter(
    prefix="/allergies",
    tags=["Аллергии и непереносимости"]
)

# Создаем роутер для семейного анамнеза
family_history_router = APIRouter(
    prefix="/family-history",
    tags=["Семейный анамнез"]
)

# Создаем роутер для образа жизни
lifestyle_router = APIRouter(
    prefix="/lifestyle",
    tags=["Образ жизни"]
)

# Объединяем все роутеры в один общий, сохраняя категоризацию
router = APIRouter(
    prefix="/health-indicators",
)


# General Info endpoints
@general_router.get("/", response_model=List[GeneralInfo], summary="Получить всю базовую информацию о здоровье")
async def get_all_general_info(session: AsyncSession = Depends(get_session)):
    """
    Получение всех записей базовой информации о здоровье.
    
    Возвращает список всех записей базовой информации о здоровье.
    """
    repository = GeneralInfoRepository(session)
    return await repository.get_all()


@general_router.get("/{id}", response_model=GeneralInfo, summary="Получить базовую информацию о здоровье по ID")
async def get_general_info(id: str, session: AsyncSession = Depends(get_session)):
    """
    Получение конкретной записи базовой информации о здоровье по её ID.
    
    - **id**: Уникальный идентификатор записи базовой информации о здоровье
    
    Возвращает запись базовой информации о здоровье, если она найдена, иначе выдает ошибку 404.
    """
    repository = GeneralInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Базовая информация с ID {id} не найдена"
        )
    return item


@general_router.post("/", response_model=GeneralInfo, status_code=status.HTTP_201_CREATED, summary="Создать общий показатель здоровья")
async def create_general_info(
    data: GeneralInfoCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Создание новой записи базовой информации о здоровье.
    
    - **name**: Название показателя
    - **orig_name**: Оригинальное название показателя
    - **value**: Значение показателя
    - **unit**: Единица измерения
    - **date**: Дата измерения
    
    Возвращает созданную запись базовой информации о здоровье с присвоенным ID.
    """
    repository = GeneralInfoRepository(session)
    return await repository.create(data.model_dump())


@general_router.put("/{id}", response_model=GeneralInfo, summary="Обновить базовую информацию о здоровье")
async def update_general_info(id: str, data: GeneralInfoCreate, session: AsyncSession = Depends(get_session)):
    """
    Обновление существующей записи базовой информации о здоровье.
    
    - **id**: Уникальный идентификатор записи для обновления
    - **data**: Обновленные данные
    
    Возвращает обновленную запись базовой информации о здоровье, если она найдена, иначе выдает ошибку 404.
    """
    repository = GeneralInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Базовая информация с ID {id} не найдена"
        )
    return await repository.update(id, data.model_dump())


@general_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить базовую информацию о здоровье")
async def delete_general_info(id: str, session: AsyncSession = Depends(get_session)):
    """
    Удаление записи базовой информации о здоровье.
    
    - **id**: Уникальный идентификатор записи для удаления
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = GeneralInfoRepository(session)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Базовая информация с ID {id} не найдена"
        )


# Detailed Info endpoints
@detailed_router.get("/", response_model=List[DetailedInfo], summary="Получить все лабораторные измерения")
async def get_all_detailed_info(session: AsyncSession = Depends(get_session)):
    """
    Получение всех записей лабораторных измерений.
    
    Возвращает список всех записей лабораторных измерений.
    """
    repository = DetailedInfoRepository(session)
    return await repository.get_all()


@detailed_router.get("/{id}", response_model=DetailedInfo, summary="Получить лабораторное измерение по ID")
async def get_detailed_info(id: str, session: AsyncSession = Depends(get_session)):
    """
    Получение конкретной записи лабораторного измерения по её ID.
    
    - **id**: Уникальный идентификатор лабораторного измерения
    
    Возвращает запись лабораторного измерения, если оно найдено, иначе выдает ошибку 404.
    """
    repository = DetailedInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Лабораторное измерение с ID {id} не найдено"
        )
    return item


@detailed_router.post("/", response_model=DetailedInfo, status_code=status.HTTP_201_CREATED, summary="Создать лабораторное измерение")
async def create_detailed_info(
    data: DetailedInfoCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Создание новой записи лабораторного измерения.
    
    - **name**: Название показателя
    - **orig_name**: Оригинальное название показателя
    - **value**: Числовое значение показателя (float)
    - **unit**: Единица измерения
    - **date**: Дата измерения
    - **target_level_min**: Минимальное целевое значение
    - **target_level_max**: Максимальное целевое значение
    
    Поле target_reached вычисляется автоматически:
    - Если value не указано, target_reached = false
    - Если value находится в диапазоне [target_level_min, target_level_max], target_reached = true
    - В противном случае target_reached = false
    
    Возвращает созданную запись лабораторного измерения с присвоенным ID.
    """
    repository = DetailedInfoRepository(session)
    return await repository.create(data.model_dump())


@detailed_router.put("/{id}", response_model=DetailedInfo, summary="Обновить лабораторное измерение")
async def update_detailed_info(id: str, data: DetailedInfoCreate, session: AsyncSession = Depends(get_session)):
    """
    Обновление существующей записи лабораторного измерения.
    
    - **id**: Уникальный идентификатор записи для обновления
    - **data**: Обновленные данные
    
    Возвращает обновленную запись лабораторного измерения, если она найдена, иначе выдает ошибку 404.
    """
    repository = DetailedInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Лабораторное измерение с ID {id} не найдено"
        )
    return await repository.update(id, data.model_dump())


@detailed_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить лабораторное измерение")
async def delete_detailed_info(id: str, session: AsyncSession = Depends(get_session)):
    """
    Удаление записи лабораторного измерения.
    
    - **id**: Уникальный идентификатор записи для удаления
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = DetailedInfoRepository(session)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Лабораторное измерение с ID {id} не найдено"
        )


# Preventive Info endpoints
@preventive_router.get("/", response_model=List[PreventiveInfo], summary="Получить всю информацию о прививках и профилактике")
async def get_all_preventive_info(session: AsyncSession = Depends(get_session)):
    """
    Получение всех записей о прививках и профилактических мероприятиях.
    
    Возвращает список всех записей о прививках и профилактических мероприятиях.
    """
    repository = PreventiveInfoRepository(session)
    return await repository.get_all()


@preventive_router.get("/{id}", response_model=PreventiveInfo, summary="Получить информацию о прививке по ID")
async def get_preventive_info(id: str, session: AsyncSession = Depends(get_session)):
    """
    Получение конкретной записи о прививке/профилактике по её ID.
    
    - **id**: Уникальный идентификатор записи о прививке/профилактике
    
    Возвращает запись о прививке/профилактике, если она найдена, иначе выдает ошибку 404.
    """
    repository = PreventiveInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Информация о прививке/профилактике с ID {id} не найдена"
        )
    return item


@preventive_router.post("/", response_model=PreventiveInfo, status_code=status.HTTP_201_CREATED, summary="Создать профилактический показатель")
async def create_preventive_info(
    data: PreventiveInfoCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Создание новой записи о прививке или профилактическом мероприятии.
    
    - **name**: Название прививки/мероприятия
    - **orig_name**: Оригинальное название
    - **value**: Статус проведения
    - **unit**: Единица измерения (если применимо)
    - **date**: Дата проведения
    
    Возвращает созданную запись о прививке/профилактике с присвоенным ID.
    """
    repository = PreventiveInfoRepository(session)
    return await repository.create(data.model_dump())


@preventive_router.put("/{id}", response_model=PreventiveInfo, summary="Обновить запись о прививке/профилактике")
async def update_preventive_info(id: str, data: PreventiveInfoCreate, session: AsyncSession = Depends(get_session)):
    """
    Обновление существующей записи о прививке или профилактическом мероприятии.
    
    - **id**: Уникальный идентификатор записи для обновления
    - **data**: Обновленные данные
    
    Возвращает обновленную запись о прививке/профилактике, если она найдена, иначе выдает ошибку 404.
    """
    repository = PreventiveInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Информация о прививке/профилактике с ID {id} не найдена"
        )
    return await repository.update(id, data.model_dump())


@preventive_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить запись о прививке/профилактике")
async def delete_preventive_info(id: str, session: AsyncSession = Depends(get_session)):
    """
    Удаление записи о прививке или профилактическом мероприятии.
    
    - **id**: Уникальный идентификатор записи для удаления
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = PreventiveInfoRepository(session)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Информация о прививке/профилактике с ID {id} не найдена"
        )


# Allergies Info endpoints
@allergies_router.get("/", response_model=List[AllergiesInfo], summary="Получить всю информацию об аллергиях")
async def get_all_allergies_info(session: AsyncSession = Depends(get_session)):
    """
    Получение всех записей об аллергиях.
    
    Возвращает список всех записей об аллергиях.
    """
    repository = AllergiesInfoRepository(session)
    return await repository.get_all()


@allergies_router.get("/{id}", response_model=AllergiesInfo, summary="Получить информацию об аллергии по ID")
async def get_allergies_info(id: str, session: AsyncSession = Depends(get_session)):
    """
    Получение конкретной записи об аллергии по её ID.
    
    - **id**: Уникальный идентификатор записи об аллергии
    
    Возвращает запись об аллергии, если она найдена, иначе выдает ошибку 404.
    """
    repository = AllergiesInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Информация об аллергии с ID {id} не найдена"
        )
    return item


@allergies_router.post("/", response_model=AllergiesInfo, status_code=status.HTTP_201_CREATED, summary="Создать информацию об аллергии")
async def create_allergies_info(
    data: AllergiesInfoCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Создание новой записи об аллергии.
    
    - **name**: Название аллергии
    - **orig_name**: Оригинальное название
    - **value**: Тяжесть реакции
    - **unit**: Единица измерения (если применимо)
    - **date**: Дата выявления
    
    Возвращает созданную запись об аллергии с присвоенным ID.
    """
    repository = AllergiesInfoRepository(session)
    return await repository.create(data.model_dump())


@allergies_router.put("/{id}", response_model=AllergiesInfo, summary="Обновить запись об аллергии")
async def update_allergies_info(id: str, data: AllergiesInfoCreate, session: AsyncSession = Depends(get_session)):
    """
    Обновление существующей записи об аллергии.
    
    - **id**: Уникальный идентификатор записи для обновления
    - **data**: Обновленные данные
    
    Возвращает обновленную запись об аллергии, если она найдена, иначе выдает ошибку 404.
    """
    repository = AllergiesInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Информация об аллергии с ID {id} не найдена"
        )
    return await repository.update(id, data.model_dump())


@allergies_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить запись об аллергии")
async def delete_allergies_info(id: str, session: AsyncSession = Depends(get_session)):
    """
    Удаление записи об аллергии.
    
    - **id**: Уникальный идентификатор записи для удаления
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = AllergiesInfoRepository(session)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Информация об аллергии с ID {id} не найдена"
        )


# Family History Info endpoints
@family_history_router.get("/", response_model=List[FamilyHistoryInfo], summary="Получить всю информацию о семейном анамнезе")
async def get_all_family_history_info(session: AsyncSession = Depends(get_session)):
    """
    Получение всех записей о семейном анамнезе.
    
    Возвращает список всех записей о семейном анамнезе.
    """
    repository = FamilyHistoryInfoRepository(session)
    return await repository.get_all()


@family_history_router.get("/{id}", response_model=FamilyHistoryInfo, summary="Получить информацию о семейном анамнезе по ID")
async def get_family_history_info(id: str, session: AsyncSession = Depends(get_session)):
    """
    Получение конкретной записи о семейном анамнезе по её ID.
    
    - **id**: Уникальный идентификатор записи о семейном анамнезе
    
    Возвращает запись о семейном анамнезе, если она найдена, иначе выдает ошибку 404.
    """
    repository = FamilyHistoryInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Информация о семейном анамнезе с ID {id} не найдена"
        )
    return item


@family_history_router.post("/", response_model=FamilyHistoryInfo, status_code=status.HTTP_201_CREATED, summary="Создать информацию о семейном анамнезе")
async def create_family_history_info(
    data: FamilyHistoryInfoCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Создание новой записи о семейном анамнезе.
    
    - **name**: Название заболевания
    - **orig_name**: Оригинальное название
    - **value**: У кого из родственников
    - **unit**: Единица измерения (если применимо)
    - **date**: Дата добавления информации
    
    Возвращает созданную запись о семейном анамнезе с присвоенным ID.
    """
    repository = FamilyHistoryInfoRepository(session)
    return await repository.create(data.model_dump())


@family_history_router.put("/{id}", response_model=FamilyHistoryInfo, summary="Обновить запись о семейном анамнезе")
async def update_family_history_info(id: str, data: FamilyHistoryInfoCreate, session: AsyncSession = Depends(get_session)):
    """
    Обновление существующей записи о семейном анамнезе.
    
    - **id**: Уникальный идентификатор записи для обновления
    - **data**: Обновленные данные
    
    Возвращает обновленную запись о семейном анамнезе, если она найдена, иначе выдает ошибку 404.
    """
    repository = FamilyHistoryInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Информация о семейном анамнезе с ID {id} не найдена"
        )
    return await repository.update(id, data.model_dump())


@family_history_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить запись о семейном анамнезе")
async def delete_family_history_info(id: str, session: AsyncSession = Depends(get_session)):
    """
    Удаление записи о семейном анамнезе.
    
    - **id**: Уникальный идентификатор записи для удаления
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = FamilyHistoryInfoRepository(session)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Информация о семейном анамнезе с ID {id} не найдена"
        )


# Lifestyle Info endpoints
@lifestyle_router.get("/", response_model=List[LifestyleInfo], summary="Получить всю информацию об образе жизни")
async def get_all_lifestyle_info(session: AsyncSession = Depends(get_session)):
    """
    Получение всех записей об образе жизни.
    
    Возвращает список всех записей об образе жизни.
    """
    repository = LifestyleInfoRepository(session)
    return await repository.get_all()


@lifestyle_router.get("/{id}", response_model=LifestyleInfo, summary="Получить информацию об образе жизни по ID")
async def get_lifestyle_info(id: str, session: AsyncSession = Depends(get_session)):
    """
    Получение конкретной записи об образе жизни по её ID.
    
    - **id**: Уникальный идентификатор записи об образе жизни
    
    Возвращает запись об образе жизни, если она найдена, иначе выдает ошибку 404.
    """
    repository = LifestyleInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Информация об образе жизни с ID {id} не найдена"
        )
    return item


@lifestyle_router.post("/", response_model=LifestyleInfo, status_code=status.HTTP_201_CREATED, summary="Создать информацию об образе жизни")
async def create_lifestyle_info(
    data: LifestyleInfoCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Создание новой записи об образе жизни.
    
    - **name**: Название показателя
    - **orig_name**: Оригинальное название
    - **value**: Значение показателя
    - **unit**: Единица измерения (если применимо)
    - **date**: Дата добавления информации
    
    Возвращает созданную запись об образе жизни с присвоенным ID.
    """
    repository = LifestyleInfoRepository(session)
    return await repository.create(data.model_dump())


@lifestyle_router.put("/{id}", response_model=LifestyleInfo, summary="Обновить запись об образе жизни")
async def update_lifestyle_info(id: str, data: LifestyleInfoCreate, session: AsyncSession = Depends(get_session)):
    """
    Обновление существующей записи об образе жизни.
    
    - **id**: Уникальный идентификатор записи для обновления
    - **data**: Обновленные данные
    
    Возвращает обновленную запись об образе жизни, если она найдена, иначе выдает ошибку 404.
    """
    repository = LifestyleInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Информация об образе жизни с ID {id} не найдена"
        )
    return await repository.update(id, data.model_dump())


@lifestyle_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить запись об образе жизни")
async def delete_lifestyle_info(id: str, session: AsyncSession = Depends(get_session)):
    """
    Удаление записи об образе жизни.
    
    - **id**: Уникальный идентификатор записи для удаления
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = LifestyleInfoRepository(session)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Информация об образе жизни с ID {id} не найдена"
        )

# Включаем все роутеры в основной роутер
router.include_router(general_router)
router.include_router(detailed_router)
router.include_router(preventive_router)
router.include_router(allergies_router)
router.include_router(family_history_router)
router.include_router(lifestyle_router) 