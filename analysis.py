""" File to aid the analysis of hash tables"""

from table_analysis import LinearProbeTable

table_sizes = [20021, 402221, 1000081]
hash_bases = [1, 9929, 250726]
my_table = LinearProbeTable(1000)

indian_cities_file = open("indian_cities.txt", "r")
australian_cities_file = open("aust_cities.txt", "r")
us_cities_file = open("us_cities.txt", "r")

indian_cities = []
australian_cities = []
us_cities = []

for line in indian_cities_file:
  city = line.strip()
  indian_cities.append(city)

for line in australian_cities_file:
  city = line.strip()
  australian_cities.append(city)

for line in us_cities_file:
  city = line.strip()
  us_cities.append(city)

indian_cities_file.close()
australian_cities_file.close()
us_cities_file.close()


# __INDIAN CITIES__

# table_size = 20021, base = 1
table1 = LinearProbeTable(20021)
table1.base = 1

# table_size = 402221, base = 1
table2 = LinearProbeTable(402221)
table2.base = 1

# table_size = 1000081, base = 1
table3 = LinearProbeTable(1000081)
table3.base = 1

# table_size = 20021, base = 9929
table4 = LinearProbeTable(20021)
table4.base = 9929

# table_size = 402221, base = 9929
table5 = LinearProbeTable(402221)
table5.base = 9929

# table_size = 1000081, base = 9929
table6 = LinearProbeTable(1000081)
table6.base = 9929

# table_size = 20021, base = 250726
table7 = LinearProbeTable(20021)
table7.base = 250726

# table_size = 402221, base = 250726
table8 = LinearProbeTable(402221)
table8.base = 250726

# table_size = 1000081, base = 250726
table9 = LinearProbeTable(1000081)
table9.base = 250726

# __AUSTRALIAN CITIES__

# table_size = 20021, base = 1
table10 = LinearProbeTable(20021)
table10.base = 1

# table_size = 402221, base = 1
table11 = LinearProbeTable(402221)
table11.base = 1

# table_size = 1000081, base = 1
table12 = LinearProbeTable(1000081)
table12.base = 1

# table_size = 20021, base = 9929
table13 = LinearProbeTable(20021)
table13.base = 9929

# table_size = 402221, base = 9929
table14 = LinearProbeTable(402221)
table14.base = 9929

# table_size = 1000081, base = 9929
table15 = LinearProbeTable(1000081)
table15.base = 9929

# table_size = 20021, base = 250726
table16 = LinearProbeTable(20021)
table16.base = 250726

# table_size = 402221, base = 250726
table17 = LinearProbeTable(402221)
table17.base = 250726

# table_size = 1000081, base = 250726
table18 = LinearProbeTable(1000081)
table18.base = 250726

# __US CITIES__
# table_size = 20021, base = 1
table19 = LinearProbeTable(20021)
table19.base = 1

# table_size = 402221, base = 1
table20 = LinearProbeTable(402221)
table20.base = 1

# table_size = 1000081, base = 1
table21 = LinearProbeTable(1000081)
table21.base = 1

# table_size = 20021, base = 9929
table22 = LinearProbeTable(20021)
table22.base = 9929

# table_size = 402221, base = 9929
table23 = LinearProbeTable(402221)
table23.base = 9929

# table_size = 1000081, base = 9929
table24 = LinearProbeTable(1000081)
table24.base = 9929

# table_size = 20021, base = 250726
table25 = LinearProbeTable(20021)
table25.base = 250726

# table_size = 402221, base = 250726
table26 = LinearProbeTable(402221)
table26.base = 250726

# table_size = 1000081, base = 250726
table27 = LinearProbeTable(1000081)
table27.base = 250726

# insert Indian cities into the hashtables
for city in indian_cities:
    table1[city] = city # treating city name (data) as key an value
    table2[city] = city
    table3[city] = city
    table4[city] = city
    table5[city] = city
    table6[city] = city
    table7[city] = city
    table8[city] = city
    table9[city] = city

# insert Australian cities into the hashtables
for city in australian_cities:
    table10[city] = city
    table11[city] = city
    table12[city] = city
    table13[city] = city
    table14[city] = city
    table15[city] = city
    table16[city] = city
    table17[city] = city
    table18[city] = city

# insert US cities into the hashtables
for city in us_cities:
    table19[city] = city
    table20[city] = city
    table21[city] = city
    table22[city] = city
    table23[city] = city
    table24[city] = city
    table25[city] = city
    table26[city] = city
    table27[city] = city

# __INDIAN CITIES__
print(table1.statistics())
print(table2.statistics())
print(table3.statistics())
print(table4.statistics())
print(table5.statistics())
print(table6.statistics())
print(table7.statistics())
print(table8.statistics())
print(table9.statistics())

# __AUSTRALIAN CITIES__
print(table10.statistics())
print(table11.statistics())
print(table12.statistics())
print(table13.statistics())
print(table14.statistics())
print(table15.statistics())
print(table16.statistics())
print(table17.statistics())
print(table18.statistics())

# __US CITIES__
print(table19.statistics())
print(table20.statistics())
print(table21.statistics())
print(table22.statistics())
print(table23.statistics())
print(table24.statistics())
print(table25.statistics())
print(table26.statistics())
print(table27.statistics())
