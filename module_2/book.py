class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __repr__(self):
        return f'{self.__class__.__name__}: "{self.title}", "{self.author}"'

    def __eq__(self, other):
        return self.title == other.title and self.author == other.author

book1 = Book('Война и мир', 'Лев Толстой')
book2 = Book('Война и мир', 'Лев Толстой')
print(book1 == book2)
#True
