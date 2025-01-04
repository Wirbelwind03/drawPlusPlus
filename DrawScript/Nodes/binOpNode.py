class BinOpNode:
    def __init__(self, left_token, op_token, right_token):
        self.left_token = left_token
        self.op_token = op_token
        self.right_token = right_token

    def __repr__(self):
        return f'({self.left_token} {self.op_token} {self.right_token})'