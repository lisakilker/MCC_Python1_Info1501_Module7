#Program that allows a user to filter through a file called data.csv and save the results to their desired file name
#Added extra "\n" to make the results easier to read in the terminal

#Library imports
import csv
import os

#Function to list all CSV files in the current directory
def list_csv_files():
    #Returns a list of all files that end with .csv
    return [f for f in os.listdir() if f.endswith('.csv')]

def main():
    #Loops to prompt the user for a file name until a valid one is provided
    while True:
        file_name = input("\nWhat's the name of the file that you'd like to search through?: ").strip()
        if not file_name:
            file_name = "data.csv"
        elif not file_name.endswith(".csv"):
            file_name += ".csv"
        
        if os.path.exists(file_name):
            break
        else:
            #If the user enters an invalid file name, this will give the user a list of the available files to choose from
            print(f"\nThe file '{file_name}' does not exist. Here are the available files:")
            csv_files = list_csv_files()
            if csv_files:
                print("\n".join(csv_files))
            else:
                print("\nNo CSV files found in the current directory.")

    data = []

    try:
        #Open and read the CSV file into a list of dictionaries
        with open(file_name, mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)

        while True:
            #Display the menu options
            print("\nMenu options:\n 1: Age (min to max) \n 2: City \n 3: Last Name \n 4: First Name \n 5: ID (min to max)")
            
            #Asks the user to choose which option
            user_input = input("\nEnter a number to filter by or type 'Q' to quit: ").strip().upper()

            #If/else statements that will be used based on the user's input from above
            if user_input == "Q":
                print("\nTerminating program. Goodbye!\n")
                break
            elif user_input == "1":
                filtered_age = filter_by_age(data)
                handle_filtered_data(filtered_age)
            elif user_input == "2":
                filtered_city = filter_by_city(data)
                handle_filtered_data(filtered_city)
            elif user_input == "3":
                filtered_last_name = filter_by_last_name(data)
                handle_filtered_data(filtered_last_name)
            elif user_input == "4":
                filtered_first_name = filter_by_first_name(data)
                handle_filtered_data(filtered_first_name)
            elif user_input == "5":
                filtered_id = filter_by_id(data)
                handle_filtered_data(filtered_id)
            else:
                #Prints if user enters invalid option
                print("\nInvalid input. Please enter a number between 1 and 5 or type 'Q' to quit.")
                continue

            #Asks the user if they want to return to the main menu or quit
            while True:
                start_over = input("\nDo you want to return to the main menu? Y/N: ").strip().upper()
                if start_over == "Y":
                    break
                elif start_over == "N":
                    print("\nTerminating program. Goodbye!\n")
                    return
                else:
                    print("\nInvalid input. Please enter 'Y' or 'N'.")

    #Error displayed if main file is not found
    except FileNotFoundError:
        print(f"\nThe file {file_name} was not found.")

#Function to handle the filtered data: print it and give the user the option to save it to a new file/override existing file
def handle_filtered_data(filtered_data):
    if not filtered_data:
        print("\nNo results")
    else:
        #Prints the data in a pretty format in the terminal while maintaining the format from the original CSV file
        print_pretty(filtered_data)
        #Asks the user if they want to save the results into a new CSV file
        save_option = input("\nDo you want to save these results? Y/N: ").strip().upper()
        while save_option not in ["Y", "N"]:
            save_option = input("\nInvalid input. Please enter 'Y' or 'N': ").strip().upper()
        if save_option == "Y":
            while True:
                #Asks the user what they'd like to name their file with the results from their search
                filename = input("\nWhat should the name of the new file be? ").strip()
                #If the user does not enter a .csv extension, this will auto add it for them
                if not filename.endswith(".csv"):
                    filename += ".csv"
                #If the file name already exists, this asks the user if they want to override the file
                if os.path.exists(filename):
                    overwrite = input(f"\nThe file '{filename}' already exists. Do you want to overwrite it? Y/N: ").strip().upper()
                    while overwrite not in ["Y", "N"]:
                        overwrite = input("\nInvalid input. Please enter 'Y' or 'N': ").strip().upper()
                    if overwrite == "Y":
                        break
                    else:
                        continue
                else:
                    break
            save_to_csv(filtered_data, filename)

#Function to print the filtered data in a pretty format in the terminal - note, csv files display the same as original data.csv file
def print_pretty(data):
    for row in data:
        print(f"\nUser ID: {row['id']}")
        print(f"Name: {row['first_name']} {row['last_name']}")
        print(f"Age: {row['age']}")
        print(f"City: {row['city']}")
        print(f"Phone Number: {row['phone_number']}")
        print("-----------------")

#Function to save the filtered data to a CSV file
def save_to_csv(data, filename):
    if not data:
        print("\nNo data to save.")
        return

    try:
        keys = data[0].keys()
        with open(filename, mode='w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        print(f"\nData saved to {filename}")
    except Exception as e:
        print(f"\nAn error occurred while saving to {filename}: {e}")

#Function to filter data by age or age range
def filter_by_age(data):
    while True:
        try:
            min_age = int(input("\nEnter minimum age: "))
            if min_age < 0:
                print("\nMinimum age cannot be less than 0. Please enter a valid minimum age.")
                continue
            break
        except ValueError:
            print("\nPlease enter a valid number for the minimum age.")

    while True:
        try:
            max_age = int(input("\nEnter maximum age: "))
            if min_age > max_age:
                print("\nMinimum age cannot be greater than maximum age.")
                continue
            break
        except ValueError:
            print("\nPlease enter a valid number for the maximum age.")

    if min_age == max_age:
        print(f"\nFiltered results for age = {min_age}:")
        filtered_data = [row for row in data if int(row["age"]) == min_age]
    else:
        print(f"\nFiltered results for age between {min_age} and {max_age}:")
        filtered_data = [row for row in data if min_age <= int(row["age"]) <= max_age]

    return filtered_data

#Function to filter data by city
def filter_by_city(data):
    while True:
        city = input("\nEnter the city to filter by: ").strip().title()
        if city:
            filtered_data = [row for row in data if row["city"].title() == city]
            break
        else:
            print("\nCity cannot be empty. Please enter a valid city.")

    return filtered_data

#Function to filter data by last name
def filter_by_last_name(data):
    while True:
        last_name = input("\nEnter the last name to filter by: ").strip().title()
        if last_name:
            filtered_data = [row for row in data if row["last_name"].title() == last_name]
            break
        else:
            print("\nLast name cannot be empty. Please enter a valid last name.")

    return filtered_data

#Function to filter data by first name
def filter_by_first_name(data):
    while True:
        first_name = input("\nEnter the first name to filter by: ").strip().title()
        if first_name:
            filtered_data = [row for row in data if row["first_name"].title() == first_name]
            break
        else:
            print("\nFirst name cannot be empty. Please enter a valid first name.")

    return filtered_data

#Function to filter data by ID or ID range
def filter_by_id(data):
    while True:
        try:
            min_id = int(input("\nEnter minimum ID: "))
            if min_id < 0:
                print("\nMinimum ID cannot be less than 0. Please enter a valid minimum ID.")
                continue
            break
        except ValueError:
            print("\nPlease enter a valid number for the minimum ID.")

    while True:
        try:
            max_id = int(input("\nEnter maximum ID: "))
            if min_id > max_id:
                print("\nMinimum ID cannot be greater than maximum ID.")
                continue
            break
        except ValueError:
            print("\nPlease enter a valid number for the maximum ID.")

    if min_id == max_id:
        print(f"\nFiltered results for ID = {min_id}: ")
        filtered_data = [row for row in data if int(row["id"]) == min_id]
    else:
        print(f"\nFiltered results for IDs between {min_id} and {max_id}:")
        filtered_data = [row for row in data if min_id <= int(row["id"]) <= max_id]

    return filtered_data

#Calls the main function
if __name__ == "__main__":
    main()