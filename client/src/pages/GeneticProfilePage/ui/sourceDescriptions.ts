export const sourceDetails = (url: string) => {
  if (url.includes("myvariant.info")) {
    return {
      name: "MyVariant.info",
      description:
        "Аннотации вариантов VCF; через этот ресурс получаются записи ClinVar для сопоставления с генотипом.",
    };
  }
  if (url.includes("pgscatalog.org")) {
    return {
      name: "PGS Catalog",
      description:
        "Каталог полигенных моделей: описания признаков и файлы весов SNP для расчёта оценок.",
    };
  }
  if (url.includes("internationalgenome.org")) {
    return {
      name: "1000 Genomes Project",
      description:
        "Публичные генотипы, на основе которых подготовлена EUR-выборка для сравнения полигенного балла.",
    };
  }
  return {
    name: url,
    description: "Дополнительный источник, указанный в отчёте.",
  };
};
