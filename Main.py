import customtkinter as ctk
from PIL import Image, ImageTk
import emoji

# Set dark theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class TokenType:
    Delimiter = "Delimiter"
    LineBreak = "Line Break"
    Word = "Word"
    Alphanumeric = "Alphanumeric"
    Punctuator = "Punctuation"
    Numeric = "Numeric"
    Whitespace = "Whitespace"


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token: '{self.value}' \t\t Type: '{self.type}'"


def tokenize(input_string):
    tokens = []
    i = 0

    while i < len(input_string):
        ch = input_string[i]

        if ch == ':':
            delimiter = ch
            i += 1
            tokens.append(Token(TokenType.Delimiter, delimiter))

        elif ch == '\n':
            lineBreak = "\\n"
            tokens.append(Token(TokenType.LineBreak, lineBreak))
            i += 1

        elif ch.isalpha():
            word = ""
            while i < len(input_string) and input_string[i].isalpha():
                word += input_string[i]
                i += 1
            tokens.append(Token(TokenType.Word, word))

        elif ch.isalnum():
            alphanumeric = ""
            while i < len(input_string) and input_string[i].isalnum():
                alphanumeric += input_string[i]
                i += 1
            if any(char.isdigit() for char in alphanumeric) and any(char.isalpha() for char in alphanumeric):
                tokens.append(Token(TokenType.Alphanumeric, alphanumeric))
            elif alphanumeric.isdigit():
                tokens.append(Token(TokenType.Numeric, alphanumeric))
            else:
                tokens.append(Token(TokenType.Word, alphanumeric))

        elif ch in '!@#%^&*()-_=+[{]}\\|;\'",<.>/?~`':
            punctuator = ""
            while i < len(input_string) and input_string[i] in '!@#%^&*()-_=+[{]}\\|;\'",<.>/?~`':
                punctuator += input_string[i]
                i += 1
            tokens.append(Token(TokenType.Punctuator, punctuator))

        elif ch == ' ':
            whitespace = ""
            while i < len(input_string) and input_string[i] == ' ':
                whitespace += input_string[i]
                i += 1
            tokens.append(Token(TokenType.Whitespace, whitespace))

        else:
            i += 1

    return tokens


def granular_breakdown(tokens):
    breakdown = []
    for token in tokens:
        chars = ', '.join([f"'{char}'" for char in token.value])
        breakdown.append(f'Token: "{token.value}" --> {chars}')
    return breakdown


class TokenizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Tokenizer")
        self.root.geometry("600x600")

        self.string_tokenizer_label = ctk.CTkLabel(root, text = emoji.emojize("String Tokenizer"), font = ("Helvetica", 18), fg_color=None)
        self.string_tokenizer_label.pack(pady = 15, anchor = "center", expand = True)

        # Input text label and box
        self.input_label = ctk.CTkLabel(root, text="Input Text:", font=("Helvetica", 12))
        self.input_label.pack(pady=10)

        self.input_text = ctk.CTkTextbox(root, wrap="word", width=400, height=100)
        self.input_text.pack(pady=10)

        # Tokenize button with image
        self.image = ctk.CTkImage(light_image = Image.open("token.png"), dark_image = Image.open("white_token.png"), size = (25, 25))
        imahe = self.image

        #self.image = Image.open("token.png") 
        #self.image = self.image.resize((30, 30))
        #self.image_icon = ctk.CTkImage(self.image)

        self.tokenize_button = ctk.CTkButton(root, text="Tokenize", image=imahe, compound="left",
                                             command=self.tokenize_text)
        self.tokenize_button.pack(pady=10)

        # Tokens output label and box
        self.tokens_label = ctk.CTkLabel(root, text="Tokens:", font=("Helvetica", 12))
        self.tokens_label.pack(pady=10)

        self.tokens_output = ctk.CTkTextbox(root, wrap="word", width=400, height=200)
        self.tokens_output.pack(pady=10)
        self.tokens_output.configure(state="disabled")

        # Granular breakdown label and box
        self.breakdown_label = ctk.CTkLabel(root, text="Granular Breakdown:", font=("Helvetica", 12))
        self.breakdown_label.pack(pady=10)

        self.breakdown_output = ctk.CTkTextbox(root, wrap="word", width=400, height=200)
        self.breakdown_output.pack(pady=10)
        self.breakdown_output.configure(state="disabled")

    def tokenize_text(self):
        # Clear previous results
        self.tokens_output.configure(state="normal")
        self.breakdown_output.configure(state="normal")
        self.tokens_output.delete('1.0', 'end')
        self.breakdown_output.delete('1.0', 'end')

        # Get input from text box
        input_string = self.input_text.get("1.0", 'end').strip()

        # Tokenize the input
        tokens = tokenize(input_string)

        # Display tokens
        for token in tokens:
            self.tokens_output.insert('end', f"{token}\n")

        # Display granular breakdown
        breakdown = granular_breakdown(tokens)
        for line in breakdown:
            self.breakdown_output.insert('end', f"{line}\n")

        # Disable text boxes to prevent editing
        self.tokens_output.configure(state="disabled")
        self.breakdown_output.configure(state="disabled")


# Create the main window
root = ctk.CTk()
app = TokenizerApp(root)

# Run the application
root.mainloop()
