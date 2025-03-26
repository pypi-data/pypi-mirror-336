# Rules for finding Prime Numbers
# Aside from 2, no even number is Prime
# If the sum of the digits is divisible by 3, then the number will be divisble by 3
# If the number end with 0 or 5, then it will be divisible by 5
# Double the last digit and subtract it from the rest of the number... If the answer is divisible by 7, the original number will be divisible by 7... For instance, if the number is 161, take the last digit (1), double it, then subtract it from the rest of the number (16)... If the answer is divisible by 7, then so is the original number... In this case the answer is 14, 14 is divisible by 7, so 161 is also
# Add alternate digits and subtract it from the difference of the next sum of alternate digits... For instance, if the number is 574652, add 5+4+5=14 and 7+6+2=15... If the difference i.e. 1 is divisible by 11, then the number will be divisible by 11... In this case, clearly the number is not divisible by 11
# Semiprimes are not true Primes and need to be ruled out by checking a number against the square of each Prime that was already added to the prime list... For example, 169 is the product of 13*13, so it's not Prime, it's Semiprime
# Squarefree Primes are an extension of Semiprimes where the number is the product of two unique Primes from the Prime list... For example, 221 is the product of 13*17, so it's not Prime, it's a Squarefree Prime

from .prime_file_handler import PrimeFileHandler


class PrimeChecker:
    def __init__(self, prime_list):
        self.starting_prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        self.prime_list = prime_list
        self.end_digit_fail_list = [0, 2, 4, 5, 6, 8]
        self.is_semiprime = False
        self.is_squarefree_prime = False

    # * Function to determine the sum of the digits of the number
    def digit_sum(self, number):
        digit_sum = 0
        digits = str(number)

        for digit in digits:
            digit_sum += int(digit)
        return digit_sum

    # * Function to check last digit of the number
    def last_digit(self, number):
        return int(str(number)[-1:])

    # * Function to check for the divisible by 7 condition
    def seven_check(self, number):
        last_digit = int(str(number)[-1:])
        new_number_1 = int(str(number)[:-1])
        new_number_2 = new_number_1 - (2 * last_digit)
        return new_number_2

    # * Function to check for the divisible by 11 condition
    def eleven_check(self, number):
        new_number_1 = int(str(number)[0::2])
        new_number_1 = self.digit_sum(new_number_1)
        new_number_2 = int(str(number)[1::2])
        new_number_2 = self.digit_sum(new_number_2)
        new_number_3 = abs(new_number_1 - new_number_2)
        return new_number_3

    # * Function to check for Semiprimes
    def semiprime_check(self, number):
        for prime in self.prime_list:
            if number == prime * prime:
                return True
        return False

    # * Function to check for Squarefree Primes
    def squarefree_prime_check(self, number):
        for prime in self.prime_list:
            if number % prime == 0:
                return True
        return False

    # * Function to determine if a number is Prime or not
    def prime_check(self, number):
        if number in self.starting_prime_list:
            self.prime_list.append(number)
            return True

        if self.last_digit(number) in self.end_digit_fail_list:
            return False

        if self.digit_sum(number) % 3 == 0:
            return False

        if self.seven_check(number) % 7 == 0:
            return False

        if self.eleven_check(number) % 11 == 0:
            return False

        if self.semiprime_check(number) is True:
            return False

        if self.squarefree_prime_check(number) is True:
            return False

        self.prime_list.append(number)

        return True

    def number_check(self, number):
        if number in self.prime_list:
            print(f"{number} is prime!")
        else:
            print(f"{number} is not prime!")


def main():
    prime_file_handler = PrimeFileHandler()
    current_number = prime_file_handler.load_current_number()
    prime_list = prime_file_handler.load_prime_numbers()
    prime_checker = PrimeChecker(prime_list)
    is_prime = False
    keep_iterating = True
    check_to_number = int()
    check_or_iterate = str(
        input(
            "Would you like to (iterate) to find new primes for your prime library or (check) to see if a specific number is prime?: "
        )
    )

    if check_or_iterate.lower() == "iterate":
        while keep_iterating:
            is_prime = prime_checker.prime_check(current_number)

            if is_prime is True:
                prime_file_handler.save_found_prime(current_number)

            current_number += 1
            prime_file_handler.save_current_number(current_number)

    elif check_or_iterate.lower() == "check":
        check_to_number = int(
            input("Enter the number you'd like to check the primality of: ")
        )

        while check_to_number > current_number:
            is_prime = prime_checker.prime_check(current_number)

            if is_prime is True:
                prime_file_handler.save_found_prime(current_number)

            current_number += 1
            prime_file_handler.save_current_number(current_number)

        prime_checker.number_check(check_to_number)


if __name__ == "__main__":
    main()
