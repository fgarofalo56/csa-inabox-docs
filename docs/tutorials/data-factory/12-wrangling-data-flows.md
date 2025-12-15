# 🧪 Wrangling Data Flows

> __🏠 [Home](../../../README.md)__ | __📖 [Documentation](../../README.md)__ | __🎓 [Tutorials](../README.md)__ | __🔄 [Data Factory](README.md)__ | __Wrangling Data Flows__

![Tutorial](https://img.shields.io/badge/Tutorial-Wrangling_Data_Flows-blue)
![Duration](https://img.shields.io/badge/Duration-20_minutes-green)
![Level](https://img.shields.io/badge/Level-Intermediate-yellow)

__Leverage Power Query integration in Azure Data Factory for self-service data preparation and transformation.__

## 📋 Table of Contents

- [Wrangling Overview](#wrangling-overview)
- [Power Query Integration](#power-query-integration)
- [Next Steps](#next-steps)

## 🎯 Wrangling Overview

Wrangling Data Flows bring Power Query's intuitive interface to Azure Data Factory, enabling business analysts to prepare data without coding.

### Features

- Visual data profiling
- Column operations
- Data type conversions
- Filtering and sorting
- Pivoting and unpivoting
- Merging and appending

## 🔄 Power Query Integration

### Create Wrangling Data Flow

```json
{
  "name": "CustomerWranglingDataFlow",
  "properties": {
    "type": "WranglingDataFlow",
    "typeProperties": {
      "sources": [
        {
          "name": "CustomerSource",
          "dataset": {"referenceName": "CustomerCSV"}
        }
      ]
    }
  }
}
```

## 📚 Additional Resources

- [Wrangling Data Flow Documentation](https://docs.microsoft.com/azure/data-factory/wrangling-overview)
- [Power Query Reference](https://docs.microsoft.com/power-query/)

## 🚀 Next Steps

__→ [13. Pipeline Triggers](13-triggers.md)__

---

__Module Progress__: 12 of 18 complete

*Tutorial Version: 1.0*
*Last Updated: January 2025*
