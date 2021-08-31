#calc bmi
w = float(input('What is your weight in kg? '))
h = float(input('What is your height in m? '))
bmi_index = round(w / (h * h), 1)
print('Your BMI is', bmi_index)
