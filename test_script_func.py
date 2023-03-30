import unittest
from script_func import installChrome
from script_func import PDFSpliter
import os


# test to check if webdriver installs and config chrome correctly
class TestChromeInstaller(unittest.TestCase):

    def test_install_chrome(self):
        chrome_service, chrome_options = installChrome()
        
        self.assertIsNotNone(chrome_service)
        self.assertIsNotNone(chrome_options)
        self.assertTrue(chrome_options.headless)
        self.assertEqual(chrome_options.window_size, '1920,1200')

# test to check if pdfsplitter function creates directory and saves at least one file
class TestPDFSpliter(unittest.TestCase):

    # create the output directory if it doesn't exist
    if not os.path.exists("output"):
     os.makedirs("output")

    def test_PDFSpliter(self):
        # Define test input values
        pdf_path = "test.pdf"
        output_dir = "output"
        first_page = 1

        # Call the function
        PDFSpliter(pdf_path, output_dir, first_page)

        # Check that the output directory was created
        self.assertTrue(os.path.isdir(output_dir))

        # Check that the output directory contains files
        self.assertGreater(len(os.listdir(output_dir)), 0)



if __name__ == '__main__':
 unittest.main()