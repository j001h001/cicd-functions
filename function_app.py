import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route="http_trigger", auth_level=func.AuthLevel.ANONYMOUS)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    number = req.params.get('number')
    if not number:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            number = req_body.get('number')

    if number:
        try:
            # Convert number to integer
            num = int(number)
            response = analyze_number(num)
            return func.HttpResponse(json.dumps(response), mimetype="application/json")
        except ValueError:
            return func.HttpResponse(
                json.dumps({"error": "please enter a valid number"}), 
                status_code=400,
                mimetype="application/json"
            )
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a number in the query string or in the request body.",
             status_code=200
        )


def analyze_number(num):
    # TODO 1: Code Logic to handle number validation
    if num <= 0:
        # FIXED: Changed from a Set {"string"} to a Dict {"key": "value"}
        return {"error": "please enter a number greater than 0"}

    # TODO 2: Code Logic to find the sum of numbers
    # FIXED: Changed 'digits' to 'digit'
    sum_of_digits = sum(int(digit) for digit in str(num))

    # TODO 3: Code Logic to check whether number is prime
    is_prime = True
    if num <= 1:
        is_prime = False
    else:
        for i in range(2, int(num ** 0.5) + 1):
            # FIXED: Changed % 1 to % i
            if num % i == 0:
                is_prime = False
                break

    # TODO 4: Code Logic to check whether number is odd
    is_odd = (num % 2 != 0)

    # TODO 5: Code Logic to check whether number is perfect
    is_perfect = False
    if num > 1:
        sum_divisors = 0
        for i in range(1, (num // 2) + 1):
            if num % i == 0:
                # FIXED: Changed += 1 to += i (sum the actual divisor, not the count)
                sum_divisors += i

        if sum_divisors == num:
            # FIXED: Removed space in variable name
            is_perfect = True
            
    # TODO 6: Replace default values
    response = {
        "sum_of_digits": sum_of_digits,
        "is_prime": is_prime,
        "is_odd": is_odd,
        "is_perfect": is_perfect
    }

    return response