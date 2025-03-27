from .prime_file_handler import PrimeFileHandler


class PrimeChecker:
    def __init__(self, prime_list):
        self.starting_prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        self.prime_list = prime_list
        self.end_digit_fail_list = [0, 2, 4, 5, 6, 8]
        self.is_semiprime = False
        self.is_squarefree_prime = False

    def digit_sum(self, number):
        """
        Function to determine the sum of the digits of the number. If the sum of the digits are divisible by 3, then the number will be divisible by 3.
        """

        digit_sum = 0
        digits = str(number)

        for digit in digits:
            digit_sum += int(digit)
        return digit_sum

    def last_digit(self, number):
        """
        Function to check last digit of the number. If the last digit of a number is in [0,2,4,5,6,8], then it can't be prime because it's either even, or is divisible by 5. The only exception to this is 2, which while even, is prime since it's only factors are 1 and 2.
        """

        return int(str(number)[-1:])

    def seven_check(self, number):
        """
        Function to check for the divisible by 7 condition. In this case, it's easier to give an example. Take 161. If we take it's last digit (1), double it (1*2=2), then subtract that from the number not including the last digit (161 becomes 16), which gives us 16-2=14, then take that result (14) and we can divide it evenly by 7 (in this case, 14/7=2), then the original number (161) is also evenly divisible by 7. This is always the case.
        """

        last_digit = int(str(number)[-1:])
        new_number_1 = int(str(number)[:-1])
        new_number_2 = new_number_1 - (2 * last_digit)
        return new_number_2

    def eleven_check(self, number):
        """
        Function to check for the divisible by 11 condition. This condition is best explained with an example. Take the number 574652. If we take the sums of alternating digits (5+4+5=14 and 7+6+2=15), then we take the absolute value of their difference (|14-15|=1), and that value is divisble by 11, then the original number is divisble by 11. In this case, 1 is not divisble by 11, so 574652 passes this check.
        """

        new_number_1 = int(str(number)[0::2])
        new_number_1 = self.digit_sum(new_number_1)
        new_number_2 = int(str(number)[1::2])
        new_number_2 = self.digit_sum(new_number_2)
        new_number_3 = abs(new_number_1 - new_number_2)
        return new_number_3

    def semiprime_and_squarefree_prime_check(self, number):
        """
        Function to check for Semiprimes and Squarefree Primes. Semiprimes are numbers that are squares of other primes. For example, 169 is the square of 13. Squarefree primes are numbers that are the product of other primes. For example, 221 is the product of 13 and 17. We can check for both these conditions in the same manner. If the number we're checking, mod a known prime (161 % 13), equals 0, then the number is either a semiprime or squarefree prime. We also only need to check up to known primes of less than or equal to the square root of the number we're checking since in either case, a factor of a semiprime or a squarefree prime will always be equal to or less than the square root of the number.
        """

        square_root = number**0.5
        for prime in self.prime_list:
            if square_root < prime:
                break
            if number % prime == 0:
                return True
        return False

    def prime_check(self, number):
        """
        Function to determine if a number is Prime or not. It runs through all the checks and then returns if the number is prime or not.
        """

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

        if self.semiprime_and_squarefree_prime_check(number) is True:
            return False

        self.prime_list.append(number)

        return True

    def number_check(self, number):
        """
        This function checks a number to see if it's in the prime list, and if it is therefore, prime.
        """

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
