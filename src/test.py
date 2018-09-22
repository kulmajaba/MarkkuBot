# -*- coding: utf-8 -*-
from StringIO import StringIO
import unittest

from test.dummy_bot import DummyBot
from test.dummy_update import DummyUpdate
from test.dummy_message import DummyMessage
from test.dummy_chat import DummyChat
from test.dummy_user import DummyUser

from core.get_ids import get_ids

from db.database_abstraction import DatabaseAbstraction
from db.database_minimal import DatabaseMinimal

from command_handlers.start import start

update_generic = DummyUpdate(chat=DummyChat('609'), from_user=DummyUser('1377', 'kurkkumopo'))

class TestGetIds(unittest.TestCase):
    def test_equals(self):
        update = DummyUpdate(chat=DummyChat('609'), from_user=DummyUser('1377', 'kurkkumopo'))
        self.assertEqual(get_ids(update), ('1377', '609'))

@unittest.skip("Tietokanta ei vielä käytössä")
class TestStart(unittest.TestCase):
    def test_equals(self):
        out = StringIO()
        bot = DummyBot(out=out)
        start(bot, update_generic)
        botText = out.getvalue().strip()
        self.assertEqual(botText, "Woof woof")

class TestDatabaseMinimal(unittest.TestCase):
    def __init__(self, tc):
        unittest.TestCase.__init__(self, tc)
        db_imp = DatabaseMinimal()
        self.db = DatabaseAbstraction(db_imp)

    def test_blacklist_user(self):
        self.db.add_blacklist('kurkkumopo')
        self.db.add_blacklist('kurkkumopo')
        
        self.assertTrue(self.db.in_blacklist('kurkkumopo'))
        self.assertFalse(self.db.in_blacklist('toinen_user'))

        self.db.remove_blacklist('kurkkumopo')
        self.db.remove_blacklist('kurkkumopo')

        self.assertFalse(self.db.in_blacklist('kurkkumopo'))

    def test_counter_user(self):
        self.db.increment_counter('kurkkumopo', 'chatti', 'laskuri', 609)
        self.assertEqual(self.db.get_counter_user('kurkkumopo', 'chatti', 'laskuri'), 609)
        self.db.increment_counter('kurkkumopo', 'chatti', 'laskuri', 1)
        self.assertEqual(self.db.get_counter_user('kurkkumopo', 'chatti', 'laskuri'), 610)        
        self.db.get_counter_user('joku', 'joku', 'joku')

    def test_word_counter_user(self):
        self.db.word_collection_add('chatti', 'kurkkumopo', '', '', 'ebin', 3)
        self.db.word_collection_add('chatti', 'kurkkumopo', '', '', 'sana', 1)
        self.db.word_collection_add('chatti', 'eltsu7', '', '', 'ebin', 33)
        self.db.word_collection_add('chatti', 'eltsu7', '', '', 'sana', 12)  
        self.db.word_collection_add('chatti', 'markku', '', '', 'ebin', 3)
  
        self.assertEqual(self.db.word_collection_get_chat_user('chatti', \
            'kurkkumopo'), {'ebin': 3, 'sana': 1})

        self.assertEqual(self.db.word_collection_get_chat('chatti')['ebin'], 39)

if __name__ == '__main__':
    print("Yksikkötestit")
    unittest.main()