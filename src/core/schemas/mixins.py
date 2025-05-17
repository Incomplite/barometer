from datetime import datetime

from pydantic import BaseModel


class TimestampSchemaMixin(BaseModel):
    created_at: datetime
    updated_at: datetime

    def update_timestamp(self):
        self.updated_at = datetime.now()
