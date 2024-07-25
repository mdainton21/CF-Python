import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password')

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    ingredients VARCHAR(255),
    cooking_time INT,
    difficulty VARCHAR(20)
)''')

#Main Menu Loop
def main_menu(conn, cursor):
    choice = ""
    while (choice != "quit"):
        print("\nMain Menu")
        print("\n===================================")
        print("Pick a choice:")
        print("   1. Create a new recipe")
        print("   2. Search for a recipe by ingredient")
        print("   3. Update an existing recipe")
        print("   4. Delete a recipe")
        print("\n   Type 'quit' to exit the program.")
        choice = input("\nYour choice: ")

        if choice == "1":
            create_recipe(conn, cursor)
        elif choice == "2":
            search_recipe(conn, cursor)
        elif choice == "3":
            update_recipe(conn, cursor)
        elif choice == "4":
            delete_recipe(conn, cursor)
        elif choice == "quit":
            break
        else:
            print("Invalid choice. Please try again.")

#Creates Recipe and adds their ingredients to the ingredients list
def create_recipe(conn, cursor):
    recipe_ingredients = []
    name = str(input("Enter the name of your recipe: "))
    cooking_time = int(input("How long is the cooking time? (in minutes): "))
    ingredient = input("Enter the ingredients needed: ")
    recipe_ingredients.append(ingredient)
    recipe_ingredients_str = ", ".join(recipe_ingredients)

    difficulty = calc_difficulty(cooking_time, recipe_ingredients)

    sql = "INSERT INTO recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    val = (name, recipe_ingredients_str, cooking_time, difficulty)

    cursor.execute(sql, val)
    conn.commit()
    print("Recipe saved into the database.")


# Difficulty Calc
def calc_difficulty(cooking_time, recipe_ingredients):
    
    if cooking_time < 10:
        if len(recipe_ingredients) < 4:
                difficulty = "Easy"
        elif len(recipe_ingredients) >= 4:
                difficulty = "Medium"
    elif cooking_time >= 10:
        if len(recipe_ingredients) < 4:
                difficulty = "Intermediate"
        elif len(recipe_ingredients) >= 4:
                difficulty = "Hard"
    return difficulty

#Search Recipe Function
def search_recipe(conn, cursor):
    #Unique Ingredients set to avoid duplicate ingredients
    unique_ingredients = set()
    cursor.execute("SELECT ingredients FROM recipes")
    results = cursor.fetchall()
    for recipe in results:
        #For loop to split the string
        for recipe_ingredients in recipe:
            recipe_ingredients = recipe_ingredients.split(", ")
            unique_ingredients.update(recipe_ingredients)
    all_ingredients = list(enumerate(unique_ingredients))
    print("\nAll ingredients list:")
    print("========================")
    for index, tup in enumerate(all_ingredients):
        print(str(tup[0]) + ". " + tup[1])

    #User input for Ingredient selection
    try:
        search_ingredient = int(
            input(
                "\nEnter the number corresponding to the ingredient you wish to search for: "
            )
        )
        search_ingredient = all_ingredients[search_ingredient][1]
        print("\nYou selected the ingredient:", search_ingredient)

    except IndexError:
        print("That number does not match any ingredients. Please try again.")

    except ValueError:
        print("Invalid input. Please enter a number.")

    except:
         print("An error hass occured, please try again.")

    else:
        print("The following recipes contain", search_ingredient, ":")
        print("=================================")

        cursor.execute(
            "SELECT * FROM recipes WHERE ingredients LIKE %s",
            ("%" + search_ingredient + "%",),
        )
        results = cursor.fetchall()
        for recipe in results:
            print("\nID:", recipe[0])
            print("Name:", recipe[1])
            print("Ingredients:", recipe[2])
            print("Cooking time:", recipe[3], "minutes")
            print("Difficulty:", recipe[4])

#A function to view all recipes which will be used for the update/delete recipe functions.
def view_recipes(conn, cursor):
    print("Full recipe List:")
    print("===================")

    cursor.execute(
            "SELECT * FROM recipes",
    )
    results = cursor.fetchall()
    for row in results:
        print("\nID:", row[0])
        print("Name:", row[1])
        print("Ingredients:", row[2])
        print("Cooking time:", row[3], "minutes")
        print("Difficulty:", row[4])

#A function to update recipe data
def update_recipe(conn, cursor):
     # Get all recipes from database
    view_recipes(conn, cursor)
    recipe_id = int(input("\nEnter the number of the recipe you want to update: "))
    cursor.execute("SELECT name FROM recipes WHERE id = %s", (recipe_id,))
    result = cursor.fetchone()

    #error check
    if result is None:
        print("Recipe with ID %s does not exist." % recipe_id)
        return
    recipe_name = result[0]

    print("\n1. Name")
    print("2. Ingredients")
    print("3. Cooking Time")
    column_update = int(input("\nEnter the number of the category you would like to update:"))


    # Update the name of the recipe
    if column_update == 1:
        new_name = str(input("\nEnter the new name: ").title())
        sql = "UPDATE recipes SET name = %s WHERE id = %s"
        val = (new_name, recipe_id)
        cursor.execute(sql, val)
        conn.commit()
        print("Recipe updated successfully.")


    # Update the ingredients
    elif column_update == 2:
        ingredients_input = input("Enter the new ingredients for %s : " % recipe_name)
        new_ingredients = ", ".join(
            [ingredient.strip().title() for ingredient in ingredients_input.split(",")]
        )

        # Update the ingredients in the database
        sql = "UPDATE recipes SET ingredients = %s WHERE id = %s"
        val = (new_ingredients, recipe_id)
        cursor.execute(sql, val)

        # Grabbing the cooking time
        cursor.execute("SELECT cooking_time FROM recipes WHERE id = %s", (recipe_id,))
        result = cursor.fetchone()
        current_cooking_time = result[0]

        # Calculating Difficulty
        new_difficulty = calc_difficulty(current_cooking_time, new_ingredients)
        sql = "UPDATE recipes SET difficulty = %s WHERE id = %s"
        val = (new_difficulty, recipe_id)
        cursor.execute(sql, val)
        conn.commit()
        print("Recipe updated and difficulty calculated.")

    #Update the cooking time
    elif column_update == 3:
        # Ask user for new cooking time
        new_cooking_time = int(input("\nEnter the new cooking time (in minutes): "))
        sql = "UPDATE recipes SET cooking_time = %s WHERE id = %s"
        val = (new_cooking_time, recipe_id)
        cursor.execute(sql, val)

        # Update the difficulty in the database
        cursor.execute("SELECT ingredients FROM recipes WHERE id = %s", (recipe_id,))
        result = cursor.fetchone()
        current_ingredients = result[0]
        new_difficulty = calc_difficulty(new_cooking_time, current_ingredients)
        sql = "UPDATE recipes SET difficulty = %s WHERE id = %s"
        val = (new_difficulty, recipe_id)
        cursor.execute(sql, val)
        conn.commit()
        print("Recipe updated successfully.")

    else:
        print("Invalid input. Please try again.")

def delete_recipe(conn, cursor):
    view_recipes(conn, cursor)
    try:
        delete_recipe_id = int(input("\nPlease enter the number of the recipe you would like to delete: "))
    
    except ValueError:
        print("Invalid Input. Please enter a number.")

    else:
        sql = "DELETE FROM recipes WHERE id = %s"
        val = (delete_recipe_id,)
        cursor.execute(sql, val)
        conn.commit()
        print("Recipe deleted successfully.")
    

main_menu(conn, cursor)
print("Thank you for using the Recipe App!")

