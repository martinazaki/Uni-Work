def factors(num):

	if n <= 0:
		raise ValueError

	if type(num) == str():
		raise TypeError

	i = 2
	number_factors = []

	while i*i <= num:
		if num % i:
			i += 1
			
		else:
			num //= i
			number_factors.append(i)

	if num > 1:
		number_factors.append(num)					

	return number_factors