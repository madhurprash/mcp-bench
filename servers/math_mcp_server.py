from mcp.server.fastmcp import FastMCP
import math
import statistics
from typing import List, Union, Tuple, Any

mcp = FastMCP("Math")

@mcp.tool()
def add(a: Any, b: Any) -> Union[int, float]:
    """Add two numbers."""
    # Convert to float first to handle potential type mismatches
    a_float = float(a)
    b_float = float(b)
    result = a_float + b_float
    # Return int if result is a whole number, otherwise float
    return int(result) if result.is_integer() else result

@mcp.tool()
def subtract(a: Any, b: Any) -> Union[int, float]:
    """Subtract b from a."""
    # Convert to float first to handle potential type mismatches
    a_float = float(a)
    b_float = float(b)
    result = a_float - b_float
    # Return int if result is a whole number, otherwise float
    return int(result) if result.is_integer() else result

@mcp.tool()
def multiply(a: Any, b: Any) -> Union[int, float]:
    """Multiply two numbers."""
    # Convert to float first to handle potential type mismatches
    a_float = float(a)
    b_float = float(b)
    result = a_float * b_float
    # Return int if result is a whole number, otherwise float
    return int(result) if result.is_integer() else result

@mcp.tool()
def divide(a: Any, b: Any) -> Union[int, float]:
    """Divide a by b."""
    # Convert to float first to handle potential type mismatches
    a_float = float(a)
    b_float = float(b)
    
    if b_float == 0:
        raise ValueError("Cannot divide by zero")
    
    result = a_float / b_float
    # Return int if result is a whole number, otherwise float
    return int(result) if result.is_integer() else result

@mcp.tool()
def sqrt(n: Any) -> float:
    """Calculate the square root of a number."""
    n_float = float(n)
    if n_float < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return math.sqrt(n_float)

@mcp.tool()
def power(base: Any, exponent: Any) -> Union[int, float]:
    """Calculate base raised to the exponent power."""
    # Convert to float first to handle potential type mismatches
    base_float = float(base)
    exponent_float = float(exponent)
    result = base_float ** exponent_float
    # Return int if result is a whole number, otherwise float
    return int(result) if result.is_integer() else result

@mcp.tool()
def log(n: Any, base: Any = 10) -> float:
    """Calculate logarithm of n with given base (default: base 10)."""
    n_float = float(n)
    base_float = float(base)
    
    if n_float <= 0 or base_float <= 0 or base_float == 1:
        raise ValueError("Invalid input for logarithm")
    
    return math.log(n_float, base_float)

@mcp.tool()
def trigonometry(function: str, angle: Any, unit: str = "degrees") -> float:
    """Calculate trigonometric functions.
    
    Args:
        function: One of 'sin', 'cos', 'tan'
        angle: The angle
        unit: 'degrees' or 'radians'
    """
    angle_float = float(angle)
    
    if unit.lower() == "degrees":
        angle_rad = math.radians(angle_float)
    elif unit.lower() == "radians":
        angle_rad = angle_float
    else:
        raise ValueError("Unit must be 'degrees' or 'radians'")
    
    if function.lower() == "sin":
        return math.sin(angle_rad)
    elif function.lower() == "cos":
        return math.cos(angle_rad)
    elif function.lower() == "tan":
        return math.tan(angle_rad)
    else:
        raise ValueError("Function must be 'sin', 'cos', or 'tan'")

@mcp.tool()
def geometry(shape: str, **kwargs) -> float:
    """Calculate geometric properties.
    
    Args:
        shape: The geometric shape ('circle', 'rectangle', 'triangle', etc.)
        **kwargs: Parameters specific to the shape
    """
    shape = shape.lower()
    # Convert all numeric kwargs to float
    for key, value in kwargs.items():
        if isinstance(value, (int, float, str)) and not isinstance(value, bool):
            try:
                kwargs[key] = float(value)
            except ValueError:
                pass
    
    if shape == "circle":
        if "radius" in kwargs:
            radius = kwargs["radius"]
            return math.pi * radius ** 2
        elif "diameter" in kwargs:
            diameter = kwargs["diameter"]
            return math.pi * (diameter / 2) ** 2
        else:
            raise ValueError("Circle requires radius or diameter")
    elif shape == "rectangle":
        if "length" in kwargs and "width" in kwargs:
            return kwargs["length"] * kwargs["width"]
        else:
            raise ValueError("Rectangle requires length and width")
    elif shape == "triangle":
        if "base" in kwargs and "height" in kwargs:
            return 0.5 * kwargs["base"] * kwargs["height"]
        elif "sides" in kwargs and len(kwargs["sides"]) == 3:
            # Heron's formula
            a, b, c = [float(side) for side in kwargs["sides"]]
            s = (a + b + c) / 2
            return math.sqrt(s * (s - a) * (s - b) * (s - c))
        else:
            raise ValueError("Triangle requires base and height or three sides")
    else:
        raise ValueError(f"Unsupported shape: {shape}")

@mcp.tool()
def percentage(part: Any = None, whole: Any = None, percentage: Any = None) -> float:
    """Calculate percentage.
    
    Usage:
    - percentage(part=25, whole=200) -> 12.5 (what percent is part of whole)
    - percentage(part=25, percentage=10) -> 250 (what is the whole if part is percentage%)
    - percentage(percentage=25, whole=200) -> 50 (what is part if it's percentage% of whole)
    """
    # Convert inputs to float if they're not None
    part_float = float(part) if part is not None else None
    whole_float = float(whole) if whole is not None else None
    percentage_float = float(percentage) if percentage is not None else None
    
    if whole_float is not None and percentage_float is None:
        return (part_float / whole_float) * 100
    elif whole_float is not None and part_float is None:
        return (percentage_float / 100) * whole_float
    elif percentage_float is not None and part_float is not None:
        return (part_float * 100) / percentage_float
    else:
        raise ValueError("Invalid combination of arguments")

@mcp.tool()
def conversion(value: Any, from_unit: str, to_unit: str) -> float:
    """Convert between different units.
    
    Supported conversions:
    - Length: km, m, cm, mm, mile, yard, foot, inch
    - Weight: kg, g, mg, pound, ounce
    - Temperature: celsius, fahrenheit, kelvin
    - Time: hour, minute, second
    """
    value_float = float(value)
    
    # Conversion factors to SI units
    length_to_meter = {
        "km": 1000, "m": 1, "cm": 0.01, "mm": 0.001,
        "mile": 1609.344, "yard": 0.9144, "foot": 0.3048, "inch": 0.0254
    }
    
    weight_to_kg = {
        "kg": 1, "g": 0.001, "mg": 0.000001,
        "pound": 0.45359237, "ounce": 0.028349523125
    }
    
    time_to_second = {
        "hour": 3600, "minute": 60, "second": 1
    }
    
    # Check if it's a temperature conversion
    if from_unit.lower() in ["celsius", "fahrenheit", "kelvin"] and to_unit.lower() in ["celsius", "fahrenheit", "kelvin"]:
        return temperature_conversion(value_float, from_unit, to_unit)
    
    # Length conversion
    if from_unit.lower() in length_to_meter and to_unit.lower() in length_to_meter:
        return value_float * length_to_meter[from_unit.lower()] / length_to_meter[to_unit.lower()]
    
    # Weight conversion
    if from_unit.lower() in weight_to_kg and to_unit.lower() in weight_to_kg:
        return value_float * weight_to_kg[from_unit.lower()] / weight_to_kg[to_unit.lower()]
    
    # Time conversion
    if from_unit.lower() in time_to_second and to_unit.lower() in time_to_second:
        return value_float * time_to_second[from_unit.lower()] / time_to_second[to_unit.lower()]
    
    raise ValueError(f"Unsupported conversion from {from_unit} to {to_unit}")

@mcp.tool()
def temperature_conversion(value: Any, from_unit: str, to_unit: str) -> float:
    """Convert between temperature units: Celsius, Fahrenheit, Kelvin."""
    value_float = float(value)
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    # Convert to Celsius first
    if from_unit == "celsius":
        celsius = value_float
    elif from_unit == "fahrenheit":
        celsius = (value_float - 32) * 5/9
    elif from_unit == "kelvin":
        celsius = value_float - 273.15
    else:
        raise ValueError(f"Unsupported temperature unit: {from_unit}")
    
    # Convert from Celsius to target unit
    if to_unit == "celsius":
        return celsius
    elif to_unit == "fahrenheit":
        return celsius * 9/5 + 32
    elif to_unit == "kelvin":
        return celsius + 273.15
    else:
        raise ValueError(f"Unsupported temperature unit: {to_unit}")

@mcp.tool()
def gcd(a: Any, b: Any) -> int:
    """Calculate the greatest common divisor of two integers."""
    a_int = int(float(a))
    b_int = int(float(b))
    return math.gcd(a_int, b_int)

@mcp.tool()
def lcm(a: Any, b: Any) -> int:
    """Calculate the least common multiple of two integers."""
    a_int = int(float(a))
    b_int = int(float(b))
    return abs(a_int * b_int) // math.gcd(a_int, b_int)

@mcp.tool()
def round_number(value: Any, decimal_places: Any = 0) -> Union[int, float]:
    """Round a number to specified decimal places."""
    value_float = float(value)
    decimal_places_int = int(decimal_places)
    return round(value_float, decimal_places_int)

@mcp.tool()
def factorial(n: Any) -> int:
    """Calculate the factorial of a non-negative integer."""
    n_int = int(float(n))
    if n_int < 0:
        raise ValueError("Factorial is only defined for non-negative integers")
    return math.factorial(n_int)

@mcp.tool()
def summation(start: Any, end: Any, expression: str = "n") -> Union[int, float]:
    """Calculate the sum of a series.
    
    Default sums the numbers from start to end.
    For custom expressions, use 'n' as the variable.
    """
    import re
    
    start_int = int(float(start))
    end_int = int(float(end))
    
    # Validate expression - check if it only contains safe characters
    if not re.match(r'^[0-9n\s\+\-\*\/\(\)\.\^]+$', expression):
        raise ValueError("Invalid expression: only basic math operations allowed")
    
    # Replace ^ with ** for Python's power operator
    expression = expression.replace("^", "**")
    
    result = 0
    for n in range(start_int, end_int + 1):
        # Evaluate the expression for each n
        term = eval(expression)
        result += term
    
    # Return int if result is a whole number, otherwise float
    return int(result) if result == int(result) else result

@mcp.tool()
def abs_value(n: Any) -> Union[int, float]:
    """Calculate the absolute value of a number."""
    n_float = float(n)
    result = abs(n_float)
    # Return int if result is a whole number, otherwise float
    return int(result) if result == int(result) else result

@mcp.tool()
def max_value(numbers: List[Any]) -> Union[int, float]:
    """Find the maximum value in a list of numbers."""
    if not numbers:
        raise ValueError("Empty list")
    # Convert all elements to float
    numbers_float = [float(n) for n in numbers]
    result = max(numbers_float)
    # Return int if result is a whole number, otherwise float
    return int(result) if result == int(result) else result

@mcp.tool()
def min_value(numbers: List[Any]) -> Union[int, float]:
    """Find the minimum value in a list of numbers."""
    if not numbers:
        raise ValueError("Empty list")
    # Convert all elements to float
    numbers_float = [float(n) for n in numbers]
    result = min(numbers_float)
    # Return int if result is a whole number, otherwise float
    return int(result) if result == int(result) else result

@mcp.tool()
def average(numbers: List[Any]) -> float:
    """Calculate the average (mean) of a list of numbers."""
    if not numbers:
        raise ValueError("Empty list")
    # Convert all elements to float
    numbers_float = [float(n) for n in numbers]
    return sum(numbers_float) / len(numbers_float)

@mcp.tool()
def median(numbers: List[Any]) -> float:
    """Calculate the median of a list of numbers."""
    if not numbers:
        raise ValueError("Empty list")
    # Convert all elements to float
    numbers_float = [float(n) for n in numbers]
    return statistics.median(numbers_float)

@mcp.tool()
def mode(numbers: List[Any]) -> Union[float, List[float]]:
    """Calculate the mode of a list of numbers."""
    if not numbers:
        raise ValueError("Empty list")
    # Convert all elements to float
    numbers_float = [float(n) for n in numbers]
    
    try:
        return statistics.mode(numbers_float)
    except statistics.StatisticsError:
        # Find mode manually if multiple modes exist
        frequency = {}
        for num in numbers_float:
            frequency[num] = frequency.get(num, 0) + 1
        max_freq = max(frequency.values())
        modes = [k for k, v in frequency.items() if v == max_freq]
        return modes

@mcp.tool()
def volume(shape: str, **kwargs) -> float:
    """Calculate the volume of a 3D shape.
    
    Args:
        shape: The 3D shape ('cube', 'sphere', 'cylinder', etc.)
        **kwargs: Parameters specific to the shape
    """
    shape = shape.lower()
    
    # Convert all numeric kwargs to float
    for key, value in kwargs.items():
        if isinstance(value, (int, float, str)) and not isinstance(value, bool):
            try:
                kwargs[key] = float(value)
            except ValueError:
                pass
    
    if shape == "cube":
        if "side" in kwargs:
            return kwargs["side"] ** 3
        else:
            raise ValueError("Cube requires side length")
    elif shape == "sphere":
        if "radius" in kwargs:
            return (4/3) * math.pi * kwargs["radius"] ** 3
        else:
            raise ValueError("Sphere requires radius")
    elif shape == "cylinder":
        if "radius" in kwargs and "height" in kwargs:
            return math.pi * kwargs["radius"] ** 2 * kwargs["height"]
        else:
            raise ValueError("Cylinder requires radius and height")
    elif shape == "cone":
        if "radius" in kwargs and "height" in kwargs:
            return (1/3) * math.pi * kwargs["radius"] ** 2 * kwargs["height"]
        else:
            raise ValueError("Cone requires radius and height")
    elif shape == "rectangular_prism" or shape == "cuboid":
        if "length" in kwargs and "width" in kwargs and "height" in kwargs:
            return kwargs["length"] * kwargs["width"] * kwargs["height"]
        else:
            raise ValueError("Rectangular prism requires length, width, and height")
    else:
        raise ValueError(f"Unsupported shape: {shape}")

@mcp.tool()
def perimeter(shape: str, **kwargs) -> float:
    """Calculate the perimeter of a 2D shape.
    
    Args:
        shape: The 2D shape ('square', 'rectangle', 'circle', etc.)
        **kwargs: Parameters specific to the shape
    """
    shape = shape.lower()
    
    # Convert all numeric kwargs to float
    for key, value in kwargs.items():
        if isinstance(value, (int, float, str)) and not isinstance(value, bool):
            try:
                kwargs[key] = float(value)
            except ValueError:
                pass
        elif isinstance(value, list):
            try:
                kwargs[key] = [float(item) for item in value]
            except (ValueError, TypeError):
                pass
    
    if shape == "square":
        if "side" in kwargs:
            return 4 * kwargs["side"]
        else:
            raise ValueError("Square requires side length")
    elif shape == "rectangle":
        if "length" in kwargs and "width" in kwargs:
            return 2 * (kwargs["length"] + kwargs["width"])
        else:
            raise ValueError("Rectangle requires length and width")
    elif shape == "circle":
        if "radius" in kwargs:
            return 2 * math.pi * kwargs["radius"]
        elif "diameter" in kwargs:
            return math.pi * kwargs["diameter"]
        else:
            raise ValueError("Circle requires radius or diameter")
    elif shape == "triangle":
        if "sides" in kwargs and len(kwargs["sides"]) == 3:
            return sum(kwargs["sides"])
        else:
            raise ValueError("Triangle requires three sides")
    else:
        raise ValueError(f"Unsupported shape: {shape}")

@mcp.tool()
def equation_solving(equation: str, variable: str = "x") -> Union[int, float]:
    """Solve a simple linear equation for the specified variable.
    
    Equation should be in the form "expression = expression"
    """
    import re
    
    # Validate equation - check if it only contains safe characters
    if not re.match(r'^[0-9a-zA-Z\s\+\-\*\/\(\)\.\=]+$', equation):
        raise ValueError("Invalid equation: only basic math operations allowed")
    
    if "=" not in equation:
        raise ValueError("Equation must contain '='")
    
    # For simple equations of form ax + b = c, solve directly
    try:
        left, right = equation.split("=", 1)
        left = left.strip()
        right = right.strip()
        
        # Move all terms with variable to left, constants to right
        left_terms = []
        right_terms = []
        
        for term in left.replace("-", "+-").split("+"):
            term = term.strip()
            if not term:
                continue
            if variable in term:
                left_terms.append(term)
            else:
                if term.startswith("-"):
                    right_terms.append(term[1:])  # Remove the negative sign
                else:
                    right_terms.append("-" + term)
        
        for term in right.replace("-", "+-").split("+"):
            term = term.strip()
            if not term:
                continue
            if variable in term:
                if term.startswith("-"):
                    left_terms.append(term)
                else:
                    left_terms.append("-" + term)
            else:
                right_terms.append(term)
        
        # Calculate coefficient of variable
        coef = 0
        for term in left_terms:
            if term == variable:
                coef += 1
            elif term == "-" + variable:
                coef -= 1
            else:
                # Parse terms like "2x" or "-3x"
                c = term.replace(variable, "")
                if c == "-":
                    coef -= 1
                elif c == "":
                    coef += 1
                else:
                    coef += float(c)
        
        # Calculate constant
        constant = 0
        for term in right_terms:
            if term and term not in ["+", "-"]:
                constant += float(term)
        
        # Solve
        if coef == 0:
            raise ValueError("Equation has no solution for " + variable)
        
        result = constant / coef
        # Return int if result is a whole number, otherwise float
        return int(result) if result == int(result) else result
    except Exception as e:
        raise ValueError(f"Could not solve equation: {str(e)}")

@mcp.tool()
def slope(point1: List[Any], point2: List[Any]) -> Union[int, float]:
    """Calculate the slope of a line passing through two points."""
    if len(point1) != 2 or len(point2) != 2:
        raise ValueError("Points must be in the form [x, y]")
    
    # Convert to float
    x1, y1 = float(point1[0]), float(point1[1])
    x2, y2 = float(point2[0]), float(point2[1])
    
    if x1 == x2:
        raise ValueError("Slope is undefined (vertical line)")
        
    result = (y2 - y1) / (x2 - x1)
    # Return int if result is a whole number, otherwise float
    return int(result) if result == int(result) else result

@mcp.tool()
def area(shape: str, **kwargs) -> float:
    """Calculate the area of a 2D shape."""
    # This is essentially an alias for the geometry tool
    return geometry(shape, **kwargs)

@mcp.tool()
def surface_area(shape: str, **kwargs) -> float:
    """Calculate the surface area of a 3D shape.
    
    Args:
        shape: The 3D shape ('cube', 'sphere', 'cylinder', etc.)
        **kwargs: Parameters specific to the shape
    """
    shape = shape.lower()
    
    # Convert all numeric kwargs to float
    for key, value in kwargs.items():
        if isinstance(value, (int, float, str)) and not isinstance(value, bool):
            try:
                kwargs[key] = float(value)
            except ValueError:
                pass
    
    if shape == "cube":
        if "side" in kwargs:
            side = kwargs["side"]
            return 6 * side ** 2
        else:
            raise ValueError("Cube requires side length")
    elif shape == "sphere":
        if "radius" in kwargs:
            radius = kwargs["radius"]
            return 4 * math.pi * radius ** 2
        else:
            raise ValueError("Sphere requires radius")
    elif shape == "cylinder":
        if "radius" in kwargs and "height" in kwargs:
            radius = kwargs["radius"]
            height = kwargs["height"]
            return 2 * math.pi * radius * (radius + height)
        else:
            raise ValueError("Cylinder requires radius and height")
    elif shape == "cone":
        if "radius" in kwargs and "height" in kwargs:
            radius = kwargs["radius"]
            height = kwargs["height"]
            slant_height = math.sqrt(radius**2 + height**2)
            return math.pi * radius * (radius + slant_height)
        else:
            raise ValueError("Cone requires radius and height")
    elif shape == "rectangular_prism" or shape == "cuboid":
        if "length" in kwargs and "width" in kwargs and "height" in kwargs:
            length = kwargs["length"]
            width = kwargs["width"]
            height = kwargs["height"]
            return 2 * (length * width + length * height + width * height)
        else:
            raise ValueError("Rectangular prism requires length, width, and height")
    else:
        raise ValueError(f"Unsupported shape: {shape}")

@mcp.tool()
def distance(point1: List[Any], point2: List[Any]) -> float:
    """Calculate the distance between two points in 2D or 3D space."""
    if len(point1) != len(point2):
        raise ValueError("Points must have the same dimensions")
    
    # Convert to float
    point1_float = [float(coord) for coord in point1]
    point2_float = [float(coord) for coord in point2]
    
    # Calculate sum of squared differences
    sum_sq = sum((x - y) ** 2 for x, y in zip(point1_float, point2_float))
    
    return math.sqrt(sum_sq)

@mcp.tool()
def statistics_tool(operation: str, data: List[Any]) -> Union[float, List[float]]:
    """Perform statistical operations on a dataset.
    
    Supported operations:
    - mean: Calculate the mean (average)
    - median: Calculate the median
    - mode: Calculate the mode
    - variance: Calculate the variance
    - stdev: Calculate the standard deviation
    - range: Calculate the range (max - min)
    """
    # Convert all elements to float
    data_float = [float(n) for n in data]
    
    operation = operation.lower()
    
    if operation == "mean":
        return sum(data_float) / len(data_float)
    elif operation == "median":
        return statistics.median(data_float)
    elif operation == "mode":
        try:
            return statistics.mode(data_float)
        except statistics.StatisticsError:
            # Find mode manually if multiple modes exist
            frequency = {}
            for num in data_float:
                frequency[num] = frequency.get(num, 0) + 1
            max_freq = max(frequency.values())
            modes = [k for k, v in frequency.items() if v == max_freq]
            return modes
    elif operation == "variance":
        return statistics.variance(data_float)
    elif operation == "stdev":
        return statistics.stdev(data_float)
    elif operation == "range":
        return max(data_float) - min(data_float)
    else:
        raise ValueError(f"Unsupported operation: {operation}")

@mcp.tool()
def pythagorean(a: Any, b: Any) -> float:
    """Calculate the length of the hypotenuse using the Pythagorean theorem."""
    a_float = float(a)
    b_float = float(b)
    
    if a_float <= 0 or b_float <= 0:
        raise ValueError("Side lengths must be positive")
    
    return math.sqrt(a_float**2 + b_float**2)

if __name__ == "__main__":
    mcp.run(transport="stdio")