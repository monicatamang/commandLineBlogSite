import dbcreds
import mariadb
import traceback
import re

# Creating a function that allow users to upload blog posts
def create_blog_post():
    while(True):
        # Creating a try block to catch runtime errors associated with uploading the user's blog post to the database
        try:
            # Prompting the user to enter their blog post content
            print(f"\nNew Blog Post by @{username_login}")
            print("------------------------------ \n")
            blog_content_string = input("Enter text here: \n\n")

            # If the user enters no content, print an error message to the user and prompt them to re-enter their blog post entry
            if(blog_content_string == ""):
                print("Invalid entry. Please re-enter your entry.")
            # If the user enters a valid entry, upload their blog post to the database
            else:
                # Using the regular expression library in python, escape all apostrophes found in the user's input
                # Subtitute each apostrophe in the user's input and replace it with a backlash and single quote to escape it then store the "escaped" user input as a variable
                # Note: I was running into issues where whenever a user would enter words that contain apostrophes (i.e., can't, don't, etc.), mariadb would intepret the apostrophe as a metacharacter rather than a string which would result in an error and would fail to upload the user's post
                blog_content_escape = re.sub(r"\'", r"\\'", blog_content_string)

                # Add the user's username and blog post content into the database and commit the changes
                cursor.execute(f"INSERT INTO blog_post(username, content) VALUES('{username_login}', '{blog_content_escape}')")
                conn.commit()

                # If the user's blog post was added to the database, print an "upload" success message to the user
                print(f"\n@{username_login}'s blog post was successfully uploaded.\n")

                # The loop will break and the remaining code in the get_selection function will run
                break
        except:
            # If an error has occured, print an error message to the user and the traceback
            print("\nAn error occured. Failed to upload post.\n")
            traceback.print_exc()

# Creating a function that shows the user all of the blog posts
def view_all_blog_posts():
    # Creating a try block that catches runtime errors associated with getting the blog posts from the database
    try:
        # Get the username and content from the blog_post table in the database and store the information as a variable
        cursor.execute("SELECT username, content FROM blog_post")
        all_blog_posts = cursor.fetchall()
        
        # If there are no blog posts, print a message to the user
        if(len(all_blog_posts) == 0):
            print("\nNo posts found.\n")
        # If there are one or more blog posts, print the username and content of each blog post in the database
        else:
            print("\nAll Posts")
            print("--------- \n")
            for i in range (len(all_blog_posts)):
                for j in range (len(all_blog_posts[i])):
                    print(f"{all_blog_posts[i][j]}\n")
                print("------------------------------\n")
    except:
        # If an error has occured, print an error message to the user and the traceback
        print("\nAn error has occured. Failed to view all posts.\n")
        traceback.print_exc()

# Creating a function that shows users the menu options
def get_selection():
    while(True):
        # Creating a try block to catch runtime error associated with user's entering their selection
        try:
            # Printing the menu options
            print("\nPlease select one of the two options: \n1: Write a new post \n2: See all other posts\n")

            # Storing the user's selection as a variable and converting it into an integer
            selection = int(input("Please enter your selection: "))
            # If the user wants to create a blog post, call the create_blog_post function
            if(selection == 1):
                create_blog_post()
                # After the function runs, the loop will break and the remaining code in the run_application function will run which will give the user the option to leave the site
                break
            # If the user wants to view all blog posts, call the view_all_blog_posts function
            elif(selection == 2):
                view_all_blog_posts()
                # After the function runs, the loop will break and the remaining code in the run_application function will run which will give the user the option to leave the site
                break
            # If the user enters an invalid selection other than 1 or 2, print an error message to the user and prompt the user to make their selection again
            else:
                print("\nInvalid selection.\n")
                continue
        except ValueError:
            # If the user enters anything but a numeric datatype, print an error message to the user and the traceback
            print("\nInvalid data entry. Expected a numerical value.\n")
            traceback.print_exc()
        except:
            # If any other error occurs, print an error message to the user and the traceback
            print("\n An error has occured.\n")
            traceback.print_exc()

# Creating a function that continues to run the application
def run_application():
    while(True):
        # Prompting the user if they would like to leave the site
        check_user_exit = input("Would you like to exit the Blog Site? Y/N: ")

        # If the user wants to exits the site, print a message to the user and end the application
        if(check_user_exit == "Y" or check_user_exit == "y"):
            print("\nThank you for visiting the Blog Site!")
            break
        # If the user wants to continue being on the site, show the menu options
        elif(check_user_exit == "N" or check_user_exit == "n"):
            get_selection()
        # If the user enters an invalid selection, print an error message to the user and prompt the user to enter their selection again
        else:
            print("\nInvalid selection.")  

# Creating a function that validates a user's login credentials
def check_user_login():
    # Printing a welcome message to the user
    print("\nWelcome to the Blog Site!")

    while(True):
        # Prompting the user to enter their username and password
        print("\nLogin")
        print("-----\n")
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        
        # Creating a try block to catch runtime errors associated with getting the user's login credentials from the database
        try:
            # Get the user's username and password from the users table in the database and store the information as a variable
            cursor.execute("SELECT username, password FROM users")
            database_user_login_info = cursor.fetchall()

            # Since the database returns the information as a list of tuples, for every list, verify the user's login credentials
            for i in range (len(database_user_login_info)):
                # If the user's username provided matches with the username stored in the database and the user's password provided matches with the password stored in the database, print a login success message to the user and return the user's username
                if(database_user_login_info[i][0] == username and database_user_login_info[i][1] == password):
                    print("\nYou have successfully logged in.")
                    return database_user_login_info[i][0]

            # If the user's login credentials do not match with the databases records, prompt the user to log in again
            continue
        except:
            # If an error has occurred, print an error message to the user and the traceback
            print(f"\nAn error has occured. Failed to retrieve @{username}'s login information.\n")
            traceback.print_exc()  

# Creating a try block to catch runtime errors associated with connecting with the database and creating a cursor
try:
    # Setting up the connection with the database
    conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)

    # Creating a cursor
    cursor = conn.cursor()

    # Authenticating the user's login information and storing the user's login username as a variable
    username_login = check_user_login()

    # If the user has logged in successfully, call the functions to show the user their options on the Blog Site and continue running the application
    get_selection()
    run_application()
except:
    # If an error has occurred, print an error message to the user and the traceback
    print("\nAn error in the database has occured.\n")
    traceback.print_exc()

# If there is an error with connecting to the database or creating a cursor, the code will still proceed to close the cursor and database connection

# Creating a try block to catch runtime errors associated with closing the cursor
try:
    # Closing the cursor
    cursor.close()
except:
    # If an error has occurred, print an error message to the user and the traceback
    print("\nAn error has occured. Failed to close cursor.\n")
    traceback.print_exc()

# Creating a try block to catch runtime errors associated with closing the database connection
try:
    # Closing the database connection
    conn.close()
except:
    # If an error has occurred, print an error message to the user and the traceback
    print("\nAn error has occured. Failed to close connection.\n")
    traceback.print_exc()