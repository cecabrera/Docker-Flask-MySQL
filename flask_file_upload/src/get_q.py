from datetime import date
from pandas import NA


def get_q(st: str):
    x = str(st).split("-")
    if len(x) > 1:
        year = int(x[0])
        month = int(x[1])
        day_time = x[2]
        day = int(day_time.split(sep="T")[0])
        r = date(year=year, month=month, day=day)
        q = (r.month-1)//3 + 1
        q = f"Q{q}"
    else:
        q = NA
    return q
