import requests  # Import requests library
from pprint import pprint  # Import pretty print

meal_db_api_base_url = 'https://www.themealdb.com/api/json/v1/1/'  # Store themealdb base URL in a new variable

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


def search_ingredient():
    ingredient_name = input("What is the ingredient you would like to search for? ").strip()
    ingredient_filter_path = 'filter.php?i='
    search_url = f"{meal_db_api_base_url}{ingredient_filter_path}{ingredient_name}"
    response = requests.get(search_url)
    data = response.json()

    if data['meals'] is None:
        print(f"No meals found with ingredient '{ingredient_name}'. Please try another ingredient.")
    else:
        meals = data['meals']
        recipe = []
        for meal in meals:
            pprint(meal['strMeal'])
            print(f"Meal ID: {meal['idMeal']}")
            recipe.append(meal['strMeal'])
            idmeal = meal['idMeal']
            mealdetail = get_meal_details(idmeal)
            instruction = mealdetail.get('strInstructions', 'No instructions available.')
            print("\nInstructions:")
            print(instruction)
            recipe.append(instruction)

        download_choice = input('Would you like to save the results into a txt file? (y/n): ')
        if download_choice.strip().lower() == 'y':
            with open('themealdb.txt', 'w+', encoding='utf-8') as text_file:
                for line in recipe:
                    text_file.write(f'{line}\n')
            print("Results saved to 'themealdb.txt'.")
        else:
            print('You chose not to download and save the recipes.')


def get_meal_details(meal_id):
    meal_lookup_path = f"lookup.php?i={meal_id}"
    search_url = f"{meal_db_api_base_url}{meal_lookup_path}"
    response = requests.get(search_url)
    data = response.json()
    return data['meals'][0] if data['meals'] else {}


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
