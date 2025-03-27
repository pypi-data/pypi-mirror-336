REPORT_MOCK = {
    "header": {
        "version": "1.00",
        "messageType": "Response",
        "messageText": "Ответ на сообщение",
        "system": "SAP MDG",
        "uuID": "425f1d56-2015-1eef-95a5-89a7df685893",
        "createDateTime": "2025-02-03T02:17:03Z",
        "currentPack": 1,
        "totalPack": 10,
        "statusCode": "53",
        "statusText": "Запрос обработан",
        "statusComment": "Спасибо за корректные данные!"
    },
    "metadata": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "Parameter_1": {
                    "type": "string"
                },
                "Parameter_3": {
                    "type": "string"
                },
                "Parameter_6": {
                    "type": "string"
                },
                "Table_1": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "Field_1": {
                                "type": "integer"
                            },
                            "Field_2": {
                                "type": "string"
                            },
                            "Field_3": {
                                "type": "string"
                            }
                        },
                        "additionalProperties": False,
                        "required": ["Field_1", "Field_2", "Field_3"]
                    }
                }
            },
            "additionalProperties": False,
            "required": [
                "Parameter_1", "Parameter_3", "Parameter_6", "Table_1"
            ]
        }
    },
    "data": [
        {
            "Parameter_1": "значение параметра 1",
            "Parameter_3": "100.750",
            "Parameter_6": "2024-08-08T02:17:03.466995Z",
            "Table_1": [
                {
                    "Field_1": 11,
                    "Field_2": "строка Field_2",
                    "Field_3": "строка Field_2"
                }, {
                    "Field_1": 21,
                    "Field_2": "строка 22",
                    "Field_3": "строка Field_2"
                }, {
                    "Field_1": 31,
                    "Field_2": "строка 32",
                    "Field_3": "строка Field_2"
                }
            ]
        }
    ]
}

SCHEMA_MOCK = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "Parameter_1": {
                "type": "string"
            },
            "Parameter_3": {
                "type": "string"
            },
            "Parameter_6": {
                "type": "string"
            },
            "Table_1": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "Field_1": {
                            "type": "integer"
                        },
                        "Field_2": {
                            "type": "string"
                        },
                        "Field_3": {
                            "type": "string"
                        }
                    },
                    "additionalProperties": False,
                    "required": ["Field_1", "Field_2", "Field_3"]
                }
            }
        },
        "additionalProperties": False,
        "required": ["Parameter_1", "Parameter_3", "Parameter_6", "Table_1"]
    }
}
