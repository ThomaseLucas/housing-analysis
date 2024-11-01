import pandas as pd
import numpy
import matplotlib.pyplot as plt
import os
import dotenv
import customtkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Questions to answer:
# 1. What are the top 10 cheapest cities to live in this U.S.?
# 2. How much more expensive are housing prices in the U.S. compared to 10 years ago?

# Load the data from the csv file
data = pd.read_csv('Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv')
canvas = None

# Finding the cheapest cities to buy a house in a specific state
def find_cheapest_cities_in_state(state):
    """The function returns the 10 cheapest cities to buy a house in a specific state. Based on the input parameter of which state."""
    cheapest_cities = data.loc[data['StateName'] == state, ['RegionName', '2024-09-30']].nsmallest(10, '2024-09-30')
    return cheapest_cities

def create_dict_of_prices():
    #This function creates a dictionary of prices since 2014 based on the median price throughout the US.
    prices = {}
    for year in range(2014, 2024):
        prices[year] = data[f"{year}-09-30"].median()
    return prices

def make_pandas_graph(prices, root):
    # This function creates a pandas graph of the prices from 2014 to 2024
    global canvas
    prices_series = pd.Series(prices)
    fig, ax = plt.subplots()
    prices_series.plot(ax=ax, color='blue', linewidth=3)
    ax.set_title('US Housing Price Trend from 2014 to 2024')
    ax.set_xlabel('Year')
    ax.set_ylabel('Median Price')

    if canvas is not None:
        canvas.get_tk_widget().destroy()
        canvas = None

    # Create a canvas to display the graph in tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side='right',padx=20, pady=20)

def display_price_trend(root):
    prices = create_dict_of_prices()
    make_pandas_graph(prices, root)

def display_cheapest_cities(state_var, result_label):
    state_choice = state_var.get()
    cheapest_cities = find_cheapest_cities_in_state(state_choice)
    result_text = "\n\n".join([f"{row['RegionName']}: ${row['2024-09-30']:,.2f}" for index, row in cheapest_cities.iterrows()])
    result_label.configure(text=result_text, font=("Helvetica", 25, "bold"))

def close_trend(root):
    global canvas
    if canvas is not None:
        canvas.get_tk_widget().destroy()
        canvas = None
    root.after_cancel("1956071560256")

def create_tkinter_window():
    """The function creates a tkinter window with a title, a dropdown menu for states, and an exit button."""
    # Initialize the customtkinter window
    root = tk.CTk()
    root.title("Housing Price Analysis")
    root.attributes('-fullscreen', True)

    #create a top frame for top-positioned buttons
    top_frame = tk.CTkFrame(root)
    top_frame.pack(side='top', fill='x', pady=10)

    #Create a left frame for left-positioned buttons
    left_frame = tk.CTkFrame(root)
    left_frame.pack(side='left', fill='y', padx=10) 

    # List of all 50 state abbreviations
    states = [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
    ]

    # Add a dropdown menu for states
    state_var = tk.StringVar(value=states[0])
    state_dropdown = tk.CTkOptionMenu(top_frame, variable=state_var, values=states)
    state_dropdown.pack(side='left', pady=20, padx=20)

    # Add a button to trigger the display of the 10 cheapest cities
    show_button = tk.CTkButton(left_frame, text="Show Cheapest Cities", command=lambda: display_cheapest_cities(state_var, result_label))
    show_button.pack(pady=20, padx=20)

    # Add a button to display the price trend
    trend_button = tk.CTkButton(top_frame, text="Display Price Trend", command=lambda: display_price_trend(root))
    trend_button.pack(side='left', pady=20, padx=20)

    end_trend_button = tk.CTkButton(top_frame, text="End Trend", command=lambda: close_trend(root))
    end_trend_button.pack(side='left', pady=20, padx=20)

    # Add a label to display the results
    result_label = tk.CTkLabel(root, text="")
    result_label.pack(pady=20, padx=20)

    # Add a way to exit the application
    exit_button = tk.CTkButton(left_frame, text="Exit", command=root.destroy)
    exit_button.pack(pady=20, padx=20)


    # Run the tkinter main loop
    root.mainloop()

def main():
    """The main function that runs the program."""
    create_tkinter_window()


if __name__ == "__main__":
    main()
