class Students:
    name = []

    def set_name(self, user_name):
        self.name.append(user_name)
        return len(self.name) - 1

    def get_name(self, user_id):
        if user_id >= len(self.name):
            return 'There is no such user'
        else:
            return self.name[user_id]


if __name__ == '__main__':
    students = Students() # pragma: no cover
    print("id", students.set_name('John')) # pragma: no cover
    print("name", students.get_name(0)) # pragma: no cover