import re  # Library for regular expressions
from config import DEBUG

# Define regular expressions for each token type
TOKEN_SPECIFICATION = [
    ('NEWLINE',             r'\n'),                      # New line
    ('WHITESPACE',          r'[ \t]+'),                  # Spaces and tabs
    ('MULTILINE_COMMENT',   r'/\*[\s\S]*?\*/'),          # Multi-line comment
    ('COMMENT',             r'//.*'),                    # Single-line comment
    ('NUMBER',              r'-?\d+(\.\d+)?|\.\d+'),     # Integer or decimal numbers (positive or negative)
    ('STRING',              r'"[^"\n]*"'),               # String literals in quotes (no newlines)
    ('BOOLEAN',             r'\b(true|false)\b'),        # Boolean values
    ('IDENTIFIER',          r'[A-Za-z_]\w*'),            # Identifiers
    ('ACCESS_OPERATOR',     r'\.'),                      # Dot operator (separated from other operators)
    ('OPERATOR',            r'\+|\-|\*|\/|\%|==|!=|<=|>=|<|>|&&|\|\||!'),  # Operators
    ('DELIMITER',           r'\(|\)|\{|\}|;|,|\:'),      # Delimiters
    ('ASSIGN',              r'='),                       # Assignment operator
    ('MISMATCH',            r'.'),                       # Unrecognized character
]

# Language keywords
KEYWORDS = [
    'var', 'function', 'if', 'else', 'while', 'for',
    'copy', 'animate', 'to', 'Cursor', 'return', 'do',
]

class DrawScriptTokenizer:
    def __init__(self):
        """
        Constructor for the tokenizer class.
        In this case, 'cursors' is a dictionary meant to store cursor information
        (not used in this snippet, but available for potential extensions).
        """
        self.cursors = {}  # Dictionary to store cursors (not used in this code)

    def tokenize(self, code):
        """
        This method takes a string 'code' containing the source code of the draw++ language.
        It returns a list of tokens and a corresponding list of errors.
        
        Each token is represented as a dictionary with keys like 'type', 'value', and 'line'.
        Each error is represented by an integer (0 if no error, 1 if there was an error with the token).
        """

        # Compile all regular expressions into one pattern
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION)
        # Use MULTILINE so that '^' and '$' anchors match lines appropriately if needed
        get_token = re.compile(tok_regex, re.MULTILINE).match

        # Variables for tokenization
        pos = 0          # Current position in the code string
        tokens = []      # List of produced tokens
        errors = []      # List of error flags (0 or 1)
        line_number = 1  # Start line numbering at 1

        # Start matching tokens from the beginning of the code
        mo = get_token(code, pos)  # 'mo' is a Match object
        while mo is not None:
            kind = mo.lastgroup    # The type of the token (group name)
            value = mo.group(kind) # The actual text matched by this token

            if DEBUG:
                # Debug: Print the current token information
                # 'repr(value)' adds quotes; [1:-1] removes them for tidier output
                print(f"Matched {kind}: '{repr(value)[1:-1]}' at line {line_number}")

            if kind == 'NEWLINE':
                # If we encounter a newline, increment the line counter
                line_number += 1
            elif kind == 'WHITESPACE':
                # Whitespace is ignored (not stored as a token)
                pass
            elif kind == 'MULTILINE_COMMENT':
                # For a multi-line comment, count the number of newlines it contains
                line_number += value.count('\n')
            elif kind == 'COMMENT':
                # Single-line comment is ignored
                pass
            elif kind == 'NUMBER':
                # Convert the string to a float; if it's an integer value, round it
                number = float(value)
                if float.is_integer(number):
                    number = round(number)
                tokens.append({'type': kind, 'value': number, 'line': line_number})
                errors.append(0)
            elif kind == 'STRING':
                # Remove the surrounding quotes
                tokens.append({'type': kind, 'value': value[1:-1], 'line': line_number})
                errors.append(0)
            elif kind == 'BOOLEAN':
                tokens.append({'type': kind, 'value': value, 'line': line_number})
                errors.append(0)
            elif kind == 'IDENTIFIER':
                # If the identifier is a language keyword, change its type to KEYWORD
                if value in KEYWORDS:
                    kind = 'KEYWORD'
                tokens.append({'type': kind, 'value': value, 'line': line_number})
                errors.append(0)
            elif kind in {'OPERATOR', 'DELIMITER', 'ASSIGN', 'ACCESS_OPERATOR'}:
                # Operators, delimiters, assignment signs, or dot operators
                tokens.append({'type': kind, 'value': value, 'line': line_number})
                errors.append(0)
            elif kind == 'MISMATCH':
                # Unrecognized token: record an error
                tokens.append({'type': 'UNKNOWN', 'value': value, 'line': line_number})
                errors.append(1)

            # Move to the end of the current match and look for the next token
            pos = mo.end()
            mo = get_token(code, pos)

        # If we haven't reached the end of the string, treat the remaining text as errors
        if pos != len(code):
            remaining = code[pos:]
            for char in remaining:
                if char == '\n':
                    line_number += 1
                tokens.append({'type': 'UNKNOWN', 'value': char, 'line': line_number})
                errors.append(1)

        print("\nTokenization complete.\n")
        return tokens, errors
