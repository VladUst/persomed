export interface HealthMeasurementData {
    id: string;
    canonicalName?: string;
    name: string;
    value?: string;
    unit?: string;
    date?: string;
    targetReached?: boolean;
    targetLevelMin?: number;
    targetLevelMax?: number;
}

const general: HealthMeasurementData[] = [
    {
        id: '1',
        canonicalName: 'age',
        name: 'Возраст',
        value: '30',
    },
    {
        id: '2',
        canonicalName: 'gender',
        name: 'Пол',
        value: 'Мужской',
    },
    {
        id: '3',
        canonicalName: 'birthdate',
        name: 'Дата рождения',
        value: '27.07.1994',
    },
    {
        id: '4',
        canonicalName: 'height',
        name: 'Рост',
        value: '170',
        unit: 'см',
        date: '10-20-2024',
    },
    {
        id: '5',
        canonicalName: 'weight',
        name: 'Вес',
        value: '60',
        unit: 'кг',
        date: '10-20-2024',
    },
    {
        id: '6',
        canonicalName: 'BMI',
        name: 'ИМТ',
        value: '24.2',
        unit: 'кг/м^3',
        date: '10-20-2024',
    },
    {
        id: '7',
        canonicalName: 'temperature',
        name: 'Температура',
        value: '36',
        unit: '°C',
        date: '10-20-2024',
    },
    {
        id: '8',
        canonicalName: 'systolic_pressure',
        name: 'Систолическое АД',
        value: '160',
        unit: 'мм рт.ст.',
        date: '10-20-2024',
        targetLevelMin: 120,
        targetLevelMax: 140,
    },
    {
        id: '9',
        canonicalName: 'diastolic_pressure',
        name: 'Диастолическое АД',
        value: '100',
        unit: 'мм рт.ст.',
        date: '10-20-2024',
        targetLevelMin: 80,
        targetLevelMax: 90,
    },
    {
        id: '10',
        canonicalName: 'heart_rate',
        name: 'ЧСС',
        value: '90',
        unit: 'уд/мин',
        date: '10-20-2024',
        targetLevelMin: 60,
        targetLevelMax: 80,
    },
    {
        id: '11',
        canonicalName: 'respiratory_rate',
        name: 'Частота дыхания',
        value: '30',
        unit: 'число/мин',
        date: '10-20-2024',
    },
];

const detailed: HealthMeasurementData[] = [
    {
        id: '1',
        canonicalName: 'glucose',
        name: 'Глюкоза',
        value: '7.5',
        unit: 'ммоль/л',
        date: '10-20-2024',
        targetLevelMin: 3.9,
        targetLevelMax: 5.6,
    },
    {
        id: '2',
        canonicalName: 'potassium',
        name: 'Калий',
        value: '3.0',
        unit: 'ммоль/л',
        date: '10-20-2024',
        targetLevelMin: 3.5,
        targetLevelMax: 5.1,
    },
    {
        id: '3',
        canonicalName: 'vitamin_d',
        name: 'Витамин D',
        value: '38',
        unit: 'нг/мл',
        date: '10-20-2024',
        targetLevelMin: 20,
        targetLevelMax: 50,
    },
    {
        id: '4',
        canonicalName: 'SpO2',
        name: 'SpO2',
        value: '98',
        unit: '%',
        date: '10-20-2024',
        targetLevelMin: 95,
        targetLevelMax: 100,
    },
];

const allergies: HealthMeasurementData[] = [
    {
        id: '1',
        name: 'Антибиотики (пенициллины)',
        value: 'Крапивница и кожный зуд',
    },
    {
        id: '2',
        name: 'Нестероидные противовоспалительные средства (ибупрофен)',
        value: 'Отек и затрудненное дыхание',
    },
    {
        id: '3',
        name: 'Ингаляционные аллергены',
        value: 'Сезонные аллергии на цветение (пыльца амброзии)',
    },
    {
        id: '4',
        name: 'Пищевые аллергены',
        value: 'Морепродукты: кожный зуд',
    },
];

const family_history: HealthMeasurementData[] = [
    {
        id: '1',
        name: 'Антибиотики (пенициллины)',
        value: 'Крапивница и кожный зуд',
    },
    {
        id: '2',
        name: 'Нестероидные противовоспалительные средства (ибупрофен)',
        value: 'Отек и затрудненное дыхание',
    },
    {
        id: '3',
        name: 'Ингаляционные аллергены',
        value: 'Сезонные аллергии на цветение (пыльца амброзии)',
    },
    {
        id: '4',
        name: 'Пищевые аллергены',
        value: 'Морепродукты: кожный зуд',
    },
];

const preventive: HealthMeasurementData[] = [
    {
        id: '1',
        name: 'Противогриппозная вакцина',
        value: 'Последняя прививка — октябрь 2023',
    },
    {
        id: '2',
        name: 'Прививка от COVID-19',
        value: 'Полный курс, февраль 2021',
    },
    {
        id: '3',
        name: 'Вакцинация от гепатита B',
        value: 'Привит в детстве, ревакцинация не требовалась',
    },
    {
        id: '4',
        name: 'Флюорография',
        value: 'Последнее обследование — март 2024, без патологий',
    },
    {
        id: '5',
        name: 'ЭКГ и УЗИ сердца',
        value: 'Последнее обследование — январь 2024, выявлена сердечная недостаточность',
    },
];

const lifestyle: HealthMeasurementData[] = [
    {
        id: '1',
        name: 'Курение',
        value: 'Курит с 20 лет, около 10 сигарет в день',
    },
    {
        id: '2',
        name: 'Употребление алкоголя',
        value: 'Редкое, 1-2 раза в месяц, умеренные дозы',
    },
    {
        id: '3',
        name: 'Физическая активность',
        value: 'Минимальная, прогулки 2-3 раза в неделю по 30 минут',
    },
    {
        id: '4',
        name: 'Режим сна',
        value: 'Нарушен, средняя продолжительность сна 5-6 часов',
    },
    {
        id: '5',
        name: 'Питание',
        value: 'Преобладание жирной пищи, недостаточное количество овощей и фруктов',
    },
];
