import unittest
from src.main import main

class TestMain(unittest.TestCase):
    def test_main(self):
        # 测试 main 函数是否能正确输出 "Hello, world!"
        self.assertEqual(main(), None)

if __name__ == "__main__":
    unittest.main()