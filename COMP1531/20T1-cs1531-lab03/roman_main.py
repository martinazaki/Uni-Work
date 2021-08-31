import sys

from roman import roman

if __name__ == '__main__':
	print(roman('II'))          # 2
	print(roman('IV'))          # 4
	print(roman('IX'))          # 9
	print(roman('XIX'))         # 19
	print(roman('XX'))          # 20
	print(roman('MDCCLXXVI'))   # 1776
	print(roman('MMXIX'))       # 2019