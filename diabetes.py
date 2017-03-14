# -*- coding: utf-8 -*-

# This is a simple example demostrate the use SQLAlchemy with sqlite database
# Import create_engine, MetaData
from sqlalchemy import create_engine, MetaData, select
from sqlalchemy import Table, Column, String, Integer, Float
from sqlalchemy import insert
import csv

# Define an engine to connect to DB diabetes.sqlite
engine = create_engine('sqlite:///diabetes.sqlite')
connection = engine.connect()

# Initialize MetaData
metadata = MetaData()

# Build a table, diabetes
diabetes = Table('diabetes', metadata, 
                 Column('times_pregnant', Integer()), 
                 Column('PGC', Float()),
                 Column('DBP', Integer()),
                 Column('triceps_thick', Integer()),
                 Column('serum_insulin', Float()),
                 Column('BMI', Float()),
                 Column('DPF', Float()),
                 Column('age', Integer()),
                 Column('diabetes', Integer())
               )

#Create the table in the database
metadata.create_all(engine)

# Create an empty list
values_list = []

csv_reader = csv.reader(open("pima-indians-diabetes.csv", 'rt'))

# Iterate over the rows
for row in csv_reader:
    # Create a dictionary with the values
    data = {'times_pregnant': row[0], 'PGC': row[1], 'DBP':row[2], 'tricepts_thick': row[3],
            'serum_insulin': row[4], 'BMI': row[5], 'DPF': row[6], 'age': row[7], 'diabetes': row[8]}
    # Append the dictionary to the values list
    values_list.append(data)
    
# Build insert statement
stmt = insert(diabetes)

# Use values_list to insert data
results = connection.execute(stmt, values_list)

# Print rowcount
print("Row counts = " + str(results.rowcount))

# Build another statement
stmt1 = select([diabetes.columns.age, diabetes.columns.BMI])
stmt1 = stmt1.where(diabetes.columns.age > 80)
results1 = connection.execute(stmt1).fetchall()

for result in results1:
      print(result.age, result.BMI)
