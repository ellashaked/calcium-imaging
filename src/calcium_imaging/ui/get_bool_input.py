def get_bool_input(prompt: str) -> bool:
    true_values = {'y', 'yes', 'true', '1'}
    false_values = {'n', 'no', 'false', '0'}

    while True:
        response = input(prompt).strip().lower()
        if response in true_values:
            return True
        elif response in false_values:
            return False
        else:
            print("Invalid input. Please enter a value like: y, yes, true, 1, n, no, false, or 0.")
