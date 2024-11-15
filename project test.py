import requests #import requests library
from pprint import pprint
ingredient_name = input('What is the ingredient you would like to search for?')
meal_db_api_base_url = 'https://www.themealdb.com/api/json/v1/1/'
ingredient_filter_path = 'filter.php?i='
search_url = '{}{}{}'.format(meal_db_api_base_url, ingredient_filter_path, ingredient_name) # asked to get ingredient name from url
response = requests.get(search_url) #use the requests library to ask fro this information
data = response.json() #turned into json object that we can work with
print(data['meals']) #print out
meals = data['meals']
if meals is None:
    print('No meals found with ingredient {}. Please choose another one.'.format(ingredient_name))
else:
    for meal in meals:
        pprint(meal['strMeal'])