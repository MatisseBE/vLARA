import re
from datetime import time
from typing import List, Tuple

from area import Area


def parse_line() -> dict:
    pass


def normalize_text(text: str) -> str:
    """ Remove unwanted data irregularities """
    _text = text.replace("\r", "")
    _text = _text.replace("\ufeff", "")
    return _text


def parse_time_string(string: str) -> time:
    """ Example 11:00 -> time(hour=11, minute=0)"""
    hour, minute = string.split(':')
    return time(hour=int(hour), minute=int(minute))


def regex_areas(text: str) -> List[Tuple[str]]:
    """Parenthesis means that the data will be extracted
    Sequence: RSA,NOTAM,REMARK,MNM FL,MAX FL,WEF,UNT,FUA/EU RS,FIR,UIR"""
    return re.findall(r"(\S*),.*,.*,(\d{3}),(\d{3}),(\d{2}:\d{2}),(\d{2}:\d{2})", text)


def parse_csv_lines(raw: str) -> List[Area]:
    text: str = normalize_text(raw)
    _areas: List[Tuple[str]] = regex_areas(text)
    parsed_areas: List[Area] = []
    for _area in _areas:
        name, minimum_fl, maximum_fl, start_time, end_time = _area
        if not len(name):
            continue
        parsed_areas.append(
            Area(name=str(name),
                 minimum_fl=int(minimum_fl),
                 maximum_fl=int(maximum_fl),
                 start_time=parse_time_string(start_time),
                 end_time=parse_time_string(end_time)))
    return parsed_areas
