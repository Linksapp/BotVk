import time

def main(func):
    def a(one_time=False):
        print(0)
        func(one_time)
        print(0)
        return []
    return a

@main
def c(c = None): print(c)

main_menu = {
		'Красная': 'negative', 
		'Зеленая': 'positive', 
		'Синяя': 'primary', 
		'Белая': 'secondary', 
		'': None,
		'Меню 2': 'secondary'
	}

c(1)