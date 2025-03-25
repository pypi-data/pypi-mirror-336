#Rathureqpy - A Python Utility Library

Rathureqpy is a Python library that provides a set of useful functions for a variety of tasks including list manipulation, mathematical operations, logical operations, statistical measures, and more.

##Installation

You can install Rathureqpy by running:

``bash
pip install rathureqpy
``

##Features

###List Operations

- **zero(number)**: Returns a list of zeros with the specified length.

- **prod(L, a)**: Returns a new list with each element of `L` multiplied by `a`.

- **addl(*args)**: Adds corresponding elements from multiple lists of equal length.

- **linespace(start, end, step)**: Generates a list of evenly spaced values between `start` and `end` with a given `step`.

- **array(start, end, n)**: Generates an array of `n` evenly spaced values between `start` and `end`.

- **uni(*lists)**: Flattens multiple lists into a single list.

- **uniwd(*lists)**: Flattens multiple lists into a single list and removes duplicates.

- **inter(*lists)**: Returns the intersection of multiple lists.

- **uniq(L)**: Returns a list with unique elements from `L`.

- **moy(L)**: Returns the mean of a list `L`.

- **sum_int(start, end)**: Returns the sum of integers between `start` and `end`.

- **randl(min, max, n)**: Generates a list of `n` random integers between `min` and `max`.

- **shuffle_list(L)**: Returns a shuffled version of `L`.

- **filtrer(L, condition)**: Filters `L` based on a condition.

- **apply(L, function)**: Applies a function to each element in the list `L`.

- **chunk(L, n)**: Splits `L` into chunks of size `n`.

- **partition(L, condition)**: Partitions `L` into two lists based on a condition.


###Logical Operations

- **binr(n)**: Converts an integer `n` to its binary representation as a string.

- **change_base(value, inp_base, out_base)**: Converts `value` from `inp_base` to `out_base`.

- **divisor_list(n)**: Returns a list of divisors of `n`.

- **dicho(start, end, f, eps)**: Performs binary search to find the root of the function `f` in the interval `[start, end]` with an error tolerance `eps`.

- **size(point_A, point_B)**: Calculates the distance between two points `A` and `B` in a 2D space.

###Constants

- **pi()**: Returns the constant `π`.

- **e()**: Returns the constant `e`.

- **tau()**: Returns the constant `τ` (2π).

###Mathematical Operations

- **abs(x)**: Returns the absolute value of `x`.

- **cos(x)**: Returns the cosine of `x`.

- **sin(x)**: Returns the sine of `x`.

- **log(x, base=e())**: Returns the logarithm of `x` to the specified `base`.

- **exp(x)**: Returns the exponential of `x`.

- **sqrt(x)**: Returns the square root of `x`.

- **facto(n)**: Returns the factorial of `n`.

- **floor(x)**: Returns the largest integer less than or equal to `x`.

- **ceil(x)**: Returns the smallest integer greater than or equal to `x`.

- **rint(x)**: Returns the integer closest to `x` (rounding halfway cases away from zero).

- **gcd(a, b)**: Returns the greatest common divisor of `a` and `b`.

- **lcm(a, b)**: Returns the least common multiple of `a` and `b`.

- **is_prime(n)**: Checks if `n` is a prime number.

###Statistical Measures

- **variance(L)**: Returns the variance of the list `L`.

- **ecart_type(L)**: Returns the standard deviation of the list `L`.

- **mediane(L)**: Returns the median of the list `L`.

- **decomp(n)**: Returns the prime factorization of `n` as a list of tuples.

- **list_prime(n)**: Returns a list of all prime numbers up to `n`.

- **pascal_row(n)**: Returns the `n`-th row of Pascal's Triangle.

##Contribute and Bugs

If you encounter any bugs or would like to contribute to the project, feel free to open an issue or submit a pull request. Contributions are always welcome!

Made by Arthur Quersin
