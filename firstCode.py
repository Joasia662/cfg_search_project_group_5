import requests  # Import requests library
from pprint import pprint  # Import pretty prin
# Use raw_input instead of input for Python 2.7
ingredient_name = raw_input('What is the ingredient you would like to search for? ')  # Ask the user to enter an ingredient
meal_db_api_base_url = 'https://www.themealdb.com/api/json/v1/1/'  # Store the MealDB base URL in a variable

def search_ingredient(ingredient_name):  # Create a function that makes a request to the Themealdb API with the required ingredient as part of the search query
    ingredient_filter_path = 'filter.php?i='  # Store the ingredient filter path in new variable
    search_url = '{}{}{}'.format(meal_db_api_base_url, ingredient_filter_path, ingredient_name.strip())  # Construct search URL
    response = requests.get(search_url)  # Use the requests library to ask for this information using the search_url variable
    data = response.json()  # Turn into JSON object that we can work with and store in new variable called data
    return data.get('meals')  # Return the response

def search_meal(idmeal):  # Create a function that makes a request to the Themealdb API with a specific meal id to get the full details of a meal
    meal_lookup_path = 'lookup.php?i='  # Store the ingredient lookup path in new variable
    search_url = '{}{}{}'.format(meal_db_api_base_url, meal_lookup_path, idmeal)  # Construct search URL
    response = requests.get(search_url)  # Use the requests library to ask for this information using the search_url variable
    data = response.json()  # Turn into JSON object that we can work with and store in new variable called data
    return data.get('meals')  # Return the response

meals = search_ingredient(ingredient_name)  # Store the search result in a new variable called meals
recipe = []  # Create a list called recipe

if not meals:  # Check if we received any data at all. if not, then
    print('No meals found with ingredient {}. Please choose another one.'.format(ingredient_name))  # Print out a message to the user and ask to pick another ingredient
else:
    for meal in meals:  # If the ingredient is found, then
        mealname = meal['strMeal']  # Create new variable called mealname
        pprint(mealname)  # Print out the name of the meal
        recipe.append(mealname)  # Add the mealname to the recipe list
        idmeal = meal['idMeal']  # Create a new variable called idmeal to get the meal id
        mealdetail = search_meal(idmeal)[0]  # Get the full meal details from the meal id for the first item and store in new variable called mealdetail
        instruction = mealdetail['strInstructions']  # Create new variable called instruction
        print(instruction)  # Print the instructions
        recipe.append(instruction)  # Add the instruction to the recipe list

download_choice = raw_input('Would you like to save the result into a txt file? y/n ')

if download_choice.strip().lower() == 'y':
    with open('themealdb.txt', 'w') as text_file:  # Open the themealdb.txt file in write mode as text file
        for line in recipe:
            text_file.write('{}\n'.format(line))  # Take this text file and write the content of our variable inside
    print('The recipe has been saved to themealdb.txt.')
else:
    print('You chose not to download and save the recipe.')
