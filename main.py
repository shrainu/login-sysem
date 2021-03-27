import os
import json
import getpass
from time import sleep


data = None


def clear_screen():
    if os.name == "posix":
        _ = os.system('clear')
    else:
        _ = os.system('cls')


def add_admin(data, username, password):
    data['admins'].append({"username": username, "password": password})
    update_data(data)


def add_user(data, username, password):
    data['users'].append({"username": username, "password": password})
    update_data(data)


def update_data(data):
    with open('user_database.json', 'w') as jsn:
        json.dump(data, jsn, indent=2)


def delete_user(del_user, admin = False):
    data = None

    with open('user_database.json') as jsn:
        data = json.load(jsn)
    
    if admin == False:
        for user in data['users']:
            if user == del_user:
                data['users'].remove(user)
    else:
        for admin in data['admins']:
            if admin == del_user:
                data['admins'].remove(admin)
    
    update_data(data)
    
    return data


def main():
    with open('user_database.json') as jsn:
        data = json.load(jsn)
    clear_screen()
    action = input("Type 'login' or 'register'. Type 'quit' to quit the application. Default is login: ")
    if action == "login" or action == "":
        clear_screen()
        login(data)
    elif action == "register":
        clear_screen()
        register(data)
    elif action == "quit":
        clear_screen()
        action = input("Are you sure do you want to exit? Default is yes. (Y/N): ")
        if action == "N":
            print("Shutdown canceled.")
            sleep(1)
            main()
            return
        else:
            clear_screen()
            print("Shuting down the application.")
            sleep(1)
            quit()
    elif action == "-a -log":
        clear_screen()
        admin_log(data)
    elif action == "-a -log f":
        clear_screen()
        admin_log(data, True)
    else:
        print("Wrong input, please enter a valid input type. ")
        sleep(2.5)
        main()


def admin_log(data, forced = False):
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    login = False
    for admin in data['admins']:
        if admin['username'] ==  username:
            if admin['password'] == password:
                login = True
                break
            else:
                continue
        else:
            continue
    if not login:
        clear_screen()
        print("Wrong username or password.")
        sleep(1.5)
        clear_screen()
        admin_log(data, forced)
        return
    if not forced:
        print("Login successfull. You'll be directed to the admin panel as " + username.upper() + " in 3 seconds.")
        countdown = 3
        for x in range(3):
            print(countdown)
            sleep(1)
            countdown -= 1
        clear_screen()
        print("Directing to the admin panel.")
        sleep(0.5)
        clear_screen()
        admin_panel(data, username)
    else:
        print("Login successfull. You'll be directed to the admin panel as " + username + ".")
        sleep(1)
        clear_screen()
        print("Directing to the admin panel.")
        sleep(0.5)
        clear_screen()
        admin_panel(data, username, True)



def admin_panel(data, admin_name, forced = False, first_call = True):
    if not forced and first_call:
        print("Welcome to admin panel " + admin_name + ".")
        print("Write -a -help to see the admin commands.")
        print("Write -a -q to quit from the admin panel")
        action = input("- " + admin_name + " : ")
        admin_actions(admin_name, action, data)
    elif forced and first_call:
        print("Logged in as " + admin_name + ".")
        action = input("- " + admin_name + " : ")
        admin_actions(admin_name, action, data)
    else:
        action = input("- " + admin_name + " : ")
        admin_actions(admin_name, action, data)

def admin_actions(admin_name, action_name, data):
    if action_name == "-a -help":
            print("-a -help                : See the all admin commands.")
            print("-a -q                   : Logout from the admin panel.")
            print("-a -q f                 : Quit from the application.")
            print("-a -clean               : Clean the panel.")
            print("-a -ls users            : List all the normal users.")
            print("-a -ls admins           : List all the admin users.")
            print("-a -ls -la              : List all the users.")
            print("-a -del user            : Delete a user from database.")
            print("-a -del admin           : Delete a admin from database.")
            print("-a -dg admin            : Downgrade a admin to user.")
            print("-a -ug user             : Upgrade a user to admin.")
    elif action_name == "-a -q":
        clear_screen()
        print("Loged out of the admin account...")
        sleep(1)
        main()
        return
    elif action_name == "-a -q f":
        action = input("Are you sure do you want to exit? Default is yes. (Y/N): ")
        if action == "N":
            print("Shutdown canceled.")
            sleep(1)
        else:
            clear_screen()
            print("Shuting down the application.")
            sleep(1)
            quit()
    elif action_name == "-a -clean":
        clear_screen()
    elif action_name == "-a -ls users":
        iteration = 0
        print("----- # Listing all the users in system # -----")
        for user in data['users']:
            print("\t" + str(iteration) + "- " + user["username"])
            iteration += 1
        print("Total user count is: " + str(len(data['users'])))
    elif action_name == "-a -ls admins":
        iteration = 0
        print("----- # Listing all the admins in system # -----")
        for admin in data['admins']:
            print("\t" + str(iteration) + "- " + admin["username"])
            iteration += 1
        print("Total admin count is: " + str(len(data['admins'])))
    elif action_name == "-a -ls -la":
        iteration = 0
        print("----- # Listing all the users and admins in system # -----")
        for admin in data['admins']:
            print("\t" + str(iteration) + "- " + admin["username"] + "\t" + "admin")
            iteration += 1
        print("----------------------------------------------------------")
        for user in data['users']:
            print("\t" + str(iteration) + "- " + user["username"] + "\tuser")
            iteration += 1
        print("Total user count is: " + str(len(data['users'])))
        print("Total admin count is: " + str(len(data['admins'])))
        print("Total user and admin count is: " + str(len(data['admins']) + len(data['users'])) )
    elif action_name == "-a -del user":
        del_username = input("Enter the username of the user that you want to delete: ")
        user_to_delete = None
        user_found = False
        for user in data['users']:
            if user["username"] == del_username:
                user_to_delete = user
                user_found = True
            else:
                continue
        if not user_found:
            print("There is no user registered under that username.")
            admin_panel(data, admin_name, False, False)
            return
        print("Are you sure that you want to delete this user from database? This can't be undone.")
        decision = input("Default is 'N'. (Y/N): ")
        if decision.upper() == "Y":
            for user in data['users']:
                if user == user_to_delete:
                    new_data = delete_user(user)
                    break
                else:
                    continue
        else:
            clear_screen()
            print("Aborting deletion process...")
            sleep(1)
            admin_panel(data, admin_name, False, False)
            return
        print("User " + del_username + " has successfully deleted from the system.")
        admin_panel(new_data, admin_name, False, False)
        return
    elif action_name == "-a -del admin":
        del_username = input("Enter the username of the admin that you want to delete: ")
        user_to_delete = None
        user_found = False
        for admin in data['admins']:
            if admin["username"] == del_username:
                user_to_delete = admin
                user_found = True
            else:
                continue
        if not user_found:
            print("There is no user registered under that username.")
            admin_panel(data, admin_name, False, False)
            return
        print("Are you sure that you want to delete this admin from database? This can't be undone.")
        decision = input("Default is 'N'. (Y/N): ")
        if decision.upper() == "Y":
            for admin in data['admins']:
                if admin == user_to_delete:
                    new_data = delete_user(admin, True)
                    break
                else:
                    continue
        else:
            clear_screen()
            print("Aborting deletion process...")
            sleep(1)
            admin_panel(data, admin_name, False, False)
            return
        print("Admin " + "'" + del_username + "'" + " has successfully deleted from the system.")
        admin_panel(new_data, admin_name, False, False)
        return
    elif action_name == "-a -dg admin":
        username = input("Enter the username of the admin that you want to make an user: ")
        temp_user = None
        user_found = False
        for admin in data['admins']:
            if admin["username"] == username:
                temp_user = admin
                user_found = True
            else:
                continue
        if not user_found:
            print("There is no admin registered under that username.")
            admin_panel(data, admin_name, False, False)
            return
        password = getpass.getpass("Enter your password: ")
        pass_r = False
        for admin in data['admins']:
            if admin["username"] == admin_name:
                if admin["password"] == password:
                    pass_r = True
                    break
                else:
                    continue
            else:
                continue
        if pass_r == False:
            print("Wrong password!")
            admin_panel(data, admin_name, False, False)
            return
        decision = input("Are you sure you want to make " + "'" + temp_user["username"] + "'" + " a normal user from now on? (Y/N) Default is 'N': ")
        if decision.upper() == "Y":
            add_user(data, temp_user["username"], temp_user["password"])
            new_data = delete_user(temp_user, True)
        else:
            clear_screen()
            print("Aborting downgrading process...")
            sleep(1)
            admin_panel(data, admin_name, False, False)
            return
        clear_screen()
        print("Admin " + "'" + temp_user["username"] + "'" + " is now a normal user from now on.")
        sleep(1)
        print("Returning to the admin panel...")
        sleep(0.5)
        clear_screen()
        admin_panel(new_data, admin_name, False, False)
        return
    elif action_name == "-a -ug user":
        username = input("Enter the username of the user that you want to make an admin: ")
        temp_user = None
        user_found = False
        for user in data['users']:
            if user["username"] == username:
                temp_user = user
                user_found = True
            else:
                continue
        if not user_found:
            print("There is no user registered under that username.")
            admin_panel(data, admin_name, False, False)
            return
        password = getpass.getpass("Enter your password: ")
        pass_r = False
        for admin in data['admins']:
            if admin["username"] == admin_name:
                if admin["password"] == password:
                    pass_r = True
                    break
                else:
                    continue
            else:
                continue
        if pass_r == False:
            print("Wrong password!")
            admin_panel(data, admin_name, False, False)
            return
        decision = input("Are you sure you want to make " + "'" + temp_user["username"] + "'" + " a admin from now on? (Y/N) Default is 'N': ")
        if decision.upper() == "Y":
            add_admin(data, temp_user["username"], temp_user["password"])
            new_data = delete_user(temp_user, False)
        else:
            clear_screen()
            print("Aborting upgrading process...")
            sleep(1)
            admin_panel(data, admin_name, False, False)
            return
        clear_screen()
        print("User " + "'" + temp_user["username"] + "'" + " is now a admin from now on.")
        sleep(1)
        print("Returning to the admin panel...")
        sleep(0.5)
        clear_screen()
        admin_panel(new_data, admin_name, False, False)
        return
    else:
        print("Wrong input " + "'" + action_name + "'" + " is not a known command." )
    admin_panel(data, admin_name, False, False)


def register(data):
    username = input("Please enter a username for you account: ")
    for user in data['users']:
        if user['username'] == username:
            clear_screen()
            print("That username is already taken.")
            register(data)
            return
    for admin in data['admins']:
        if admin['username'] == username:
            clear_screen()
            print("That username is already taken.")
            register(data)
            return
    if username.isidentifier() == False:
        clear_screen()
        print("Wrong input for your username! Username can't start with numbers and cant contain any spaces.")
        register()
        return
    password = getpass.getpass("Please enter a password for your account: ")
    if password.count(" ") > 0:
        clear_screen()
        print("Wrong input for your password! Password can't contain any whitespaces. ")
        register()
        return
    if password == "":
        clear_screen()
        print("Wrong input! You cant leave your password blank. ")
        register()
        return
    re_password = getpass.getpass("Please re-enter your password to confirm it: ")
    if password != re_password:
        clear_screen()
        print("Passwords doesn't match. ")
        register()
        return
    data['users'].append({"username": username, "password": password})
    update_data(data)
    print("You've successfully registered. Welcome to shrain's login system! ")
    action = input("Press 'Enter' to  login and 'q' to quit: ")
    if action == "":
        main()
        return
    elif action == "q":
        quit()
    else:
        main()
        return


def login(data):
    username = input("Username: ")
    user_found = False
    password_match = False
    for user in data['users']:
        if user['username'] == username:
            user_found = True
            break
        if user['username'] != username:
            continue 
    if not user_found:
        clear_screen()
        print("There is no account registered under that username.")
        sleep(2.5)
        clear_screen()
        login(data)
        return
    password = getpass.getpass("Password: ")
    for user in data['users']:
        if user['username'] == username:
            if user['password'] == password:
                password_match = True
                break
            else:
                continue
        else:
            continue
    if not password_match:
        clear_screen()
        print("Wrong password.")
        sleep(1)
        clear_screen()
        login(data)
        return
    print("You've successfully Loged in as " + username + ". Welcome to shrain's login system! ")
    action = input("Press 'Enter' to  login and 'q' to quit: ")
    if action == "":
        login()
        return
    elif action == "q":
        quit()
    else:
        main()
        return


if __name__ == "__main__":
    main()