import numpy as np
import matplotlib.pyplot as plt

def plot_membership_functions():
    """
    Plots the membership function ranges.
    """
    MAX_FRIGID = 5
    MIN_COLD = -10
    MAX_COLD = 30
    MIN_WARM = 20
    MAX_WARM = 40
    MIN_HOT = 30

    # Define membership functions
    temperature_functions = {
        "frigid": lambda x: max(0, min(1, (MAX_FRIGID - x) / 10)),
        "cold": lambda x: max(0, min(1, (MAX_COLD - x) / 15 if x > 15 else (x - MIN_COLD) / 25)),
        "warm": lambda x: max(0, min(1, (x - MIN_WARM) / 10 if x < 30 else (MAX_WARM - x) / 10)),
        "hot": lambda x: max(0, min(1, (x - MIN_HOT) / 20)),
    }

    # Generate temperature range
    temperatures = np.linspace(-10, 50, 500)

    # Plot membership functions
    plt.figure(figsize=(10, 6))
    for name, func in temperature_functions.items():
        memberships = [func(temp) for temp in temperatures]
        plt.plot(temperatures, memberships, label=name)

    plt.title("Fuzzy Membership Functions")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Membership Degree")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    plot_membership_functions()
