def get_int_input(prompt: str, min_value: int = None, max_value: int = None, allow_none: bool = True) -> int | None:
    while True:
        response = input(prompt).strip().lower()

        if allow_none and (response == "" or response in {'none', 'skip'}):
            return None

        if response.isdigit() or (response.startswith('-') and response[1:].isdigit()):
            value = int(response)
            if (min_value is not None and value < min_value) or \
               (max_value is not None and value > max_value):
                print(f"Please enter an integer between {min_value} and {max_value}, or press Enter to skip.")
            else:
                return value
        else:
            print("Invalid input. Please enter an integer" + (", or press Enter to skip." if allow_none else "."))
