import requests  # Import requests library
from pprint import pprint  # Import pretty print

# Function to view file contents
def view_file_contents(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print("The file does not exist.")
    except IOError:
        print("An error occurred while trying to read the file.")

# Function to format and clean recipe details
def format_recipe_details(meal):
    formatted_details = {}
    formatted_details['Meal'] = meal.get('strMeal', 'N/A')
    formatted_details['Category'] = meal.get('strCategory', 'N/A')
    formatted_details['Cuisine'] = meal.get('strArea', 'N/A')
    formatted_details['Tags'] = meal.get('strTags', 'N/A')
    formatted_details['Instructions'] = meal.get('strInstructions', 'N/A')
    formatted_details['Image'] = meal.get('strMealThumb', 'N/A')
    formatted_details['Source'] = meal.get('strSource', 'N/A')
    formatted_details['YouTube'] = meal.get('strYoutube', 'N/A')

    ingredients = []
    for i in range(1, 21):
        ingredient = meal.get('strIngredient{}'.format(i))
        measure = meal.get('strMeasure{}'.format(i))
        if ingredient and ingredient.strip() and measure and measure.strip():
            ingredients.append('{} {}'.format(measure, ingredient))

    formatted_details['Ingredients'] = ingredients
    return formatted_details

def search_ingredient_vegan_nonvegan():
    # Initialize the variable
    ingredient_name = None

    # Use raw_input for Python 2.7
    try:
        ingredient_name = input('What is the ingredient you would like to search for? ').strip()  # Strip any whitespace
        if not ingredient_name:
            raise ValueError("No input provided.")
    except NameError:
        print("Please enter the ingredient as a string.")
    except ValueError as ve:
        print(ve)

    # Proceed only if valid ingredient_name is provided
    if ingredient_name:
        meal_db_api_base_url = 'https://www.themealdb.com/api/json/v1/1/'  # Store the MealDB base URL in a variable

        # Dummy data for vegan/non-vegan classification (for demonstration purposes)
        vegan_ingredients = ['tofu', 'lettuce', 'tomato', 'cucumber', 'mushroom', 'beans']
        non_vegan_ingredients = ['chicken', 'beef', 'pork', 'fish', 'egg', 'cheese']

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

        def is_vegan_meal(mealdetail):  # Function to determine if the meal is vegan
            ingredients = []
            for i in range(1, 21):  # TheMealDB API lists up to 20 ingredients
                ingredient = mealdetail.get('strIngredient{}'.format(i))
                if ingredient:
                    ingredients.append(ingredient.lower())

            # Check if all ingredients are in the vegan ingredients list
            return all(ingredient in vegan_ingredients for ingredient in ingredients)

        # Step 1: Search for recipes
        meals = search_ingredient(ingredient_name)  # Store the search result in a new variable called meals
        vegan_recipes = []  # Create a list for vegan recipes
        non_vegan_recipes = []  # Create a list for non-vegan recipes

        if not meals:  # Check if we received any data at all. if not, then
            print('No meals found with ingredient {}. Please choose another one.'.format(ingredient_name))  # Print out a message to the user and ask to pick another ingredient
        else:
            # Step 2: Classify the recipes
            for meal in meals:  # If the ingredient is found, then
                mealname = meal['strMeal']  # Create new variable called mealname
                idmeal = meal['idMeal']  # Create a new variable called idmeal to get the meal id
                mealdetail = search_meal(idmeal)[0]  # Get the full meal details from the meal id for the first item and store in new variable called mealdetail

                # Determine if the meal is vegan or non-vegan
                if is_vegan_meal(mealdetail):
                    vegan_recipes.append({'name': mealname, 'id': idmeal})
                else:
                    non_vegan_recipes.append({'name': mealname, 'id': idmeal})

            # Print and sort results
            print('\nVegan Recipes:')
            for recipe in vegan_recipes:
                print(recipe['name'])

            print('\nNon-Vegan Recipes:')
            for recipe in non_vegan_recipes:
                print(recipe['name'])

            # Step 3: Ask the user to select multiple recipes for detailed information
            selected_recipe_names = input('\nEnter the names of the recipes you would like details about, separated by commas: ').split(',')

            for selected_recipe_name in selected_recipe_names:
                selected_recipe_name = selected_recipe_name.strip()
                # Find the selected recipe in both vegan and non-vegan lists
                selected_recipe = next((recipe for recipe in vegan_recipes + non_vegan_recipes if recipe['name'] == selected_recipe_name), None)

                if selected_recipe:
                    selected_meal_details = search_meal(selected_recipe['id'])[0]
                    cleaned_details = format_recipe_details(selected_meal_details)
                    print('\nDetails for {}:'.format(selected_recipe_name))
                    print('Category: {}'.format(cleaned_details['Category']))
                    print('Cuisine: {}'.format(cleaned_details['Cuisine']))
                    print('Tags: {}'.format(cleaned_details['Tags']))
                    print('Instructions: {}'.format(cleaned_details['Instructions']))
                    print('Image: {}'.format(cleaned_details['Image']))
                    print('Source: {}'.format(cleaned_details['Source']))
                    print('YouTube: {}'.format(cleaned_details['YouTube']))
                    print('Ingredients:')
                    for ingredient in cleaned_details['Ingredients']:
                        print(ingredient)
                else:
                    print('Recipe {} not found. Please make sure you entered the name correctly.'.format(selected_recipe_name))

            download_choice = input('Would you like to save the results into a txt file? y/n ')

            if download_choice.strip().lower() == 'y':
                default_file_name = 'recipe_details.txt'
                with open(default_file_name, 'w') as text_file:  # Open a different text file in write mode
                    text_file.write('Vegan Recipes:\n')
                    for recipe in vegan_recipes:
                        text_file.write('{}\n'.format(recipe['name'].encode('utf-8')))

                    text_file.write('Non-Vegan Recipes:\n')
                    for recipe in non_vegan_recipes:
                        text_file.write('{}\n'.format(recipe['name'].encode('utf-8')))

                    text_file.write