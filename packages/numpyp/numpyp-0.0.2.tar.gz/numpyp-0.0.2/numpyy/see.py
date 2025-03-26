

def show(filename):
    import importlib.resources as pkg_resources
    from IPython.display import display, Image
    package = "varr_0.theory"
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
    package = "varr_0.theory"
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
    show('photo_2025-01-13_17-12-00')
    show('photo_2025-01-13_19-55-34')
    show('photo_2025-01-13_17-30-02')
    show('photo_2025-01-13_17-30-02 (2)')
    show('photo_2025-01-13_17-30-02 (3)')
    show('photo_2025-01-13_17-30-02 (4)')
    show('photo_2025-01-13_19-00-29')


def func1():
    print('1 z_1_1() переполнение')
    print('1 z_1_2() Потеря точности')
    print('1 z_1_3() Ошибки округления')
    print('1 z_1_4() Накопление ошибок')
    print('1 z_1_5() Потеря значимости')
    print('1 z_1_6() Суммирование по Кахану')
    print('1 z_1_7() Суммирование по Кахану vs обычное vs numpy')


