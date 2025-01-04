from DrawScript.Core.drawScriptLexer import Token, TokenType
from DrawScript.Nodes.binOpNode import BinOpNode
from DrawScript.Nodes.numberNode import NumberNode

from enum import Enum

class DrawScriptParserNew:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token: Token = None
        self.advance()

    def advance(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        return self.current_token
    
    def factor(self) -> NumberNode:
        token: Token = self.current_token

        if token.type in (TokenType.INT, TokenType.FLOAT):
            self.advance()
            return NumberNode(token)

    def term(self) -> BinOpNode:
        return self.bin_op(self.factor, (TokenType.MUL, TokenType.DIV))
    
    def expr(self):
        return self.bin_op(self.term, (TokenType.PLUS, TokenType.MINUS))
    
    def bin_op(self, func, ops) -> BinOpNode:
        left = func()

        while self.current_token.type in ops:
            op_token = self.current_token
            self.advance()
            right = func()
            left = BinOpNode(left, op_token, right)

        return left

    def parse(self):
        res = self.expr()
        return res