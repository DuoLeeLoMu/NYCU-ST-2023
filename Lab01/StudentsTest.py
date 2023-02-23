import unittest
import Students

class Test(unittest.TestCase):
    students = Students.Students()

    user_name = ['John', 'Mary','Thomas','Jane']
    user_id = []

    # test case function to check the Students.set_name function
    def test_0_set_name(self):
        print("Start set_name test\n")
        # set student id
        for name in self.user_name:
            user_id = self.students.set_name(name)
            self.user_id.append(user_id)

        # print student id and name
        for i in range(len(self.user_id)):
            print(self.user_id[i], self.user_name[i])

        print("\nFinish set_name test\n\n")


    # test case function to check the Students.get_name function
    def test_1_get_name(self):
        print("Start get_name test\n")
        print("user_id length = ", len(self.user_id))
        print("user_name length = ", len(self.user_name), "\n")
        # test
        n = len(self.user_id)
        for i in range(n):
            if self.assertEqual(self.user_name[i], self.students.get_name(self.user_id[i])) == None:
                print("id", self.user_id[i], ":", self.user_name[i])

        temp = set(self.user_id)
        mex = 0
        while mex in temp:
            mex += 1

        print("id", mex, ":", self.students.get_name(mex))

        
        print("\nFinish get_name test\n\n")

if __name__ == '__main__':
    unittest.main() # pragma: no cover