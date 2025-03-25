RESOURCE = 'YOOTK - 沐言科技'
class Book:
    def __init__(self,**kwargs):
        self.__name = kwargs.get('name')
        self.__author = kwargs.get('author')
    def __str__(self):
        return f'【图书】名称：{self.__name}，作者：{self.__author}'
class Press:
    def publish(self,book):
        print(f'【图书出版】：{book}')