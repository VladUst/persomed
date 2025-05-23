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

const diseasesHistoruDocs = [
    {
        id: '1',
        icdCode: '-',
        name: 'Подозрение на диабет',
        type: 'Анамнез',
        date: '2024-07-17',
    },
    {
        id: '2',
        icdCode: 'J00-J02',
        name: 'ОРВИ',
        type: 'Обычное',
        date: '2024-02-09',
    },
    {
        id: '3',
        icdCode: 'I11',
        name: 'Артериальная гипертензия',
        type: 'Хроническое',
        date: '2023-01-15',
    },
    {
        id: '4',
        icdCode: 'I50.9',
        name: 'Сердечная недостаточность',
        type: 'Хроническое',
        date: '2023-02-10',
    },
];

const analyzesDocs = [
    {
        id: '1',
        name: 'Общий анализ крови',
        type: 'Лабораторный',
        date: '2024-01-15',
    },
    {
        id: '2',
        name: 'Биохимический анализ крови',
        type: 'Лабораторный',
        date: '2024-01-20',
    },
    { id: '3', name: 'ЭКГ', type: 'Диагностический', date: '2024-02-01' },
    {
        id: '4',
        name: 'УЗИ сердца',
        type: 'Диагностический',
        date: '2024-02-10',
    },
];

const recommendationsDocs = [
    {
        id: '1',
        name: 'Рекомендации по лечению ОРВИ',
        type: 'Рекомендации',
        specialty: 'Терапевт',
        date: '2024-03-01',
    },
    {
        id: '2',
        name: 'Препараты для лечения гипертензии',
        type: 'Препараты',
        specialty: 'Кардиолог',
        date: '2024-03-05',
    },
];

const otherDocs = [
    {
        id: '1',
        name: 'Генетический профиль',
        type: 'Генетика',
        date: '2023-12-01',
    },
    {
        id: '2',
        name: 'Справка о госпитализации',
        type: 'Справка',
        date: '2023-11-15',
    },
    {
        id: '3',
        name: 'Выписка из стационара',
        type: 'Выписка',
        date: '2024-01-20',
    },
];

interface HistoryDocumentDetails {
    title: string;
    meta: HistoryDocumentMeta;
    sections: HistoryDocumentSections;
}

interface HistoryDocumentMeta {
    icdCode: string;
    diagnosisDate: string;
    doctor: string;
    specialty: string;
    nosology: string;
    diseaseType: string;
    clinicName: string;
}

interface HistoryDocumentSections {
    anamnesis: string;
    clinicalFindings: string;
    diagnosis: string;
    treatmentPlan: string;
    conclusion: string;
}

const hypertensionDocument: HistoryDocumentDetails = {
    title: 'Артериальная гипертензия',
    meta: {
        icdCode: 'I10',
        diagnosisDate: '2024-11-20',
        doctor: 'Иванов Петр Сергеевич',
        specialty: 'Терапевт',
        nosology: 'Сердечно-сосудистые заболевания',
        diseaseType: 'Хроническое',
        clinicName: 'Городская поликлиника №1',
    },
    sections: {
        anamnesis: `
        Пациент обратился с жалобами на периодические головные боли, учащенное сердцебиение, повышенное давление до 160/100 мм рт. ст., ощущение усталости. 
        История болезни: гипертония у пациента диагностирована впервые 5 лет назад. 
        Семейный анамнез отягощен: у отца и матери артериальная гипертензия.
        Обострение состояния отмечается на фоне стрессов и нерегулярного образа жизни.
      `,
        clinicalFindings: `
        При осмотре: артериальное давление - 150/95 мм рт. ст., частота сердечных сокращений - 85 уд./мин.
        Данные ЭКГ: признаки гипертрофии левого желудочка.
        Биохимический анализ крови: повышение уровня холестерина до 6,5 ммоль/л.
        Анализы мочи: без особенностей.
      `,
        diagnosis: `
        Установленный диагноз: Артериальная гипертензия, стадия 2, риск 3.
        Осложнения: гипертрофия левого желудочка.
      `,
        treatmentPlan: `
        - Фармакотерапия:
          1. Лизиноприл 10 мг утром, ежедневно.
          2. Аторвастатин 20 мг на ночь, ежедневно.
          3. Гидрохлортиазид 12,5 мг утром, ежедневно.
        - Диетические рекомендации:
          Ограничение соли до 5 г в сутки, уменьшение потребления насыщенных жиров.
        - Лечебная физкультура:
          Умеренные аэробные нагрузки (30 минут в день, 5 раз в неделю).
        - Контроль состояния:
          Ежедневное измерение артериального давления, повторный визит через месяц.
      `,
        conclusion: `
        На основании клинических данных, анамнеза и результатов лабораторных исследований 
        рекомендована фармакотерапия и изменения образа жизни.
        Необходим постоянный контроль уровня артериального давления и липидного профиля.
      `,
    },
};
