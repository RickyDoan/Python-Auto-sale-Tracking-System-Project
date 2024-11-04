from fastapi import FastAPI, HTTPException
from fontTools.misc.plistlib import end_date

import db_helper
from datetime import date
from typing import List
from pydantic import BaseModel


class List_sales(BaseModel):
        DATE_TIME : date
        PRODUCTLINE : str
        STATUS : str
        COUNTRY : str
        QUANTITYORDERED : float
        SALES : float

class Date_sale(BaseModel):
    start_date : date
    end_date : date

app = FastAPI()

@app.get('/sales/{date_time}', response_model= List[List_sales])
def get_expense(date_time : date):
    sales = db_helper.fetch_sales_for_date(date_time)
    return sales

@app.post('/sales/{date_time}')
def add_or_update_sales(date_time: date, sales : List[List_sales]):
    db_helper.delete_sales_for_date(date_time)
    for sale in sales:
        db_helper.insert_sales(date_time,sale.ORDERNUMBER,sale.PRODUCTLINE,sale.DEALSIZE,sale.STATUS,
        sale.COUNTRY, sale.QUANTITYORDERED, sale.PRICEEACH, sale.SALES)
    return "Successfully added or updated sales"

@app.post('/analytics/productline')
def get_analytics_sales(date_range: Date_sale):
    data = db_helper.fetch_sales_summary(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database.")

    total_amount_sale =  sum([ row['total_sale'] for row in data])
    total_amount_quantity = sum([ row['total_quantity'] for row in data])

    holder = []
    for index, row in enumerate(data):
        holder.append({
            'name_productline' : row['PRODUCTLINE'],
            'total_sale' : row['total_sale'],
            'total_quantity' : row['total_quantity'],
            'total_sale_pct' : round(row['total_sale']*100/total_amount_sale,2),
            'total_quantity_pct' : round(row['total_quantity']*100/total_amount_quantity,2),
        })
    return holder

@app.post('/analytics/country')
def fetch_sale_by_country(date_range: Date_sale):
    data = db_helper.fetch_sale_by_country(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database.")

    total_sale = sum([ row['total_sale'] for row in data])
    total_quantity = sum([ row['total_quantity'] for row in data])
    holder = []
    for index, row in enumerate(data):
        holder.append({
            'country_name': row['COUNTRY'],
            'total_sale' : row['total_sale'],
            'total_quantity' : row['total_quantity'],
            'total_sale_pct' : round(row['total_sale']*100/total_sale,2),
            'total_quantity_pct' : round(row['total_quantity']*100/total_quantity,2)
        })
    return holder