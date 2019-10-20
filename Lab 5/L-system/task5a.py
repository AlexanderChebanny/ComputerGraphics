"""
Лысенко Никита 4.8

Лабораторная работа №5. L-системы. Diamond-square. Cплайны
1. L-системы
Реализовать программу для построения фрактальных узоров посредством L-систем.

Описание L-систем задается в текстовом файле вида:

<атомарный символ> <угол поворота> <начальное направление>
<правило №1>
<правило №2>
...
Реализовать возможность разветвления в системе (скобки).
Предусмотреть масштабирование получаемого набора точек (должен помещаться в окне).
В качестве тестов использовать фракталы из лекций.
"""

import turtle
import os


def derivation(axiom, steps, rules):
    derived = [axiom]  # seed
    for _ in range(steps):
        next_seq = derived[-1]
        next_axiom = [get_rule(char, rules) for char in next_seq]
        derived.append(''.join(next_axiom))
    return derived


def get_rule(sequence, rules):
    if sequence in rules:
        return rules[sequence]
    return sequence


def set_turtle(angle_zero):
    r_turtle = turtle.Turtle()  # recursive turtle
    r_turtle.speed(0)  # adjust as needed (0 = fastest)
    r_turtle.setheading(angle_zero)  # initial heading
    return r_turtle


def start_l_system(turtle, commands, step_length, angle):
    stack = []
    for command in commands:
        turtle.pd()
        if command == 'F':
            turtle.forward(step_length)
        elif command == "f":
            turtle.pu()  # pen up - not drawing
            turtle.forward(step_length)
        elif command == "+":
            turtle.right(angle)
        elif command == "-":
            turtle.left(angle)
        elif command == "[":
            stack.append((turtle.position(), turtle.heading()))
        elif command == "]":
            turtle.pu()  # pen up - not drawing
            position, heading = stack.pop()
            turtle.goto(position)
            turtle.setheading(heading)


def l_system(iterations, file_name, step_length):
    input_file = open(file_name, 'r')
    # getting all information from input file
    config = input_file.readline().split(' ')
    axiom = config[0]
    angle = float(config[1])
    angle_zero = float(config[2])  # initial direction in degrees (0 - right, 90 - up, 180 - left, 270 - down
    rules = dict()
    for rule_line in input_file:
        key, value = rule_line.split('=>')
        rules[key.strip()] = value
    print(axiom, angle, angle_zero)
    print(rules)

    commands = derivation(axiom=axiom, steps=iterations, rules=rules)  # axiom (initial string), nth iterations

    # iterations_list = [0, 1, 2, 3, 4, 5]
    # steps = [405, 135, 45, 15, 5, 1]
    # index_of_step_length = iterations_list.index(iterations)
    # step_length = steps[index_of_step_length] # 0-405  1-135  2-45 3-15 4-5 5-1

    # Set turtle parameters and draw L-System
    r_turtle = set_turtle(angle_zero)  # create turtle object
    turtle_screen = turtle.Screen()  # create graphics window
    turtle_screen.screensize(1500, 1500)
    start_l_system(turtle=r_turtle, commands=commands[-1], step_length=step_length, angle=angle)  # draw model
    turtle_screen.exitonclick()


def test_files(path):
    files = os.listdir(path)
    res = list()
    i = 1
    while i < len(files) + 1:
        for file in files:
            if '.txt' in file:
                if str(i) in file[:2]:
                    res.append(file[:-4])
                    break
        i += 1
    return res


if __name__ == '__main__':
    path = './tests/'
    print('Выберите тестовый пример: ')
    files = test_files(path)
    for file in files:
        print(file)

    number = int(input('Введите номер файла: '))
    # number = 1
    file_name = path + files[number - 1] + '.txt'

    iterations = int(input('\nВведите количество итераций: '))
    # iterations = 10

    step_length = 10
    l_system(iterations=iterations, file_name=file_name, step_length=step_length)

