def fizzbuzz(n: int) -> str:
    output = ""
    if n % 3 == 0:
        output += "fizz"
    if n % 5 == 0:
        output += "buzz"
    return output or str(n)

if __name__ == "__main__":
    assert fizzbuzz(15) == "fizzbuzz"
