#Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Integer, String, Column

#Connecting SQLAlchemy with the Database
engine = create_engine("mysql://cf-python:password@localhost/my_database")

Base = declarative_base()

#Creating Recipe class using Base class
class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(225))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return "<ID: " + str(self.id) + ", Name: " + self.name + ", Difficulty: " + self.difficulty + ">"
    
    def __str__(self): 
        output = (
            "-----------------------------------"
            "\nName: " + self.name
            + "\nCooking Time(min): " + str(self.cooking_time)
            + "\nIngredients: " + str(self.ingredients)
            + "\nDifficulty: " + str(self.difficulty)
            + "\n-----------------------------------" + "\n"
        )
        return output

#Table Creation
Base.metadata.create_all(engine)

#Intitializing the Session
Session = sessionmaker(bind=engine)
session = Session()

#Difficulty Calc
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
    else:
          print("An error occured while calculating difficulty. Please try again.")
    
    return difficulty


#Retrieve Ingredients and convert to a list
def return_ingredients_as_list():
    results = session.query(Recipe.ingredients).all()
    all_ingredients = []
    for ingredients_list in results:
        #For loop to split the string
        for recipe_ingredients in ingredients_list:
            recipe_ingredients_raw = recipe_ingredients.split(", ")
            all_ingredients.extend(recipe_ingredients_raw)

    #Remove duplicate ingredients
    all_ingredients = list(dict.fromkeys(all_ingredients))

    #Print ingredient list
    Format_ingredients = list(enumerate(all_ingredients))
    print("\nAll ingredients list:")
    print("========================")
    for index, tup in enumerate(Format_ingredients):
        print(str(tup[0]) + ". " + tup[1])

    return Format_ingredients


#Create recipe function
def create_recipe():
    recipe_ingredients = []
    #Name Error Check
    while True:
        name = str(input("Enter the name of your recipe: "))
        if len(name) < 50:
             name=str(name)
             break
        else:
             print("Recipe name is too long, please try again")
    
    #Cooking Time Error Check
    while True:
        cooking_time = input("How long is the cooking time? (in minutes): ")
        if cooking_time.isnumeric():
            cooking_time = int(cooking_time)
            break
        else:
            print("Invalid input. Please enter a number.")

    #Ingredient Number Error Check
    while True:
        ingredient_number = input("Enter the number of ingredients needed: ")
        if ingredient_number.isnumeric():
            ingredients_number = int(ingredient_number)
            break
        else:
            print("Invalid input. Please try again.")

    #Ingredient Input
    for i in range(ingredients_number):
        ingredient = input("Enter an ingredient: ").title().strip()
        recipe_ingredients.append(ingredient)

    recipe_ingredients_str = ", ".join(recipe_ingredients)

    #Difficulty Calculation
    difficulty = calc_difficulty(cooking_time, recipe_ingredients)

    #Add inputs and commit to database
    new_recipe = Recipe(
        name=name,
        cooking_time=cooking_time,
        ingredients=recipe_ingredients_str,
        difficulty=difficulty,
    )
    session.add(new_recipe)
    session.commit()
    print("Recipe saved into the database.")


#View all Recipes
def view_all_recipes():
    all_recipes = []
    all_recipes = session.query(Recipe).all()

    #Check if Recipe list is empty
    if len(all_recipes) == 0:
        print("There are no recipes in the database.")
        return None
    else:
        #Print Recipe
        print("\nRecipe List:")
        for recipe in all_recipes:
            print(recipe)


#Search Recipe by ingredients
def search_by_ingredients():
    #Checks for 0 recipe count
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database")
        return None
    
    else:
        #Call Ingredient List function
        Format_ingredients=return_ingredients_as_list()

        try:
            #User Ingredient selection 
            ingredient_searched_nber = input("\nEnter the corresponding number of the ingredients you would like \nto search. You can select multiple ingredients, and the numbers \nshould be separated by a space in this case: ")
            ingredients_nber_list_searched = ingredient_searched_nber.split(" ")

            #Creates a list of the selected ingredients, and prints it
            search_ingredients = []
            for ingredient_searched_nber in ingredients_nber_list_searched:
                ingredient_searched_index = int(ingredient_searched_nber)
                ingredient_searched = Format_ingredients[ingredient_searched_index][1]

                search_ingredients.append(ingredient_searched.strip())
            print(
                "\nRecipes containing the following ingredient(s): ",
                search_ingredients,
                )

            #Create a list of conditions that is used to filter the recipes
            conditions = []
            for ingredient in search_ingredients:
                like_term = "%" + ingredient + "%"
                condition = Recipe.ingredients.like(like_term)
                conditions.append(condition)

            #Retrieve filtered recipes from database
            searched_recipes = session.query(Recipe).filter(*conditions).all()
        except:
                print(
                    "An unexpected error occurred. Make sure to select a number from the list."
                )

        else:
                # Print the list of filtered recipes
                for recipe in searched_recipes:
                    print(recipe)


#Fetch recipes function
def fetch_recipes():
    results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()

    print("\nList of available recipes: ")
    for recipe in results:
        print("\nId: ", recipe[0])
        print("Name: ", recipe[1])


#Edit Recipe Function
def edit_recipe():
    #Checks for 0 recipe count
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database")
        return None
    
    else:
        #Fetch recipe list and input for user
        fetch_recipes()            
        edit_id = int(
            (input("\nEnter the id number of the recipe you want to edit: "))
        )

        #Checking if selected id is in the list
        recipes_id_tup_list = session.query(Recipe).with_entities(Recipe.id).all()
        recipes_id_list = []
        for recipe_tup in recipes_id_tup_list:
            recipes_id_list.append(recipe_tup[0])
        #If ID is not in the list abort
        if edit_id not in recipes_id_list:
            print("Not a valid ID, please select an ID from the list.")
        
        else:
            # Get the recipe object to edit
            recipe_to_edit = (
                session.query(Recipe).filter(Recipe.id == edit_id).one()
            )

            #User selects which attribute to edit
            print("\n1. Name")
            print("2. Cooking Time")
            print("3. Ingredients")
            column_for_update = int(
                input(
                    "\nPlease enter the corresponding number for the attribute you want to update: "
                )
            )

            # Update the name of the recipe
            if column_for_update == 1:
                print("You want to update the name of the recipe")
                while True:
                    updated_name = str(input("Enter the new name of your recipe: "))
                    if len(updated_name) < 50:
                        updated_name=str(updated_name)
                        break
                    else:
                        print("Recipe name is too long, please try again")
                session.query(Recipe).filter(Recipe.id == edit_id).update(
                    {Recipe.name: updated_name}
                )
                session.commit()
                print("Name updated successfully!")

            # Update the cooking time of the recipe
            elif column_for_update == 2:
                print("You want to update the cooking time of the recipe")
                while True:
                    updated_cooking_time = input("How long is the new cooking time? (in minutes): ")
                    if updated_cooking_time.isnumeric():
                        updated_cooking_time = int(updated_cooking_time)
                        break
                    else:
                        print("Invalid input. Please enter a number.")
                session.query(Recipe).filter(Recipe.id == edit_id).update(
                    {Recipe.cooking_time: updated_cooking_time}
                )
                #Update Difficulty
                updated_difficulty = calc_difficulty(updated_cooking_time, recipe_to_edit.ingredients)
                recipe_to_edit.difficulty = updated_difficulty
                session.commit()
                print("Cooking Time and Difficulty updated successfully!")

            # Update the ingredients of the recipe
            elif column_for_update == 3:
                print("You want to update the ingredients of the recipe")
                new_recipe_ingredients = []
                while True:
                    new_ingredient_number = input("Enter the number of ingredients needed: ")
                    if new_ingredient_number.isnumeric():
                        new_ingredients_number = int(new_ingredient_number)
                        break
                    else:
                        print("Invalid input. Please try again.")

                #Ingredient Input
                for i in range(new_ingredients_number):
                    updated_ingredient = input("Enter an ingredient: ").title().strip()
                    new_recipe_ingredients.append(updated_ingredient)

                    recipe_ingredients_str = ", ".join(new_recipe_ingredients)

                
                session.query(Recipe).filter(Recipe.id == edit_id).update(
                    {Recipe.ingredients: recipe_ingredients_str}
                )
                #Update Difficulty and commit ingredients/difficulty to database
                updated_difficulty = calc_difficulty(recipe_to_edit.cooking_time, new_recipe_ingredients)
                recipe_to_edit.difficulty = updated_difficulty
                session.commit()
                print("Ingredients and Difficulty updated successfully!")

            else:
                print("Wrong input, please try again.")


#Delete Recipe Function
def delete_recipe():
    fetch_recipes()
    delete_id = int(
            (input("\nEnter the id number of the recipe you want to delete: "))
        )

    #Checking if selected ID is in the list
    recipes_id_tup_list = session.query(Recipe).with_entities(Recipe.id).all()
    recipes_id_list = []
    for recipe_tup in recipes_id_tup_list:
        recipes_id_list.append(recipe_tup[0])
    #If ID is not in the list abort
    if delete_id not in recipes_id_list:
        print("Not a valid ID, please select an ID from the list.")
        
    else:
        recipe_to_delete = (
            session.query(Recipe).filter(Recipe.id == delete_id).one()
            )
        #Final Warning before deletion
        print("\nWARNING: You are about to delete the following recipe: ")
        print(recipe_to_delete)

        #Deletion Confirmation
        final_check = input("\nAre you sure you want to delete this recipe?\nSelect 'yes' or 'no': ")
        if final_check == "yes":
            session.delete(recipe_to_delete)
            session.commit()
            print("Recipe deleted successfully")
        elif final_check == "no":
            print("Recipe was not deleted")
        else:
            print("Invalid Input. Returning to main menu")

def main_menu():
    while True:
        print("\nWelcome to the Recipe App!")
        print("================================")
        print("\nMain Menu")
        print("================================")
        print("\nPlease Select an Option:")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for recipes by ingredients")
        print("4. Edit a recipe")
        print("5. Delete a recipe")
        print("6. Exit\n")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_by_ingredients()
        elif choice == "4":
            edit_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")


main_menu()
session.close()




