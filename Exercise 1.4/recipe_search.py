import pickle

#Displays a single recipe and it's data
def display_recipe(recipe):
    print("")
    print("Recipe: ", recipe["name"])
    print("Cooking Time (min): ", recipe["cooking_time"])
    print("Ingredients:")
    for ingredient in recipe["ingredients"]:
        print("- ", ingredient)
    print("Difficulty Level: ", recipe["difficulty"])

#Converts ingredients to a list and searches them by number
def search_ingredient(data):
    all_ingredients = enumerate(data["all_ingredients"])
    ingredients_list = list(all_ingredients)

    print("Ingredients List: ")

    for ingredient in ingredients_list:
        print(ingredient[0], ingredient[1])

    try:
        usernumber = int(input("Enter the number of the ingredient you would like to search for: "))
        ingredient_searched = ingredients_list[usernumber][1]

    #Error check for a number
    except ValueError:
        print("Invalid input. Please enter a number.")

    #Error check for a valid number
    except IndexError:
        print("That number does not match any ingredients. Please try again.")

    #Prints all recipes with searched ingredient
    else:
        for recipe in data["recipes_list"]:
            if ingredient_searched in recipe["ingredients"]:
                display_recipe(recipe)

#Main Code
filename = input("Enter the name of the file you wish to save to: ")

#Checks if filename exists and loads if possible
try:
    file = open(filename, "rb")
    data = pickle.load(file)
    print("File opened successfully")

except FileNotFoundError:
    print("No file with that name was found. Creating new file")

#Throws an error if something else went wrong
except:
    print("An error has occurred, please try again.")

#Closes the file and calls search_ingredient function
else:
    file.close()
    search_ingredient(data)

