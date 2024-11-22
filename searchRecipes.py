import requests # Importing the request module to make http request

# List of common non-vegan ingredients
non_vegan_ingredients = [
    "chicken", "beef", "pork", "fish", "seafood", "egg", "milk", "cheese", "honey",
    "butter", "gelatin", "yogurt", "lamb", "bacon", "duck", "turkey", "shrimp", "crab"
]

def get_recipes_by_ingredient(ingredient): # Define a function to search for a recipes bz ingredient
    url = "https://www.themealdb.com/api/json/v1/1/filter.php?i={}".format(ingredient) # Construct the URL with the ingredient
    response = requests.get(url) # Make a GET request to the URL
    if response.status_code == 200: # Check if the request was successful
        return response.json() #Return the response in JSON format
    else: # If the request was not successful
        return None # Return None

def is_vegan(meal): # Define a function to check if a meal is vegan
    # List comprehension to get all ingredients from the meal
    ingredients = [meal["strIngredient{}".format(i)] for i in range(1, 21) if meal["strIngredient{}".format(i)]]
    # Check if all ingredients are not in the non-vegan list
    return all(ingredient.lower() not in non_vegan_ingredients for ingredient in ingredients) # prompt the user for ingredient and normalize it
ingredient = raw_input("Enter an ingredient you want to search for: ").strip().lower()  # Use raw_input() to read input as a string in Python 2

recipes = get_recipes_by_ingredient(ingredient) # search recipes using the given ingredient

if recipes: # If recipes were found successfully
    vegan_meals = [] # Prepare a list to find out the vegan meals
    non_vegan_meals = [] # Prepare a list to find out the non-vegan meal
    meals = recipes.get("meals", []) # Get the list of meals from the response

    if meals: # If there are meals in the list
        for meal in meals: # iterate over each meal
            meal_id = meal['idMeal'] # Get the meal ID
            meal_details_url = "https://www.themealdb.com/api/json/v1/1/lookup.php?i={}".format(meal_id) # Construct the URL to get meal details
            meal_details = requests.get(meal_details_url).json().get("meals", [])[0] # searching the email details about the meals
            if is_vegan(meal_details): # Check if the meal is vegan
                vegan_meals.append(meal['strMeal']) # Add the meal to the vegan list
            else: # if the meal is not vegan
                non_vegan_meals.append(meal['strMeal']) #Add the meal to the non-vegan list

        print("Recipes with {}:".format(ingredient)) # Print the searched ingredient
        print("\nVegan Meals:") # Print header for vegan meals
        for vegan_meal in vegan_meals: #Iterate over vegan meals
            print("- {}".format(vegan_meal)) # Print each vegan meal

        print("\nNon-Vegan Meals:") #Print header for non-vegan meals
        for non_vegan_meal in non_vegan_meals: #Iterate over non-vegan-meals
            print("- {}".format(non_vegan_meal)) #Print each non-vegan meal
    else:
        print("No recipes found with {}.".format(ingredient)) # Print no recipes
else: #if the request failure
    print("Failed to find recipes.") # Print failure message

