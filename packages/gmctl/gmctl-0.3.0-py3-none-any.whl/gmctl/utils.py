from tabulate import tabulate

def print_table(data, tablefmt="simple"):
    """
    Prints a list of dictionaries as a table.

    Args:
        data: A list of dictionaries where each dictionary represents a row in the table.
        tablefmt: The table format to use. Defaults to "grid". Other popular formats include "plain", "pipe", "html", "latex", and more.
    """
    if not data:
        print("No data to display.")
        return

    headers = data[0].keys()
    rows = [list(item.values()) for item in data]

    print(tabulate(rows, headers=headers, tablefmt=tablefmt))