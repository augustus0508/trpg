import random

def generate_random_integers(count, upper_limit):
  return [random.randint(1, upper_limit) for _ in range(count)]
