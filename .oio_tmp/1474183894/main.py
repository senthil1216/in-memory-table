#!/usr/bin/env python

import sys
from collections import defaultdict

class Table(object):
    def __init__(self, name, column_names, data):
        self.name = name
        self.column_names = column_names
        self.data = data


    def select(self, projected_column_names):
        selectedColIdx = []
        for colIdx in range(len(self.column_names)):
            if self.column_names[colIdx] in projected_column_names:
                selectedColIdx.append(colIdx)

        selected_columns = []
        for col in selectedColIdx:
            selected_columns.append(self.column_names[col])

        selected_data = [] 
        for rowIdx in range(len(self.data)):
            newRow = []
            for col in selectedColIdx:
                newRow.append(self.data[rowIdx][col])
            selected_data.append(newRow)
        return Table("Select", selected_columns, selected_data)


    def where(self, column_name, value):
        # find position of column
        currCol = None
        for colIdx in xrange(len(self.column_names)):
            if self.column_names[colIdx] == column_name:
                currCol = colIdx
                break
        selectedRows = []
        for rowId in xrange(len(self.data)):
            if self.data[rowId][currCol] == value:
                selectedRows.append(self.data[rowId])
        return Table("Where", self.column_names, selectedRows)


    def __repr__(self):
        return ", ".join(self.column_names) + "\n" + \
            "\n".join([", ".join([str(val) for val in row]) for row in self.data])


class DB(object):
    def __init__(self):
        self.table_map = {}


    def add_table(self, table):
        self.table_map[table.name] = table


    def table(self, table_name):
        return self.table_map[table_name]


    def right_join(self, left_table, left_table_key_name, right_table, right_table_key_name):
        return Table("RightJoin", None, None)


    def left_join(self, left_table, left_table_key_name, right_table, right_table_key_name):
        return Table("LeftJoin", None, None)


    def outer_join(self, left_table, left_table_key_name, right_table, right_table_key_name):
        return Table("OuterJoin", None, None)


    def inner_join(self, left_table, left_table_key_name, right_table, right_table_key_name):
        l = None
        for l_cols in left_table.column_names:
            if left_table.column_names[l_cols] == left_table_key_name:
                l = l_cols
                break
        r = None
        for r_cols in right_table.column_names:
            if right.column_names[r_cols] == right_table_key_name:
                r = r_cols
                break

        for l_row_id in range(len(left_table.data)):
            for r_row_id in range(len(right_table.data)):
                

        #return Table("InnerJoin", None, None)


def main(argv):
    department_table = Table('departments', ['id', 'name'], [
        [0, 'engineering'],
        [1, 'finance'] ])
    user_table = Table('users', ['id', 'department_id', 'name'], [
        [0, 0, 'Ian'],
        [1, 0, 'John'],
        [2, 1, 'Eddie'],
        [3, 1, 'Mark'] ])
    salary_table = Table('salaries', ['id', 'user_id', 'amount'], [
        [0, 0, 100],
        [1, 1, 150],
        [2, 1, 200],
        [3, 3, 200],
        [4, 3, 300],
        [5, 4, 400] ])

    db = DB()
    db.add_table(user_table)
    db.add_table(department_table)
    db.add_table(salary_table)

    # should print something like
    # id, department_id, name
    # 1, 0, John
    print db.table('users') \
            .where('id', 1) \
            .select(['id', 'department_id', 'name'])

    # should print something like
    # users.name, departments.name
    # Ian, engineering
    # John, engineering
    print db.inner_join(db.table('users'), 'department_id', db.table('departments'), 'id') \
            .where('departments.name', 'engineering') \
            .select(['users.name', 'departments.name'])

"""
    # should print something like
    # users.name, salaries.amount
    # Ian, 100
    # John, 150
    # John, 200
    # Mark, 200
    # Mark, 300
    # Eddie, None
    print db.left_join(db.table('users'), 'id', db.table('salaries'), 'user_id') \
            .select(['users.name', 'salaries.amount'])


    # should print something like
    # users.name, salaries.amount
    # Ian, 100
    # John, 150
    # John, 200
    # Mark, 200
    # Mark, 300
    # None, 400
    print db.right_join(db.table('users'), 'id', db.table('salaries'), 'user_id') \
            .select(['users.name', 'salaries.amount'])

    # should print something like
    # users.name, salaries.amount
    # Ian, 100
    # John, 150
    # John, 200
    # Mark, 200
    # Mark, 300
    # Eddie, None
    # None, 400
    print db.outer_join(db.table('users'), 'id', db.table('salaries'), 'user_id') \
            .select(['users.name', 'salaries.amount'])

"""

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


