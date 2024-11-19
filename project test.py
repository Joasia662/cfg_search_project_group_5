import requests #Import requests library
from pprint import pprint #Import pretty print

ingredient_name = input('What is the ingredient you would like to search for?') #Ask the user to enter an ingredient that they want to search for
meal_db_api_base_url = 'https://www.themealdb.com/api/json/v1/1/'  # Store themealdb base url in new variable

def search_ingredient(): #Create a function that makes a request to the Themealdb API with the required ingredient as part of the search query

    ingredient_filter_path = 'filter.php?i='  #Store the ingredient filter path in new variable
    search_url = '{}{}{}'.format(meal_db_api_base_url, ingredient_filter_path, ingredient_name.strip())  #Store the search url in new variable, including base + filter + the ingredient the user selected. Used the strip method on the ingredient_name variable in order to remove leading and trailing white spaces
    response = requests.get(search_url)  #Use the requests library to ask for this information using the search_url variable
    data = response.json()  #Turn into json object that we can work with and store in new variable called data
    #print(data['meals'])  #Print out the response in order to see the list of returned recipes and their properties
    return data['meals']  #Return the response

meals = search_ingredient() #Store the search result in a new variable called meals
if meals is None: #Check if we received any data at all. if not, then
    print('No meals found with ingredient {}. Please choose another one.'.format(ingredient_name)) #Print out a message to the user and ask to pick another ingredient
else:
    for meal in meals: #If the ingredient is found, then
        pprint(meal['strMeal']) #Print out the name of the meal
