import requests  # Import requests library
from pprint import pprint  # Import pretty print

# Store themealdb base URL in a new variable
meal_db_api_base_url = 'https://www.themealdb.com/api/json/v1/1/'  

# Welcome message
user_name = input('Hi! Welcome to the Meal Planner. Please, tell us your name :) ')
print('Nice to meet you, {}! '.format(user_name))


def search_meal_by_name():
    meal_name = input("Enter the name of the meal you want to search for: ").strip()
    search_url = f"{meal_db_api_base_url}search.php?s={meal_name}"
    response = requests.get(search_url)
    data = response.json()
    if data['meals'] is None:
        print(f"No meal found with the name '{meal_name}'.")
    else:
        meal = data['meals'][0]
        pprint(meal)
        print("\nInstructions:")
        print(meal['strInstructions'])


def get_meal_details(meal_id):
    meal_lookup_path = f"lookup.php?i={meal_id}"
    search_url = f"{meal_db_api_base_url}{meal_lookup_path}"
    response = requests.get(search_url)
    data = response.json()
    return data['meals'][0] if data['meals'] else {}

def separate_ingredients_and_id_from_meal(my_local_meal):
    item = {
        "meal_id": my_local_meal['idMeal'],
        "ingredients": format_ingredients(my_local_meal)
    }
    return item

def format_ingredients(my_local_meal):
    local_iterator = 1
    ingredient_list = []
    while True:
        if f"strIngredient{local_iterator}" in my_local_meal:
            ingredient = my_local_meal[f"strIngredient{local_iterator}"]
            if ingredient:
                ingredient_list.append((ingredient.lower()))
            local_iterator += 1
        else:
            break
    return ingredient_list

def filter_by_ingredient(my_local_meal_list, my_local_ingredient):
    new_array = [meal for meal in my_local_meal_list if my_local_ingredient in meal["ingredients"]]
    return new_array

def display_meals(local_list_of_meals_with_their_ingredients):
    local_recipe = []
    for meal in local_list_of_meals_with_their_ingredients:
        meal_detail = get_meal_details(meal["meal_id"])
        local_recipe.append(meal_detail["strMeal"])

        for key, value in meal_detail.items():  # For all the key value pairs in a meal
            if key.startswith("strIngredient") and value:  # Find those where the key starts with strIngredient and
                index = key[
                        len("strIngredient"):]  # Extract the number from the key (e.g. strIngredient1 2 3 4 5...)
                ingredient_and_measure = 'Ingredient {}: {}, Measure: {}'.format(index, value, meal_detail[
                    'strMeasure' + str(index)])
                print(ingredient_and_measure)  # Print ingredient + measure as result
                local_recipe.append(ingredient_and_measure)  # Add the ingredient + measure to the recipe list

        instruction = meal_detail.get('strInstructions', 'No instructions available.')
        print("\nInstructions:")
        print(instruction, "\n\n")
        local_recipe.append(instruction)

    return local_recipe

def download_file(local_recipe):
    download_choice = input('Would you like to save the results into a txt file? (y/n): ')
    if download_choice.strip().lower() == 'y':
        with open('themealdb.txt', 'w+', encoding='utf-8') as text_file:
            for line in local_recipe:
                text_file.write(f'{line}\n')
        print("Results saved to 'themealdb.txt'.")
    else:
        print('You chose not to download and save the recipes.')

def search_ingredient():
    index = 0
    ingredient_filter_path = 'filter.php?i='
    list_of_meals_with_their_ingredients = []

    print('What is the ingredient you would like to search for? ')
    ingredient_name = input("Ingredient nr: " + str(index + 1) + " : ")
    search_url = f"{meal_db_api_base_url}{ingredient_filter_path}{ingredient_name}"
    response = requests.get(search_url)
    data = response.json()

    if data['meals'] is None:
        print(f"No meals found with ingredient '{ingredient_name}'. Please try another ingredient.")
    else:
        meals = data['meals']
        recipe = []
        for meal in meals:
            id_meal = meal['idMeal']
            meal_detail = get_meal_details(id_meal)
            list_of_meals_with_their_ingredients.append(separate_ingredients_and_id_from_meal(meal_detail))

        index += 1
        while True:
            if len(list_of_meals_with_their_ingredients) != 0:
                user_input = input("We have found " + str(
                    len(list_of_meals_with_their_ingredients)) + " meals. Would you like to narrow your search? (y/n)")
                if user_input.lower() == 'n':
                    break
                elif user_input.lower() == 'y':
                    ingredient_name = input("Ingredient nr: " + str(index + 1) + " : ")
                    list_of_meals_with_their_ingredients = filter_by_ingredient(list_of_meals_with_their_ingredients,
                                                                                ingredient_name.lower())
                    index += 1
                else:
                    print("Unknown option was selected")
            else:
                print("There is no recipe matching your criteria :( Try Again")
                break

        recipe = display_meals(list_of_meals_with_their_ingredients)
        if len(list_of_meals_with_their_ingredients) != 0: download_file(recipe)

def random_meal():
    random_meal_url = f"{meal_db_api_base_url}random.php"
    response = requests.get(random_meal_url)
    data = response.json()
    meal = data['meals'][0]
    pprint(meal)
    print("\nInstructions:")
    print(meal['strInstructions'])


def menu():
    while True:
        print("\nMenu:")
        print("1. Search for a meal by name")
        print("2. Get a random meal")
        print("3. Search meals by ingredient")
        print("4. Exit")
        choice = input("Please enter your choice (1-4): ").strip()

        if choice == "1":
            search_meal_by_name()
        elif choice == "2":
            random_meal()
        elif choice == "3":
            search_ingredient()
        elif choice == "4":
            print(f"Goodbye, {user_name}! Happy cooking!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
menu()

