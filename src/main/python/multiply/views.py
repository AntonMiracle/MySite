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
    input_number_error = False
    input_times_error = False
    input_result_error = False
    if request.POST:
        input_number = int(request.POST.get('input_number'))
        input_times = int(request.POST.get('input_times'))
        input_result = int(request.POST.get('input_result'))
        if input_number != multiply.number:
            input_number_error = True
        if input_times != multiply.times:
            input_times_error = True
        if input_result != multiply.result:
            input_result_error = True
        if not input_number_error and not input_times_error and not input_result_error:
            multiply.generate()

    times_sum = [multiply.number for i in range(multiply.times)]
    times_sum_len = len(times_sum)
    ctx = {
        'number': multiply.number,
        'times': multiply.times,
        'result': multiply.result,
        'times_sum': times_sum,
        'times_sum_len': times_sum_len,
        'input_number_error': input_number_error,
        'input_times_error': input_times_error,
        'input_result_error': input_result_error,
    }

    return render(request, 'multiply/learn.html', ctx)


@login_required()
def main(request):
    return render(request, 'multiply/main.html')
