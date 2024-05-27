# Asm. Транслятор и модель

- Филатов Фёдор Романович
- `asm | cisc -> risc | neum | hw | instr | struct | stream | port | cstr | prob1 | cache`
- Без усложнения.


## Язык программирования

``` ebnf
program ::= { line }

line ::= label [ comment ] "\n"
       | instr [ comment ] "\n"
       | [ comment ] "\n"

label ::= label_name ":"

instr ::= op0
        | op1 positive_integer
        | op2 positive_integer, type
        | op3 address 

op0 ::= "inc"
      | "dec"
      | "halt"

op1 ::= "mov"
      | "add"
      | "sub"
      | "mul"
      | "div"
      | "rmd"
      | "cmp"
      | "in"

op2 ::= "out"

op3 ::= "jmp"
      | "jz"
      | "je"
      | "jb"
      | "jl"

address ::= lable_name
          | positive_integer

positive_integer ::= [0-9]+

type ::= "str"
      | "numb"

label_name ::= <any of "a-z A-Z _">

comment ::= ";" <any symbols except "\n">
```
Поддерживаются однострочные комментарии, начинающиеся с ;.
Код выполняется последовательно, одна инструкция за другой.

Список доступных инструкций см. [система команд](#система-команд)

## Организация памяти

Модель памяти процессора:

+ Фон-Неймановская архитектура – общая память для инструкций и данных
+ Размер машинного слова не определен (данные в памяти представляют собой структуры данных)
+ В случае переполнения регистров доступной памяти в начале выполнения будет выброшено исключение

Память адресуется двумя регистрами:
+ `AR` – регистр адреса для обращения к памяти из DataPath
+ `AP` – регистр адреса для обращения к памяти из ControlUnit

### Организация памяти при выполнении
```text
           Registers
+------------------------------+
| acc                          |
+------------------------------+

  Instruction and data memory
+------------------------------+
| 00   : program start         |
|     ...                      |
| n    : hlt                   |
| n+1  : value                 |
| n+2  : value                 |
|     ...                      |
+------------------------------+
```
В языке отсутствуют константы и литералы. Можно создавать переменные в части кода, которая идет после `.data:`.
Численные переменные занимаю одну ячейку памяти, строковые переменные хранятся последовательно в памяти и оканчиваются
специальным символом `\0`.

В коде программы к переменным можно обращаться по имени, которое задается в `.data:`. В процессе трансляции все имена 
переменных заменяются на адреса этих переменных в памяти.


## Система команд

Особенности процессора:

- Машинное слово -- не определено (CISC архитектура).
- Доступ к памяти данных осуществляется по адресу, хранящемуся в специальном регистре `data_address`. 
- Доступ к текущей инструкции осуществляется по адресу, хранящемуся в специальном регистре `program_address`.
- Напрямую установка адреса недоступна, осуществляется неявно внутри команд операторов, команд переходов и внутри команд загрузки, выгрузки памяти.
- Обработка данных происходит при помощи операторов `inc`, `dec`, `add`, `sub`, `mul`, `div`, `rmd`
- Поток управления:
    - инкремент `pc` после каждой инструкции;
    - условный (`jz`, `je`, `jb`, `jl`) и безусловный (`jmp`, `mov`) переходы
    - `counter` для выполнения команд требующих больше одного такта  
- Устройства ввода вывода используется при помощи портов
    - Для доступа к устройству вывода используется команда `out { port, type }`
    - Для доступа к устройству ввода используется команда `in { port }`, `in { port, address }`

Набор инструкций:

- `mov { address }` -- безусловный переход по заданному адресу (используется для DataPath)
- `mov { el1_addr, el2_addr, address }` -- поменять местами два элемента, используя промежуточный адрес
- `inc` -- увеличить значение в текущей ячейке на 1
- `dec` -- уменьшить значение в текущей ячейке на 1
- `add { el1_addr, el2_addr, address }` -- сложить произвольное количество элементов из памяти и положить в ячейку по указанному адресу (элементы берутся слева направо)
- `sub { el1_addr, el2_addr, address }` -- вычесть произвольное количество элементов из памяти и положить в ячейку по указанному адресу (элементы берутся слева направо)
- `mul { el1_addr, el2_addr, address }` -- перемножить произвольное количество элементов из памяти и положить в ячейку по указанному адресу (элементы берутся слева направо)
- `div { el1_addr, el2_addr, address }` -- поделить произвольное количество элементов из памяти и положить в ячейку по указанному адресу (элементы берутся слева направо)
- `rmd { el1_addr, el2_addr, address }` -- найти остаток от деления el1 на el2 и положить в ячейку по указанному адресу
- `cmp { el1_addr, el2_addr }` -- сравнить два элемента из памяти
- `jmp { address }` -- безусловный переход по заданному адресу или метке (используется для ControlUnit)
- `jz { address }` -- условный переход по заданному адресу или метке, если значение аккумулятора равно ноль
- `je { address }` -- условный переход по заданному адресу или метке, если в команде `cmp` первый элемент равен второму элементу
- `jb { address }` -- условный переход по заданному адресу или метке, если в команде `cmp` первый элемент больше второго элемента
- `jl { address }` -- условный переход по заданному адресу или метке, если в команде `cmp` первый элемент меньше второго элемента
- `in { port }` -- ввести извне значение и сохранить в аккумулятор (символ)
- `in { port, address }` -- ввести извне значение и сохранить в память начиная с текущей ячейки (последовательность символов)
- `out { port, type }` -- напечатать значение из текущей ячейки (символ)
- `halt` -- завершить выполнение программы

### Кодирование инструкций

- Машинный код сериализуется в список JSON.
- Один элемент списка -- одна инструкция.
- Индекс списка -- адрес инструкции. Используется для команд перехода.

Пример:

```json
[
  {
    "index": 0, 
    "operation": "add", 
    "arg": [21, 22, 23, 30]
  }
]
```

где:
- `index` -- адрес ячейки в памяти
- `operation` -- строка с кодом операции;
- `arg` -- аргумент (может отсутствовать);

## Транслятор

Интерфейс командной строки: `translator.py <input_file> <target_file>`

Реализовано в модуле: [translator](translator.py)

Этапы трансляции (функция `main`):

1. Очистка комментариев и лишних пробелов
2. Генерация машинного кода без адресов переходов
3. Подстановка меток перехода в инструкции.

## Модель процессора

