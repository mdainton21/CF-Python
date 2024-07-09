import pickle

def take_recipe():
    recipe_name = str(input("Enter the name of your recipe: "))
    cooking_time = int(input("How long is the cooking time? (in minutes): "))
    ingredients = list(input("Enter your ingredients, separated by a comma: ").split(", "))
    difficulty = calc_difficulty(cooking_time, ingredients)
    recipe = {
        "name": recipe_name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
        "difficulty": difficulty,
    }
    return recipe

def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10:
        if len(ingredients) < 4:
            difficulty = "Easy"
        elif len(ingredients) >= 4:
            difficulty = "Medium"
    elif cooking_time >= 10:
        if len(ingredients) < 4:
            difficulty = "Intermediate"
        elif len(ingredients) >= 4:
            difficulty = "Hard"
    return difficulty

#User filename input
filename = input("Enter the name of the file you wish to save to: ")

#Checks if filename exists and loads if possible
try:
    file = open(filename, "rb")
    data = pickle.load(file)
    print("File opened successfully")

#Creates a new file if name does not exist
except FileNotFoundError:
    print("No file with that name was found. Creating new file")
    data = {"recipes_list": [], "all_ingredients": []}

#Throws an error if something else went wrong
except:
    print("An error has occurred, please try again.")
    data = {"recipes_list": [], "all_ingredients": []}

#Closes the file
else:
    file.close()

#Extracts data into two variables
finally:
    recipes_list = data["recipes_list"]
    all_ingredients= data["all_ingredients"]


# Starting User Input
n = int(input("Enter the amount of recipes you would like to add: "))

#Stores recipe and cross-checks ingredients list
for i in range(0, n):
    recipe = take_recipe()

    for ingredient in recipe["ingredients"]:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

    recipes_list.append(recipe)

#Updates data dictionary with the new information
data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}

#Open binary file and write to it.
new_file = open(filename, "wb")
pickle.dump(data, new_file)
new_file.close()

print("Recipes have been updated!")
