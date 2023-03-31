# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager, ChromeType
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# import shutil
# import os
# import fitz
# import yaml
# import time



# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

# The function of installChrome.

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager, ChromeType
from selenium.webdriver.chrome.options import Options

def installChrome():
    chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

    chrome_options = Options()
    options = [
        "--headless",
        "--disable-gpu",
        "--window-size=1920,1200",
        "--ignore-certificate-errors",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage"
    ]
    for option in options:
        chrome_options.add_argument(option)
    
    return [chrome_service, chrome_options]

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

# The function of spliting the PDF into images.

import os
import fitz

# pdf_path is the path of the PDF. type: string. eg: home/source/sample.pdf   
# output_dir is the path of the generated images save in. type: string.  eg: home/result/sample/
# first_page is the page number of first page. type: int. 

def PDFSpliter(pdf_path, output_dir, first_page=1):   

    # Load the list of data_img
    data_img = os.listdir(output_dir)

    # Open the PDF using PyMuPDF
    pages = fitz.open(pdf_path)
    
    # Iterate over each page of the PDF
    for page_num_1, page in enumerate(pages): 

        # More than 40 pages each time will lead to a ban from Transkribus.
        if page_num_1 == 40:
            break

        # Page number starts from 1.
        page_num = page_num_1 + first_page

        # Every page's name
        filename = "Page[" + str(page_num) + "].png"

        # Render the page as a PNG image
        pic = page.get_pixmap(alpha=False)

        # Define the filename for the PNG file
        filepath = os.path.join(output_dir, filename)

        # Save the PNG file
        pic.save(filepath)
    
    return None

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

# The function of openning the chrome.

from selenium import webdriver
from selenium.webdriver.common.by import By

# URL is the target URL. type: string

def openChrome(URL):
        
        # Install the chrome
        chrome = installChrome()
        chrome_service, chrome_options = chrome
        
        # Define using chrome
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        # Reach to the Transkribus site
        driver.get(URL)

        # Print the title
        URLTitle = driver.find_element(By.CLASS_NAME, 'title')

        # Close the site
        driver.quit()

        return URLTitle

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

import shutil

# Generate the dataset.
# contents is the dataset content. type: list. Element type: string.
# Example: contents = ['first page title', 'first page content1', 'first page content 2', 'second page title', 'second page content']
# new_page_symbol should be the keywords signning a new session. type: string. Example: 'title'

def datasetGenerator(contents, new_page_symbol_1, new_page_symbol_2):

    # Define the PDF name.
    pdf_name = 'test.pdf'

    # Define the final page.
    final_page = len(contents)

    # Define the indice.
    page_num_1 = 1

    # Define the new_page status.
    new_page = 'beginning'

    while page_num_1 <= final_page:

        content = contents[page_num_1-1]

        # If new_page equals 'beginning', it means this is a beginning of a new page.
        if new_page == 'beginning':

            # Start page number in resources.
            start_page = page_num

            # Define the text file name.
            text_name = pdf_name[:-4] + "-" + str(session) + '.txt'

            # Change text file into md file and move it into _datasets foleder.
            mdfile = text_name[:-4] + '.md'

            # Create a new session file and Write the general beginning content into text file.
            with open (text_name, 'w', encoding='utf-8') as file:
                file.write('---')
                file.write('\n')
                file.write('schema: default  ')
                file.write('\n')
                file.write('title: ' + text_name[:-4])
                file.write('\n')
                file.write('organization: Team Charlie')
                file.write('\n')
                file.write('notes: "')
                file.write('\n')
                file.write('<p><b>Page.' + str(page_num) + '</b></p>')
                file.write('\n')
                file.write(content)
                file.write('\n')

            # Close the file.
            file.close()

            # New_page equals 'continue', it means the content continues.
            new_page = 'continue'

            # Then the beginning page with the content finishes.
            # when the page is not the final page.
            if page_num_1 != final_page:
                break
        
        # If new_page equals 'continue', it means the content should follow the existed text.
        if new_page == 'continue' and (new_page_symbol_1 not in content) or (new_page_symbol_2 not in content):

            with open (text_name, 'a', encoding='utf-8') as file:

                # Write the continuous content.
                file.write('<p></p>')
                file.write('<p><b>Page.' + str(page_num) + '</b></p>')
                file.write('\n')
                file.write(content)
                file.write('\n')

            # Close the file.
            file.close()

            # Then the content finishes when the page is not the final page.
            if page_num_1 != final_page:
                break
            

        # If new_page equals 'continue' and new_page_symbol is in the content.
        # It means one file ends and it should be closed.
        if page_num_1 == final_page or (new_page == 'continue' and new_page_symbol_1 in content and new_page_symbol_2 in content):
            
            # If this is the final page, add one to ensure the last page will be in the resources.
            if page_num_1 == final_page:
                page_num += 1

            with open (text_name, 'a', encoding='utf-8') as file:

                # Close the notes sesstion.
                file.write('"')
                file.write('\n')

                # Write the rest general part. Resources and maintain sesstion.
                file.write('resources: ')
                file.write('\n')

                # For loop to fill the resources. From start page number to current page number.
                for num in range(start_page, page_num):
                    file.write('- format: png ')
                    file.write('\n')
                    file.write('  name: Page[' + str(num) + '].png ')
                    file.write('\n')
                    file.write('  url: ../../' + '/Page[' + str(num) + '].png ')
                    file.write('\n')
                
                # Add the category.
                file.write('category: ')
                file.write('\n')
                file.write('  - ' + pdf_name[:-4] + ' ')
                file.write('\n')

                # Add the maintainer. Frank Chen who is the software developer.
                file.write('maintainer: maintainer')
                file.write('\n')
                file.write('maintainer_email: maintainer_email')
                file.write('\n')
                file.write('--- ')
                file.write('\n')

            # Close the file.
            file.close()

            # Change the statement from 'continue' to 'beginning'
            new_page = 'beginning'

            # Change the file type from txt to md and move it into datasets.
            shutil.copyfile(text_name, mdfile)
            os.remove(text_name)
            shutil.move(mdfile, '_datasets/' + mdfile)

            # Session increase.
            session += 1

            # However, this page has not been stored if it not the final page.
            # Notice that page_num has been added 1 if it is the final page.
            if page_num_1 == final_page:
                break
            else:
                continue
            
    return None

    