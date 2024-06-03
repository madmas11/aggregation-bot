import pymongo
from datetime import datetime
import pandas as pd


def aggregate_salaries(start_date, end_date, type_date):
    try:
        start_date = datetime.fromisoformat(start_date)
        end_date = datetime.fromisoformat(end_date)
    except ValueError as e:
        raise ValueError('Неверный формат даты.') from e

    client = pymongo.MongoClient('127.0.0.1', 27017)
    db = client['doc']
    collection = db['sample_collection']

    sample_docs = collection.find().limit(5)
    for doc in sample_docs:
        if 'dt' not in doc or 'value' not in doc:
            raise ValueError('Данные в коллекциях должны содержать поля dt и value')

    match_stage = {
        "$match": {
            "dt": {
                "$gte": start_date,
                "$lte": end_date
            }
        }
    }
    if type_date == "month":
        date_format = "%Y-%m"
        delta = pd.date_range(start=start_date, end=end_date, freq='MS')
    elif type_date == "day":
        date_format = "%Y-%m-%d"
        delta = pd.date_range(start=start_date, end=end_date, freq='D')
    elif type_date == "hour":
        date_format = "%Y-%m-%d-%H"
        delta = pd.date_range(start=start_date, end=end_date, freq='h')

    group_stage = {
        "$group": {
            "_id": {
                "$dateToString": {
                    "format": date_format,
                    "date": "$dt"
                }
            },
            "total_salary": {"$sum": "$value"}
        }
    }
    sort_stage = {"$sort": {"_id": 1}}

    aggregation_pipeline = [match_stage, group_stage, sort_stage]
    result = list(collection.aggregate(aggregation_pipeline))

    existing_data = {item["_id"]: item["total_salary"] for item in result}
    dataset = []
    labels = []

    for date in delta:
        date_str = date.strftime(date_format)
        if date_str in existing_data:
            dataset.append(existing_data[date_str])
        else:
            dataset.append(0)
        labels.append(date.isoformat())

    return {"dataset": dataset, "labels": labels}
