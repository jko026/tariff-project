from datetime import datetime
date = '5/1/2020'
print(date.replace('/',','))
date_object = datetime.strptime(date, "%m/%d/%Y")
print(date_object)

new_date = datetime.strptime(date, '%m/%d/%Y').strftime('%B %d, %Y')
print(new_date)