def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    output = []
    stack = []
    
    for char in expression:
        if char.isalnum():  # Operand
            output.append(char)
        elif char in precedence:  # Operator
            while stack and precedence.get(stack[-1], 0) >= precedence[char]:
                output.append(stack.pop())
            stack.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # Remove '('

    while stack:
        output.append(stack.pop())

    return ''.join(output)

def infix_to_prefix(expression):
    expression = expression[::-1]  # Reverse the expression
    expression = expression.replace('(', 'temp').replace(')', '(').replace('temp', ')')
    postfix = infix_to_postfix(expression)
    return postfix[::-1]

def postfix_to_infix(expression):
    stack = []
    
    for char in expression:
        if char.isalnum():
            stack.append(char)
        else:
            op1 = stack.pop()
            op2 = stack.pop()
            stack.append(f"({op2}{char}{op1})")

    return stack[0]

def prefix_to_infix(expression):
    stack = []
    
    # Traverse the prefix expression from right to left
    for char in reversed(expression):
        if char.isalnum():  # If operand, push to stack
            stack.append(char)
        else:  # If operator, pop two operands and create infix expression
            op1 = stack.pop()
            op2 = stack.pop()
            stack.append(f"({op1}{char}{op2})")

    return stack[0]

def evaluate_prefix(expression):
    stack = []
    
    for char in reversed(expression):
        if char.isdigit():  # If operand, push to stack
            stack.append(int(char))
        else:  # If operator, pop two operands and apply operator
            op1 = stack.pop()
            op2 = stack.pop()
            if char == '+':
                stack.append(op1 + op2)
            elif char == '-':
                stack.append(op1 - op2)
            elif char == '*':
                stack.append(op1 * op2)
            elif char == '/':
                stack.append(op1 / op2)

    return stack[0]

def evaluate_infix(expression):
    try:
        return eval(expression)  # Using Python's eval function
    except Exception as e:
        return f"Error: {e}"

def evaluate_postfix(expression):
    stack = []
    
    for char in expression:
        if char.isdigit():
            stack.append(int(char))
        else:
            op2 = stack.pop()
            op1 = stack.pop()
            if char == '+':
                stack.append(op1 + op2)
            elif char == '-':
                stack.append(op1 - op2)
            elif char == '*':
                stack.append(op1 * op2)
            elif char == '/':
                stack.append(op1 / op2)

    return stack[0]