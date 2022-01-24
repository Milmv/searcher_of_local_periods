import datetime
import time
from datetime import timezone

MS_FROM_DAY = 86400.0


def change_date_to_datetime(arg):
    return datetime.datetime.strptime(arg, '%Y-%m-%d')


def change_datetime_to_unix(arg):
    return arg.replace(tzinfo=timezone.utc).timestamp()


def array_from_unix_range(start, end):
    arr = [start]

    i = start
    while i < end:
        i = i + MS_FROM_DAY
        arr.append(i)

    return arr


def attribute_array_from_dictionary(list, value):
    arr = []

    for el in list:
        arr.append(el.__getattribute__(value))

    return arr


def datetime_array_from_unix_array(list):
    arr = []
    for el in list:
        newel = datetime.datetime.utcfromtimestamp(el).strftime('%Y-%m-%d')
        arr.append(newel)

    return arr


def delete_duplicates(arr):
    return list(set(arr))


def get_union_range(arr):
    array = []

    for el in arr:
        start_unix = change_datetime_to_unix(el.start)
        end_unix = change_datetime_to_unix(el.end)
        newArr = array_from_unix_range(start_unix, end_unix)
        array = array + newArr

    array_without_duplicates = delete_duplicates(array)
    return sorted(array_without_duplicates)


def array_of_uncontained(period, data):
    newArr = []
    for el in period:
        if el not in data:
            newArr.append(el)

    return newArr
