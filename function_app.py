import azure.functions as func
import json
import logging
import math

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
             "This HTTP triggered function executed successfully. Pass a number in the query string.",
             status_code=200
        )

def analyze_number(num):
    if num <= 0:
        return {"error": "please enter a number greater than 0"}

    sum_of_digits = sum(int(digit) for digit in str(num))

    is_prime = True
    if num <= 1:
        is_prime = False
    else:
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break

    is_odd = (num % 2 != 0)

    is_perfect = False
    if num > 1:
        sum_divisors = sum(i for i in range(1, (num // 2) + 1) if num % i == 0)
        if sum_divisors == num:
            is_perfect = True

    # TRIANGULAR LOGIC
    is_triangular = False
    if num > 0:
        # A number x is triangular if 8x + 1 is a perfect square
        check_val = (8 * num) + 1
        root = int(math.isqrt(check_val))
        if root * root == check_val:
            is_triangular = True

    response = {
        "sum_of_digits": sum_of_digits,
        "is_prime": is_prime,
        "is_odd": is_odd,
        "is_perfect": is_perfect,
        "is_triangular": is_triangular
    }

    return response