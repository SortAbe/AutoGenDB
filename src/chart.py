#!/usr/bin/env python3.11

from matplotlib import pyplot
import json

with open('size.json', 'r') as file:
    data = json.load(file)['results']

    index_lookup = [ round(i['index_lookup'], 2) for i in data]
    join_index_lookup = [ round(i['join_index_lookup'], 2) for i in data]
    string_lookup = [ round(i['string_lookup'], 2) for i in data]
    regex_lookup = [ round(i['regex_lookup'], 2) for i in data]
    derived_queries = [ round(i['derived_queries'], 2) for i in data]
    integer_sort = [ round(i['integer_sort'], 2) for i in data]
    string_sort = [ round(i['string_sort'], 2) for i in data]
    update = [ round(i['update'], 2) for i in data]
    math_operations = [ round(i['math_operations'], 2) for i in data]

    y = [ round(int(i['var_lib_mysql_size'])/1_000_000, 2) for i in data]


def make_chart(data, title, file_name):
    pyplot.figure(figsize=(18, 16), dpi=130)
    pyplot.ylabel('Time in Seconds', fontsize=24)
    pyplot.xlabel('Size of Data', fontsize=24)
    pyplot.xticks(fontsize=20)
    pyplot.yticks(fontsize=20)
    pyplot.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
    pyplot.title(title, fontsize=40)
    pyplot.plot(y, data, linewidth=3)
    pyplot.savefig(file_name + '.jpg')
    pyplot.clf()

make_chart(index_lookup, 'Index Lookup', 'index_lookup')
make_chart(join_index_lookup, 'Join Index Lookup', 'join_index_lookup')
make_chart(string_lookup, 'String Lookup', 'string_lookup')
make_chart(regex_lookup, 'Regex Lookup', 'regex_lookup')
make_chart(derived_queries, 'Derived Queries', 'derived')
make_chart(integer_sort, 'Integer Sort', 'int_sort')
make_chart(string_sort, 'String Sort', 'str_sort')
make_chart(update, 'Update', 'update')
make_chart(math_operations, 'Math Operations', 'math')
