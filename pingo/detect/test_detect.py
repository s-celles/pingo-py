import unittest
import platform

import pingo
import pingo.detect


class DetectBasics(unittest.TestCase):

    def test_board(self):
        board = pingo.detect.get_board()
        assert isinstance(board, pingo.Board)

    @unittest.skipIf(not platform.system() == 'Linux', 'Not Linux')
    def test_read_cpu_info(self):
        info = detect._read_cpu_info()
        assert isinstance(info, dict)

if __name__ == '__main__':
    unittest.main()
