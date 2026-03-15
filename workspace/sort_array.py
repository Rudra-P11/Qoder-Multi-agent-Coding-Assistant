def sort_user_array():
    while True:
        user_input = input("Enter numbers separated by commas (e.g., 5,2,8,1): ")
        try:
            # Split the input string by commas and strip whitespace from each part
            numbers_str = [s.strip() for s in user_input.split(',')]
            # Convert string parts to integers
            numbers = [int(num) for num in numbers_str if num]
            
            if not numbers:
                print("No valid numbers entered. Please try again.")
                continue

            numbers.sort()
            print("Sorted array:", numbers)
            break # Exit the loop if input is successful
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    sort_user_array()
