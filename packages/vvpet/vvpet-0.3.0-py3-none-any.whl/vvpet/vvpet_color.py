class color:
    PINK = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

if __name__ == "__main__":
    print(f"PINK {color.PINK} ahoj {color.END}")
    print(f"BLUE {color.BLUE} ahoj {color.END}")
    print(f"CYAN {color.CYAN} ahoj {color.END}")
    print(f"GREEN {color.GREEN} ahoj {color.END}")
    print(f"YELLOW {color.YELLOW} ahoj {color.END}")
    print(f"RED {color.RED} ahoj {color.END}")