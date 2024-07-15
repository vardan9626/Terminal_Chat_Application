def print_col(text, color=None, bold=False, underline=False, italic=False, blink=False, end="\n"):
    '''
    This function is used to print the text with various formatting options like color, bold, underline, italic, and blink.
    '''
    try:
        code_st = "\033["  # Start of the ANSI escape code
        code_end = "\033[0m"  # End of the ANSI escape code
        color_codes = {
            "black": 30,
            "red": 31,
            "green": 32,
            "yellow": 33,
            "blue": 34,
            "magenta": 35,
            "cyan": 36,
            "white": 37
        }
        text_decoration = {
            "bold": 1,
            "underline": 4,
            "italic": 3,
            "blink": 5
        }
        if color:
            code_st += f"{color_codes[color]};"
        if bold:
            code_st += f"{text_decoration['bold']};"
        if underline:
            code_st += f"{text_decoration['underline']};"
        if italic:
            code_st += f"{text_decoration['italic']};"
        if blink:
            code_st += f"{text_decoration['blink']};"
        if code_st[-1] == ";":
            code_st = code_st[:-1]  # Remove the last semicolon
        code_st += "m"
        
        print(f"{code_st}{text}{code_end}", end=end)
    except:
        print(text, end=end)
    
if __name__ == "__main__":
    # Example usage
    print_col("This is normal text")
    print_col("This is bold red text", "red", bold=True)
    print_col("This is underlined magenta text", "magenta", underline=True)
    print_col("This is italic cyan text", "cyan", italic=True)
    print_col("This is blinking blue text", "blue", blink=True)
