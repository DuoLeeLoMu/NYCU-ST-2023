import unittest
from app import Application, MailSystem
from unittest.mock import Mock, patch

class ApplicationTest(unittest.TestCase):
    def setUp(self):
        self.people = ["William", "Oliver", "Henry", "Liam"]
        self.selected = ["William", "Oliver", "Henry"]
        return self.people, self.selected

    def fake_mail(self, name):
        context = 'Congrats, ' + name + '!'
        return context
            
        
    def test_app(self):
        people, selected = self.setUp() 
        
        # Application
        ApplicationTest.get_random_person = Mock(side_effect=people)
        selected_person = Application.select_next_person(self)
        # Correct answer
        if self.assertEqual(selected_person, "Liam") == None:
            print(selected_person, "selected")
        

        # MailSysem
        with patch.object(MailSystem, 'write', side_effect=self.fake_mail) as mock_write, \
          patch.object(MailSystem, 'send') as mock_send:
            ApplicationTest.mailSystem = Mock(spec=MailSystem)
            Application.notify_selected(self)
            # print the mail context
            for person in selected:
                context = mock_write(person)
                print(context)
                mock_send(person, context)
        # Examine the call count of send() and write()
        self.assertEqual(ApplicationTest.mailSystem.write.call_count, 4)
        self.assertEqual(ApplicationTest.mailSystem.send.call_count, 4)
        print("\n")
        print(mock_write.call_args_list)
        print(mock_send.call_args_list)


if __name__ == "__main__":
    unittest.main()