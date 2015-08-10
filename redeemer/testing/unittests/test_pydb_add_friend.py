import unittest
import mock
from redeemer.pydb import add_friend_to_pydb


@mock.patch('redeemer.pydb._call_pydb_tool', return_value=0)
class TestAddFriendToPydb(unittest.TestCase):
    def test_add_friend_calls_pydb_tool_with_add_friend_and_friend_name(self, call_pydb_tool_mock):
        add_friend_to_pydb('friend', 'we dont have a secret')
        call_pydb_tool_mock.assert_any_call('add_friend', 'friend')

    def test_add_friend_calls_pydb_tool_with_set_comm_data_tcp_aes_friend_name_and_secret(self, call_pydb_tool_mock):
        add_friend_to_pydb('friend', 'we have a secret')
        call_pydb_tool_mock.assert_any_call('set_comm_data_tcp_aes', 'friend', '', '', 'we have a secret')

    def test_add_friend_raises_value_error_when_add_friend_call_fails(self, call_pydb_tool_mock):
        call_pydb_tool_mock.return_value = 1
        with self.assertRaises(ValueError):
            add_friend_to_pydb('friend', 'we dont have a secret')

    def test_add_friend_rasies_value_error_when_set_comm_data_tcp_aes_fails(self, call_pydb_tool_mock):
        call_pydb_tool_mock.side_effect = [0, 1]
        with self.assertRaises(ValueError):
            add_friend_to_pydb('friend', 'we have a secret')


if __name__ == '__main__':
    unittest.main()
