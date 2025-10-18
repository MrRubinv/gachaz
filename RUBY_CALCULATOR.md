# Ruby Calculator

A simple command-line calculator written in Ruby.

## Features

- Basic arithmetic operations: `+`, `-`, `*`, `/`
- Modulo operation: `%`
- Power operation: `^`
- Interactive command-line interface
- Error handling for division by zero

## How to Run

### Prerequisites
- Ruby installed on your system

### Running the Calculator
```bash
ruby calculator.rb
```

### Example Usage
```
Enter expression (e.g., 5 + 3): 10 + 5
Result: 15.0

Enter expression (e.g., 5 + 3): 2 ^ 3
Result: 8.0

Enter expression (e.g., 5 + 3): 15 / 3
Result: 5.0

Enter expression (e.g., 5 + 3): 17 % 5
Result: 2.0

Enter expression (e.g., 5 + 3): quit
Goodbye!
```

## Supported Operations

- **Addition**: `5 + 3`
- **Subtraction**: `10 - 4`
- **Multiplication**: `6 * 7`
- **Division**: `15 / 3`
- **Modulo**: `17 % 5`
- **Power**: `2 ^ 8`

## Notes

- Type `quit` or `exit` to stop the calculator
- The calculator handles decimal numbers
- Division by zero will show an error message
- Operations are processed in order: power, multiplication/division/modulo, then addition/subtraction
