from datetime import date, timedelta, time

from pydantic import BaseModel


class Area(BaseModel):
    name: str
    minimum_fl: int
    maximum_fl: int
    start_time: time
    end_time: time

    @property
    def country_ident(self) -> str:
        return self.name[:2]

    @property
    def start_date(self) -> str:
        return date.today().strftime("%y%m%d")

    @property
    def end_date(self) -> str:
        if self.start_time > self.end_time:
            return (date.today() + timedelta(days=1)).strftime("%y%m%d")
        return date.today().strftime("%y%m%d")

    @property
    def week_days(self) -> str:
        return "0"

    @property
    def out_start_time(self) -> str:
        return self.start_time.strftime("%H%M")

    @property
    def out_end_time(self) -> str:
        return self.end_time.strftime("%H%M")

    @property
    def lower(self) -> str:
        return str(self.minimum_fl * 100)

    @property
    def upper(self) -> str:
        return str(self.maximum_fl * 100)

    def __str__(self) -> str:
        return f"{self.name}:{self.start_date}:{self.end_date}:{self.week_days}:{self.out_start_time}:{self.out_end_time}:{self.lower}:{self.upper}:AUP/UUP"
