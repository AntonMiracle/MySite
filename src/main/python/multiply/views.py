from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from random import randint
from .models import MultiplyUserRank
from django.db import transaction


class MultiplyContext:
    def __init__(self, request):
        self.ctx = {}
        user = request.user
        if not MultiplyUserRank.objects.filter(user=user).count():
            create_user_rank = MultiplyUserRank(user=user, level=1, experience=0, next_level=100)
            create_user_rank.save()

        rank = MultiplyUserRank.objects.get(user=user)
        self.ctx.update({
            'username': user.username,
            'level': rank.level,
            'experience': rank.experience,
            'next_level': rank.next_level,
        })


class Multiply:
    level = 1
    number = 0
    times = 0
    result = 0

    def generate(self, level=1):
        self.level = level
        self.number = randint(2, 4 + self.level)
        self.times = randint(2, 10)
        self.result = self.number * self.times


class Task:
    def __init__(self, level):
        self.timer_amount = randint(23, 43) + (level / 10)
        self.rank = randint(1, 3)
        self.multiply = Multiply()
        self.multiply.generate(level)
        self.exp_coefficient = 1
        self.exp = 4 + level

        if self.rank == 1:
            self.exp_coefficient *= 1.5
        elif self.rank == 2:
            self.exp_coefficient *= 1.6
        elif self.rank == 3:
            my_max = max(self.multiply.number, self.multiply.times)
            self.exp_coefficient *= 2 - abs(self.multiply.number - self.multiply.times) / my_max
            self.exp_coefficient *= 1.4
        self.exp *= self.exp_coefficient


multiply = Multiply()
multiply.generate()


@login_required()
def learn(request):
    ctx = MultiplyContext(request).ctx
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
            multiply.generate(ctx['level'])

    times_sum = [multiply.number for i in range(multiply.times)]
    times_sum_len = len(times_sum)
    ctx.update({
        'number': multiply.number,
        'times': multiply.times,
        'result': multiply.result,
        'times_sum': times_sum,
        'times_sum_len': times_sum_len,
        'input_number_error': input_number_error,
        'input_times_error': input_times_error,
        'input_result_error': input_result_error,
    })
    return render(request, 'multiply/learn.html', ctx)


@login_required()
def tasks(request):
    task_complete = False
    if request.POST:
        task_rank = int(request.POST.get('task_rank'))
        task_exp = int(request.POST.get('task_exp'))
        task_number = int(request.POST.get('task_number'))
        task_result = int(request.POST.get('task_result'))
        try:
            if task_rank == 1:
                input_number = int(request.POST.get('input_number'))
                task_complete = task_number == input_number
            elif task_rank == 2:
                input_result = int(request.POST.get('input_result'))
                task_complete = task_result == input_result
            elif task_rank == 3:
                input_number = int(request.POST.get('input_number'))
                input_times = int(request.POST.get('input_times'))
                input_result = input_number * input_times
                task_complete = task_result == input_result
        except ValueError:
            pass
        if task_complete:
            amount = add_experience(request, task_exp)
        else:
            amount = remove_experience(request, task_exp)

        return complete(request, task_complete, amount)

    ctx = MultiplyContext(request).ctx
    exp = Task(ctx['level'])
    ctx['task'] = exp
    return render(request, 'multiply/tasks.html', ctx)


@login_required()
def complete(request, task_complete, amount):
    ctx = MultiplyContext(request).ctx
    ctx['complete'] = task_complete
    ctx['success_num'] = randint(1, 8)
    ctx['success_amount'] = amount
    ctx['loose_num'] = randint(1, 5)
    ctx['loose_amount'] = amount
    return render(request, 'multiply/complete.html', ctx)


@login_required()
def main(request):
    return render(request, 'multiply/main.html', MultiplyContext(request).ctx)


@transaction.atomic
@login_required()
def add_experience(request, amount):
    user = request.user
    rank = MultiplyUserRank.objects.get(user=user)
    new_experience = rank.experience + amount

    if new_experience >= rank.next_level:
        rank.level += 1
        rank.experience_for_next_level *= 1.5
        rank.next_level += rank.experience_for_next_level

    rank.experience = new_experience
    rank.save()
    return amount


@transaction.atomic
@login_required()
def remove_experience(request, amount):
    user = request.user
    rank = MultiplyUserRank.objects.get(user=user)
    amount = amount * 0.9
    if rank.experience > amount:
        new_experience = rank.experience - amount
        rank.experience = new_experience
        rank.save()
    return amount
