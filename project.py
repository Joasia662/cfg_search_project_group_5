import requests  # Import requests library
from pprint import pprint  # Import pretty print

ingredient_name = input(
    'What is the ingredient you would like to search for?')  # Ask the user to enter an ingredient that they want to search for
meal_db_api_base_url = 'https://www.themealdb.com/api/json/v1/1/'  # Store themealdb base url in new variable


def search_ingredient():  # Create a function that makes a request to the Themealdb API with the required ingredient as part of the search query
    ingredient_filter_path = 'filter.php?i='  # Store the ingredient filter path in new variable
    search_url = '{}{}{}'.format(meal_db_api_base_url, ingredient_filter_path,
                                 ingredient_name.strip())  # Store the search url in new variable, including base + filter + the ingredient the user selected. Used the strip method on the ingredient_name variable in order to remove leading and trailing white spaces
    response = requests.get(
        search_url)  # Use the requests library to ask for this information using the search_url variable
    data = response.json()  # Turn into json object that we can work with and store in new variable called data
    # print(data['meals'])  #Print out the response in order to see the list of returned recipes and their properties
    return data['meals']  # Return the response


def search_meal():  # Create a function that makes a request to the Themealdb API with the a specific meal id to get the full details of a meal
    meal_lookup_path = 'lookup.php?i='  # Store the ingredient lookup path in new variable
    search_url = '{}{}{}'.format(meal_db_api_base_url, meal_lookup_path,
                                 idmeal)  # Store the search url in new variable, including base + filter + the meal id pertaining to the ingredient the user selected.
    response = requests.get(
        search_url)  # Use the requests library to ask for this information using the search_url variable
    data = response.json()  # Turn into json object that we can work with and store in new variable called data
    # print(data['meals'])  #Print out the response in order to see the list of returned recipes and their properties
    return data['meals']  # Return the response


meals = search_ingredient()  # Store the search result in a new variable called meals
if meals is None:  # Check if we received any data at all. if not, then
    print('No meals found with ingredient {}. Please choose another one.'.format(
        ingredient_name))  # Print out a message to the user and ask to pick another ingredient
else:
    for meal in meals:  # If the ingredient is found, then
        pprint(meal['strMeal'])  # Print out the name of the meal
        # pprint(meal['idMeal'])  #Print out the id of the meal
        idmeal = meal['idMeal']  # Create a new variable called idmeal to get the meal id
        mealdetail = search_meal()[
            0]  # Get the full meal details from the meal id for the first item and store in new variable called mealdetail
        # pprint(mealdetail) #Print out the full meal details for each meal containing the ingredient selected by user

        print(mealdetail['strInstructions'])  # Print the instructions
