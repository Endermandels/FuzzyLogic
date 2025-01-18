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

def clamp(degree: float, mx: float = 1, mn: float = 0) -> float:
    ''' Clamp degree between mn and mx '''
    return max(mn, min(mx, degree))

def main():
    '''
    Important data for determining landing, touch and go, or other:
    - Altitude - feet difference from ground station (float)
    - WoW - weight on wheels (bool)
    - Timestamp - time of acknowledgement (datetime)

    The timestamp is hard to work with.  Might consider making a "time since last landed" datum instead?
    That way, if the plane just landed, the variable gets reset.
    If the plane goes airborne shortly afterward, that's a touch and go.
    However, after a certain point, it's just a landing.
    When the plane goes airborne, it doesn't matter that the time since last landed is a large number.
    Could even cap the time since last landed.

    Crisp output values:
    "landed"
    "touch-and-go"
    "airborne"
    '''

    # Define membership functions for crisp inputs
    altitude_functions = {
        "on_ground": lambda x: clamp((500 - x) / 500),
        "low_altitude": lambda x: clamp((x - 400) / 600 if x <= 1000 else (2000 - x) / 1000),
        "high_altitude": lambda x: clamp((x - 1500) / 1000),
    }
    wow_functions = {
        "no_weight": lambda x: 1 if x == 0 else 0,
        "weight": lambda x: 1 if x == 1 else 0,
    }
    time_functions = {
        "recent": lambda t: clamp((60 - t) / 60),
        "moderate": lambda t: clamp((t - 30) / 30 if t <= 90 else (120 - t) / 30),
        "long": lambda t: clamp((t - 90) / 60),
    }



    # Define centroid functions for crisp outputs
    status_functions = {
        "landed": lambda: 0,
        "touch-and-go": lambda: 50,
        "airborne": lambda: 100,
    }

    # Define rules
    rules = [
        ("on_ground", "landed"),
        ("weight", "landed"),
        ("no_weight", "airborne"),
        ("low_altitude", "touch-and-go"),
        ("recent", "landed"),
        ("moderate", "touch-and-go"),
        ("long", "airborne"),
    ]

    # Example crisp inputs
    altitude = 800  # in feet
    weight_on_wheels = 0  # 0: no weight, 1: weight
    time_since_last_landed = 45  # in seconds

    # Fuzzify inputs
    altitude_memberships = fuzzify(altitude, altitude_functions)
    print('altitude:\t', altitude_memberships)
    wow_memberships = fuzzify(weight_on_wheels, wow_functions)
    print('wow:\t\t', wow_memberships)
    time_memberships = fuzzify(time_since_last_landed, time_functions)
    print('time:\t\t', time_memberships)

    # Combine all memberships into one dictionary for rule evaluation
    all_memberships = {**altitude_memberships, **wow_memberships, **time_memberships}

    # Apply rules
    output_memberships = apply_rules(all_memberships, rules)
    print('output:\t\t', output_memberships)

    # Defuzzify output
    status = defuzzify(output_memberships, status_functions)

    # Interpret the defuzzified result
    if status < 25:
        classification = "landed"
    elif status < 75:
        classification = "touch-and-go"
    else:
        classification = "airborne"

    print(f"Input Altitude: \t\t{altitude} feet")
    print(f"Weight on Wheels: \t\t{weight_on_wheels}")
    print(f"Time Since Last Landed: \t{time_since_last_landed} seconds")
    print(f"Plane Status: \t\t\t{classification}")


# Example usage
if __name__ == "__main__":
    main()