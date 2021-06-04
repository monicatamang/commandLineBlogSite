import dbcreds
import mariadb
import traceback

def create_blog_post():
    try:
        print(f"New Blog Post by {username}")
        print("------------------------------")
        blog_content = input("Enter text here: \n")

        cursor.execute(f"INSERT INTO blog_post(username, content) VALUES('{username}', '{blog_content}')")
        conn.commit()
        print(f"{username}'s blog post was successfully uploaded. \n")
        print(f"A blog post by {username}")
        print("------------------------------")
        print(f"{blog_content}")
    except:
        print("An error occured. Failed to upload post.")
        traceback.print_exc()

def view_all_blog_posts():
    try:
        cursor.execute("SELECT * FROM blog_post")
        all_blog_posts = cursor.fetchall()

        if(len(all_blog_posts) == 0):
            print("No posts found.")
        else:
            print("\nAll Posts")
            print("--------- \n")
            for i in range (len(all_blog_posts)):
                for j in range (len(all_blog_posts[i])):
                    print(f"{all_blog_posts[i][j]} \n")
                print("------------------------------")
    except:
        print("An error has occured. Failed to view all posts.")
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
                print("Invalid selection.")
            break
        except ValueError:
            print("Invalid data entry. Expected a numerical value.")
            traceback.print_exc()
        except:
            print("An error has occured.")
            traceback.print_exc()

def get_username():
    print("Welcome to the Blog Site!")
    while(True):
        test_username = input("Please enter your username: ")
        if(len(test_username) <= 100):
            return test_username
        else:
            print("Username exceeds 100 characters.")

username = get_username()

try:
    conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
    cursor = conn.cursor()
    get_selection()
except:
    print("An error in the database has occured.")
    traceback.print_exc()

try:
    print("Closing cursor.")
    cursor.close()
except:
    print("An error has occured. Failed to close cursor.")
    traceback.print_exc()

try:
    print("Closing connection.")
    conn.close()
except:
    print("An error has occured. Failed to close connection.")
    traceback.print_exc()