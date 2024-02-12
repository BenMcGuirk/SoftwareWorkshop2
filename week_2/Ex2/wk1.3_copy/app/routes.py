from flask import Flask, render_template
from flask import Blueprint
import math

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def main():
    return 'Enter a number after /prime/ in bar to get its prime divisors.'

def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def get_prime_divisors(n):
    """Get the prime divisors of a number."""
    divisors = [i for i in range(1, n + 1) if n % i == 0 and is_prime(i)]
    return divisors

@main_bp.route('/prime/<int:number>')
def prime_divisors_page(number):
    prime_divisors = get_prime_divisors(number)
    return render_template('prime_divisors.html', number=number, prime_divisors=prime_divisors)