#Codes a program to add the color "red" to a pre-existing dictionary, loops through keys and values and displays results

def main():
    #Pre-existing dictionary for a car
    car  = dict(Brand = "Ford", Model = "Mustang", Year = 1964)

    #Prints the dictionary with the additional color
    car_brand = car.get("Brand")
    print(f"The car brand is {car_brand}")
    
    #Adds the color "red" to the car dictionary
    car["Color"] = "Red"

    #Loops through the dictionary and prints all the values
    print("Car values:")
    for value in car.values():
        print(value)

    #Loops through the dictionary and prints all the keys
    print("Car keys:")
    for key in car.keys():
        print(key)

#Calls the main function
if __name__ == "__main__":
    main()