def fuzzify(value: float, membership_functions: dict) -> dict:
    """
    Maps a crisp input to its degree of membership in each fuzzy set.

    Parameters:
        value (float): The crisp input value.
        membership_functions (dict): A dictionary of fuzzy sets with their membership functions.

    Returns:
        dict: Degrees of membership for each fuzzy set.
    """
    memberships = {name: func(value) for name, func in membership_functions.items()}
    return memberships

def apply_rules(memberships: dict, rules: list[tuple]) -> dict:
    """
    Applies fuzzy rules to compute the fuzzy output.

    Parameters:
        memberships (dict): Degrees of membership for each fuzzy set.
        rules (list of tuples): Fuzzy rules in the form (input_set, output_set).

    Returns:
        dict: Combined fuzzy output for each output set.
    """
    output_memberships = {}
    for input_set, output_set in rules:
        output_memberships[output_set] = max(output_memberships.get(output_set, 0), memberships[input_set])
    return output_memberships

def defuzzify(output_memberships: dict, output_functions: dict) -> float:
    """
    Converts fuzzy output into a crisp value using the centroid method.

    Parameters:
        output_memberships (dict): Degrees of membership for each output set.
        output_functions (dict): Functions representing the output sets.

    Returns:
        float: The defuzzified crisp output value.
    """
    numerator = 0
    denominator = 0
    for name, degree in output_memberships.items():
        centroid = output_functions[name]()
        numerator += degree * centroid
        denominator += degree
    return numerator / denominator if denominator != 0 else 0

def main():
    MAX_FRIGID = 5
    MIN_COLD = -10
    MAX_COLD = 30
    MIN_WARM = 20
    MAX_WARM = 40
    MIN_HOT = 30

    # Define membership functions
    temperature_functions = {
        "frigid": lambda x: max(0, min(1, (MAX_FRIGID - x) / 10)),
        "cold": lambda x: max(0, min(1, (MAX_COLD - x) / 20 if x > 15 else (x - MIN_COLD) / 20)),
        "warm": lambda x: max(0, min(1, (x - MIN_WARM) / 10 if x < 30 else (MAX_WARM - x) / 10)),
        "hot": lambda x: max(0, min(1, (x - MIN_HOT) / 20)),
    }

    # Define centroid functions
    fan_speed_functions = {
        "off": lambda: 0,
        "low": lambda: 20,
        "medium": lambda: 50,
        "high": lambda: 80,
    }

    # Define rules
    rules = [
        ("frigid", "off"),
        ("cold", "low"),
        ("warm", "medium"),
        ("hot", "high"),
    ]

    # Crisp input value
    temperature = 0

    # Fuzzify input
    memberships = fuzzify(temperature, temperature_functions)
    print(memberships)

    # Apply rules
    output_memberships = apply_rules(memberships, rules)
    print(output_memberships)

    # Defuzzify output
    fan_speed = defuzzify(output_memberships, fan_speed_functions)

    print(f"Input Temperature: {temperature}°C")
    print(f"Fan Speed: {fan_speed}")

# Example usage
if __name__ == "__main__":
    main()