

def show(filename):
    import importlib.resources as pkg_resources
    from IPython.display import display, Image
    package = "theory"
    filename += '.png'
    try:
        with pkg_resources.path(package, filename) as file_path:
            img = Image(filename=str(file_path))
            display(img)
    except Exception as e:
        print(f'Неправильное имя файла: {e}')
    return filename


def show_pdf(filename):
    import importlib.resources as pkg_resources
    from IPython.display import display, IFrame
    package = "numpyp.theory"
    filename += '.pdf'
    try:
        with pkg_resources.path(package, filename) as file_path:
            # Создаем IFrame для отображения PDF
            pdf_iframe = IFrame(src=str(file_path), width=1000, height=800)
            display(pdf_iframe)
    except Exception as e:
        print(f'Неправильное имя файла: {e}')
    return filename

def vec():
    show('1')
    show('2')
    show('3')
    show('4')


def func1():
    print('1 z_1_1() переполнение')
    print('1 z_1_2() Потеря точности')
    print('1 z_1_3() Ошибки округления')
    print('1 z_1_4() Накопление ошибок')
    print('1 z_1_5() Потеря значимости')
    print('1 z_1_6() Суммирование по Кахану')
    print('1 z_1_7() Суммирование по Кахану vs обычное vs numpy')

def func2():
    print('2 z_2_1() Метод простых итераций  ')
    print('2 z_2_2() Метод хорд ')
    print('2 z_2_3() Метод вегстейна')
    print('2 z_2_4() Метод ньютона ')

def func3():
    print('3 z_3() Метод дихотомии')

def func4():
    print('4 z_4_1() Простые итерации ')
    print('4 z_4_2() Метод зейделя')
    print('4 z_4_3() Метод ньютона ')
    print('4 z_4_4() Модифицированный метод ньютона')

def func5():
    print('5 z_5_1() определения ')
    print('5 z_5_2() простая интерполяция')
    print('5 z_5_3() линейная интерполяция')
    print('5 z_5_4() интерполяционные полиномы ')
    print('5 z_5_5() интерполяционный многочлен Лагранжа ')
    print('5 z_5_6() Интерполяция Кубический сплайн ')
    print('5 z_5_7() Квадратичная интерполяция')
    print('5 z_5_8() Интерполяция сплайнами ')
    print('5 z_5_9() Метод наименьших квадратов')




