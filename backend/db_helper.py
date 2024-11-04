import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger


logger = setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tung144@@",
        database="Autosales_db"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()

#Get sales from 1 day chose
def fetch_sales_for_date(date_time):
    logger.info(f"fetch_sale_for_date called with {date_time}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM auto_sale_tracking WHERE DATE_TIME = %s", (date_time,))
        sale = cursor.fetchall()
        return sale
#Delete value with specific day choose
def delete_sales_for_date(date_time):
    logger.info(f"delete_sales_for_date called with {date_time}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM auto_sale_tracking WHERE date_time = %s", (date_time,))

#Insert value in specific day
def insert_sales(date_time,PRODUCTLINE,STATUS,COUNTRY,QUANTITYORDERED,SALES):
    logger.info(
        f'''insert_sale called with date: {date_time},PRODUCTLINE: {PRODUCTLINE},
        STATUS: {STATUS},COUNTRY :{COUNTRY}, QUANTITYORDERED:{QUANTITYORDERED},SALES: {SALES} ''')
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            '''INSERT INTO auto_sale_tracking (DATE_TIME,,PRODUCTLINE,STATUS,COUNTRY,QUANTITYORDERED,SALES) 
                        VALUES (%s, %s, %s, %s, %s, %s)''',
            (date_time,PRODUCTLINE,STATUS,COUNTRY,QUANTITYORDERED,SALES))

def fetch_sales_summary(start_date, end_date):
    logger.info(f"fetch_sales_summary called with start: {start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''
                        SELECT 
                                PRODUCTLINE,
                                ROUND(SUM(SALES),2) AS total_sale,
                                ROUND(SUM(QUANTITYORDERED),2) AS total_quantity
                        FROM auto_sale_tracking
                        WHERE DATE_TIME BETWEEN %s AND %s
                        GROUP BY PRODUCTLINE
                        ''',
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data

def fetch_sale_by_country(start_date, end_date):
    logger.info(f"fetch_sale_summary_by_country called with start: {start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT 
                                COUNTRY,
                                ROUND(SUM(SALES),2) AS total_sale,
                                SUM(QUANTITYORDERED) AS total_quantity
                        FROM
                            Autosales_db.auto_sale_tracking
                        WHERE DATE_TIME BETWEEN %s AND %s
                        GROUP BY COUNTRY
                        ORDER BY total_sale DESC
                        LIMIT 7''',
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data

if __name__ == "__main__":
    # sale = fetch_sales_for_date("2020-01-20")
    # print(sale)
    # sales = delete_sales_for_date("2019-06-15")
    # print(sales)
    # sales = insert_sales('2019-06-15', 86.6, 120, 'Shipped', 'Motorcycles')
    # print(sales)
    # data = fetch_sales_summary('2018-08-02', '2020-08-02')
    # print(data)
    # for record in data:
    #     print(record)
    # print(data)
    data = fetch_sale_by_country("2018-01-05", "2020-01-05")
    print(data)
    # '2018-08-02'
    # AND
    # '2020-08-02'