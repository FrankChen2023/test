import unittest
from script_func import installChrome
from script_func import PDFSpliter
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from script_func import datasetGenerator


# test to check if webdriver installs and config chrome correctly
class TestChromeInstaller(unittest.TestCase):

    def test_install_chrome(self):
        chrome_service, chrome_options = installChrome()
        
        self.assertIsNotNone(chrome_service)
        self.assertIsNotNone(chrome_options)
        chrome_options.add_argument('--headless')
        self.assertIn('--headless', chrome_options.arguments)
      

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

class TestOpenChrome(unittest.TestCase):
    def test_openChrome(self):
        # Define the URL
        URL = "https://transkribus.ai/?htrid=36202"
        
        # Install and define chrome options and service
        chrome_service = Service("/path/to/chromedriver")
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
        
        # Open the Chrome browser and navigate to the URL
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        driver.get(URL)
        
        # Get the title of the page and assert that it is not empty
        wait = WebDriverWait(driver, 50)
        URLTitle = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'dropzone__input')))
        self.assertIsNotNone(URLTitle.text)
        
        # Close the browser
        driver.quit()


# Define the test data

def test_dataset_generator():
    contents = ["This is page 1", "This is page 2", "This is page 3"]
    new_page_symbol_1 = "new_page_symbol_1"
    new_page_symbol_2 = "new_page_symbol_2"
    
    datasetGenerator(contents, new_page_symbol_1, new_page_symbol_2)

    # Check if the output files exist in the correct folder
    assert os.path.exists('_datasets/test-1.md')
    assert os.path.exists('_datasets/test-2.md')
    assert os.path.exists('_datasets/test-3.md')

    # Check if the content of the output files is correct
    with open('_datasets/test-1.md', 'r') as f:
        expected_content = '---\nschema: default  \ntitle: test\norganization: Team Charlie\nnotes: "\n<p><b>Page.1</b></p>\nThis is page 1\n"\nresources: \ncategory: \n  - test \nmaintainer: maintainer\nmaintainer_email: maintainer_email\n---\n'
        assert f.read() == expected_content

    with open('_datasets/test-2.md', 'r') as f:
        expected_content = '---\nschema: default  \ntitle: test\norganization: Team Charlie\nnotes: "\n<p><b>Page.2</b></p>\nThis is page 2\n"\nresources: \ncategory: \n  - test \nmaintainer: maintainer\nmaintainer_email: maintainer_email\n---\n'
        assert f.read() == expected_content

    with open('_datasets/test-3.md', 'r') as f:
        expected_content = '---\nschema: default  \ntitle: test\norganization: Team Charlie\nnotes: "\n<p><b>Page.3</b></p>\nThis is page 3\n"\nresources: \ncategory: \n  - test \nmaintainer: maintainer\nmaintainer_email: maintainer_email\n---\n'
        assert f.read() == expected_content
if __name__ == '__main__':
 unittest.main()