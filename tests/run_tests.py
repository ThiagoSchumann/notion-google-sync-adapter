import unittest

if __name__ == '__main__':
    # Carrega todos os testes dos módulos cujo nome começa com 'test_'
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')

    # Executa os testes
    runner = unittest.TextTestRunner()
    runner.run(test_suite)
