# List Creation
recipes_list = []
ingredients_list = []

# Recipe Input Function
def take_recipe():
    recipe_name = input("Enter the name of your recipe: ")
    cooking_time = int(input("How long is the cooking time? (in minutes): "))
    ingredients = list(input("Enter your ingredients, separated by a comma: ").split(", "))
    recipe = {
        "name": recipe_name,
        "cooking_time": cooking_time,
        "ingredients": ingredients
    }
    return recipe

# Starting User Input
n = int(input("Enter the amount of recipes you would like to add: "))

#Stores recipe and cross-checks ingredients list
for i in range(n):
    recipe = take_recipe()

    for ingredient in recipe["ingredients"]:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)

    recipes_list.append(recipe)

#loop to determine the difficulty of recipe
for recipe in recipes_list:
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Easy"
    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Medium"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Intermediate"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Hard"

#loop to display recipe
for recipe in recipes_list:
    print("Recipe: ", recipe["name"])
    print("Cooking Time (min): ", recipe["cooking_time"])
    print("Ingredients:")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty Level: ", recipe["difficulty"])

#Display all ingredients alphabetically
def alpha_ingredients():
    print("Ingredients Available Across All Recipes")
    print("----------------------------------------")
    ingredients_list.sort()
    for ingredient in ingredients_list:
            print(ingredient)

alpha_ingredients()

