#!/usr/bin/env ruby

# Simple Calculator in Ruby
class Calculator
  def initialize
    puts "Welcome to Simple Calculator!"
    puts "Available operations: +, -, *, /, % (modulo), ^ (power)"
    puts "Type 'quit' or 'exit' to stop"
    puts "-" * 40
  end

  def run
    loop do
      print "Enter expression (e.g., 5 + 3): "
      input = gets.chomp.downcase
      
      break if input == 'quit' || input == 'exit'
      
      if input.empty?
        puts "Please enter an expression."
        next
      end
      
      result = calculate(input)
      if result
        puts "Result: #{result}"
      else
        puts "Invalid expression. Please try again."
      end
      puts "-" * 40
    end
    
    puts "Goodbye!"
  end

  private

  def calculate(expression)
    # Remove spaces and split by operators
    expression = expression.gsub(/\s+/, '')
    
    # Handle power operation (^)
    if expression.include?('^')
      parts = expression.split(/\^/)
      return nil if parts.length != 2
      return parts[0].to_f ** parts[1].to_f
    end
    
    # Handle multiplication and division
    if expression.include?('*') || expression.include?('/') || expression.include?('%')
      # Process * / % operations
      expression = process_multiplication_division(expression)
      return nil if expression.nil?
    end
    
    # Handle addition and subtraction
    if expression.include?('+') || expression.include?('-')
      return process_addition_subtraction(expression)
    end
    
    # If no operators, return the number itself
    expression.to_f
  end

  def process_multiplication_division(expr)
    # Simple regex to find * / % operations
    while expr.match(/(\d+\.?\d*)\s*([*\/%])\s*(\d+\.?\d*)/)
      expr = expr.gsub(/(\d+\.?\d*)\s*([*\/%])\s*(\d+\.?\d*)/) do |match|
        num1 = $1.to_f
        operator = $2
        num2 = $3.to_f
        
        case operator
        when '*'
          num1 * num2
        when '/'
          return nil if num2 == 0
          num1 / num2
        when '%'
          return nil if num2 == 0
          num1 % num2
        end
      end
    end
    expr
  end

  def process_addition_subtraction(expr)
    # Handle negative numbers at the beginning
    if expr.start_with?('-')
      expr = '0' + expr
    end
    
    # Simple regex to find + - operations
    while expr.match(/(\d+\.?\d*)\s*([+-])\s*(\d+\.?\d*)/)
      expr = expr.gsub(/(\d+\.?\d*)\s*([+-])\s*(\d+\.?\d*)/) do |match|
        num1 = $1.to_f
        operator = $2
        num2 = $3.to_f
        
        case operator
        when '+'
          num1 + num2
        when '-'
          num1 - num2
        end
      end
    end
    expr.to_f
  end
end

# Run the calculator
if __FILE__ == $0
  calc = Calculator.new
  calc.run
end
