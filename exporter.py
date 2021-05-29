import sys
import mariadb
import time


def export_to_db(dbconfig, temperature, weatherCode, windSpeed, windDirection):
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user=dbconfig['username'],
            password=dbconfig['password'],
            host=dbconfig['host'],
            port=dbconfig['port'],
            database=dbconfig['databaseName']
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return

    # Get Cursor
    cursor = conn.cursor()

    cDate = time.strftime('%Y-%m-%d %H:%M:%S')

    sql = "INSERT INTO " + dbconfig['measurementsTableName'] + \
        " (SensorID, Date, Value1, Value2, Value3, Value4) VALUES (%s, %s, %s, %s, %s, %s)"
    var = (str(dbconfig['sensorId']),
           cDate,
           temperature,
           weatherCode,
           windSpeed,
           windDirection)

    try:
        cursor.execute(sql, var)
        conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")

    conn.close()
