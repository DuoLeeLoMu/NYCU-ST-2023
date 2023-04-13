import unittest
from course_scheduling_system import CSS
from unittest.mock import Mock


class CSSTest(unittest.TestCase):
    css = CSS()

    def test_q1_1(self):
        self.css.check_course_exist = Mock(return_value=True)
        result = self.css.add_course(('Algorithm', 'Monday', 3, 4))
        with self.subTest():
            self.assertTrue(result)
            self.assertEqual(self.css.get_course_list(), [
                             ('Algorithm', 'Monday', 3, 4)])

    def test_q1_2(self):
        self.css.check_course_exist = Mock(return_value=True)
        self.css.add_course(('Network Se', 'Thursday', 3, 4))
        result = self.css.add_course(('Network Se', 'Thursday', 3, 4))
        with self.subTest():
            self.assertFalse(result)
            self.assertEqual(self.css.get_course_list(), [
                             ('Algorithm', 'Monday', 3, 4), ('Network Se', 'Thursday', 3, 4)])

    def test_q1_3(self):
        self.css.check_course_exist = Mock(return_value=False)
        result = self.css.add_course(('PL', 'Tuesday', 3, 4))
        with self.subTest():
            self.assertFalse(result)
            self.assertEqual(self.css.get_course_list(), [
                             ('Algorithm', 'Monday', 3, 4), ('Network Se', 'Thursday', 3, 4)])

    def test_q1_4(self):
        self.css.check_course_exist = Mock(return_value=True)
        with self.subTest():
            with self.assertRaises(TypeError):
                self.css.add_course((1, 'Tuesday', 3, 4))

    def test_q1_5(self):
        self.css.check_course_exist = Mock(return_value=True)
        # add third courses
        self.css.add_course(('PL', 'Tuesday', 1, 2))
        self.css.add_course(('Algorithm', 'Tuesday', 3, 4))
        self.css.add_course(('Network Se', 'Tuesday', 5, 6))
        # remove second course
        self.css.remove_course(('Algorithm', 'Tuesday', 3, 4))
        with self.subTest():
            self.assertEqual(self.css.get_course_list(), [('Algorithm', 'Monday', 3, 4), (
                'Network Se', 'Thursday', 3, 4), ('PL', 'Tuesday', 1, 2), ('Network Se', 'Tuesday', 5, 6)])
            self.assertEqual(self.css.check_course_exist.call_count, 4)

        print(self.css)

    def test_q1_6(self):
        self.css.check_course_exit = Mock(return_value=True)
        result = self.css.remove_course(('PL', 'Monday', 3, 4))
        with self.subTest(self):
            self.assertFalse(result)
            with self.assertRaises(TypeError):
                self.css.add_course(('PL', '1', 3, 4))
            with self.assertRaises(TypeError):
                self.css.add_course(('PL', 'Tuesday', '3', 4))
            with self.assertRaises(TypeError):
                self.css.add_course(('PL', 'Tuesday', '3'))

        self.css.check_course_exist = Mock(return_value=False)
        result = self.css.remove_course(('PL', 'Monday', 3, 4))
        with self.subTest(self):
            self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
