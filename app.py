import dbcreds
import mariadb
import traceback
import re

def create_blog_post():
    try:
        print(f"\nNew Blog Post by @{username_login}")
        print("------------------------------ \n")
        blog_content_string = input("Enter text here: \n\n")

        blog_content_escape = re.sub(r"\'", r"\\'", blog_content_string)

        cursor.execute(f"INSERT INTO blog_post(username, content) VALUES('{username_login}', '{blog_content_escape}')")
        conn.commit()

        print(f"\n@{username_login}'s blog post was successfully uploaded. \n")
    except:
        print("\nAn error occured. Failed to upload post. \n")
        traceback.print_exc()

def view_all_blog_posts():
    try:
        cursor.execute("SELECT * FROM blog_post")
        all_blog_posts = cursor.fetchall()

        if(len(all_blog_posts) == 0):
            print("\nNo posts found. \n")
        else:
            print("\nAll Posts")
            print("--------- \n")
            for i in range (len(all_blog_posts)):
                for j in range (len(all_blog_posts[i])):
                    print(f"{all_blog_posts[i][j]} \n")
                print("------------------------------ \n")
    except:
        print("\nAn error has occured. Failed to view all posts. \n")
        traceback.print_exc()

def get_selection():
    while(True):
        try:
            print("\nPlease select one of the two options: \n1: Write a new post \n2: See all other posts \n")
            selection = int(input("Please enter your selection: "))
            if(selection == 1):
                create_blog_post()
            elif(selection == 2):
                view_all_blog_posts()
            else:
                print("\nInvalid selection. \n")
            break
        except ValueError:
            print("\nInvalid data entry. Expected a numeric value. \n")
            traceback.print_exc()
        except:
            print("\n An error has occured. \n")
            traceback.print_exc()

def run_application():
    while(True):
        check_user_exit = input("Would you like to exit the Blog Site? Y/N: ")
        if(check_user_exit == "Y" or check_user_exit == "y"):
            print("\nThank you for visiting the Blog Site!")
            break
        elif(check_user_exit == "N" or check_user_exit == "n"):
            get_selection()
        else:
            print("\nInvalid selection.")  

def check_user_login():
    while(True):
        print("\nWelcome to the Blog Site! \n")
        print("Login")
        print("----- \n")
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        
        try:
            cursor.execute("SELECT username, password FROM users")
            database_user_login_info = cursor.fetchall()

            for i in range (len(database_user_login_info)):
                if(database_user_login_info[i][0] == username and database_user_login_info[i][1] == password):
                    print("\nYou have successfully logged in.")
                    return database_user_login_info[i][0]
        except:
            print(f"\nAn error has occured. Failed to retrieve @{username}'s login information. \n")
            traceback.print_exc()  

try:
    conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
    cursor = conn.cursor()

    username_login = check_user_login()
    get_selection()
    run_application()

except:
    print("\nAn error in the database has occured. \n")
    traceback.print_exc()

try:
    cursor.close()
except:
    print("\nAn error has occured. Failed to close cursor. \n")
    traceback.print_exc()

try:
    conn.close()
except:
    print("\nAn error has occured. Failed to close connection. \n")
    traceback.print_exc()