# Software Development Hub test

Реализовать решение с использованием Django.

Django приложение, реализующие регистрацию с подтверждением через email и реферальную систему пользователей.

Описание задания:

Сайт должен поддерживать регистрацию пользователей с возможностью ввести код-приглашение. После подтверждения email пользователь попадает на свою личную страницу. На этой странице он видит тех, кто привлек его и список привлеченных им людей.
Пользователь может сгенерировать свой код-приглашение.
У каждого пользователя есть его текущие очки.
Схема начисления очков такова:
Призовой фонд за успешное использование кода-приглашения составляет N баллов, где N - это текущие количество зарегистрировавшихся пользователей владельца кода + 1. 
Призовой фонд распределяется по схеме: владельцу кода 1 балл, тому кто привлек владельца 1 балл и так далее, пока будет достигнуто одно из условий: a) N == 0 b) достигнута вершина дерева
В случае b и если N > 0 - пользователю на вершине начисляются все значение N

Первые 5 пользователей могут зарегистрироваться в системе без кода-приглашения, далее только с кодом. 

Должна быть реализована страница рейтинга пользователей по очкам “Топ-10”

