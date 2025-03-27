import uuid
from datetime import datetime

from pydantic import BaseModel


class ReportFilter(BaseModel):
    idrep: int
    month: int
    year: int

    @property
    def as_json(self):
        return {
            'header': {
                'version': '1.00',
                'messageType': 'ReqReport',
                'messageText': 'Запрос данных отчета',
                'systemName': 'KNIME',
                'uuId': str(uuid.uuid4()),
                'createDateTime': datetime.now().isoformat(),
                'currentPack': 1,
                'totalPack': 1
            },
            'data': [
                {
                    'dataId': self.idrep,
                    'month': self.month,
                    'year': self.year
                }
            ]
        }
