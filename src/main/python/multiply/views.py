from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from random import randint


class Multiply:
    level = 1
    number = 0
    times = 0
    result = 0

    def generate(self, level=1):
        self.level = level
        self.number = randint(1, 9 + self.level)
        self.times = randint(1, 10 + self.level)
        self.result = self.number * self.times


multiply = Multiply()
multiply.generate()


@login_required()
def learn(request):
    print(multiply.number)
    print(multiply.times)
    print(multiply.result)
    inputNumberError = False
    inputTimesError = False
    inputResultError = False
    if request.POST:
        print("********** POST")
        inputNumber = int(request.POST.get('inputNumber'))
        inputTimes = int(request.POST.get('inputTimes'))
        inputResult = int(request.POST.get('inputResult'))
        print(inputNumber)
        print(inputTimes)
        print(inputResult)
        if inputNumber != multiply.number:
            inputNumberError = True
        if inputTimes != multiply.times:
            inputTimesError = True
        if inputResult != multiply.result:
            inputResultError = True
        print(inputNumberError)
        print(inputTimesError)
        print(inputResultError)
        if not inputNumberError and not inputTimesError and not inputResultError:
            multiply.generate()

    times_sum = [multiply.number for i in range(multiply.times)]
    times_sum_len = len(times_sum)
    ctx = {
        'number': multiply.number,
        'times': multiply.times,
        'result': multiply.result,
        'times_sum': times_sum,
        'times_sum_len': times_sum_len,
        'inputNumberError': inputNumberError,
        'inputTimesError': inputTimesError,
        'inputResultError': inputResultError,
    }

    return render(request, 'multiply/learn.html', ctx)


@login_required()
def main(request):
    return render(request, 'multiply/main.html')
