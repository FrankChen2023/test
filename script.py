from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager, ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import shutil
import os
import fitz
import yaml
import time

###############################################################################
# -----------------------------------------------------------------------------
# This part should be filled flexibly by user.

# It means the beginning of page number in a file.
# If you set it equal to 99 so that both the first page number and the first paragraph number will be 99.
first_page = 1

# The keywords symboling a new page.
# When both keywords show in one page, and then it will finish last page and start one new file.
# If there is only one keyword symboling new page, you can keep another one as ''.
new_page_symbol_1 = 'Geschehen'
new_page_symbol_2 = 'Frankfurt'

# The orgnization and maintainer of the files.
# The orgnization can help to locate the file easily.
# The maintainer should be the one who upload the file.
organization = 'Team Charlie'
maintainer_name = 'Frank Chen'
maintainer_email = 'z.chen5.21@abdn.ac.uk'

# ------------------------------------------------------------------------------
################################################################################

# Install chrome and set the options.
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

files = os.listdir("Source")

# Define the statement of new_page.
new_page = 'beginning'

# Define the session number of the PDF
session = 1

# When there is another file except keeper, it runs.
while len(files) > 1:
    for file in files:
        if file == 'keeper':
            continue
        else:
            pdf_name = file 
            break
    
    # Define the path to the PDF file
    pdf_path = "Source/" + pdf_name

    # Define the directory where the PNG files will be saved
    output_dir = "data_img/" + pdf_name[:-4]

    # Load the list of datasets
    datasets = os.listdir("_datasets")

    try:

        # Build the dirctory to save the images
        os.mkdir(output_dir)

    except:
        pass

    
    # Load the list of data_img
    data_img = os.listdir(output_dir)

    # Open the PDF using PyMuPDF
    pages = fitz.open(pdf_path)

    # Record the last page number.
    final_page = len(pages) - 1
    
    # Iterate over each page of the PDF
    for page_num_1, page in enumerate(pages): 

        # More than 40 pages each time will lead to a ban from Transkribus.
        if page_num_1 == 40:
            break

        # Page number starts from 1.
        page_num = page_num_1 + first_page

        # Every page's name
        filename = "Page[" + str(page_num) + "].png"

        # If the filename exists in the data_img dirctory, page_num should change.
        while 1:
            if filename in data_img:
                first_page += 1
                page_num = page_num_1 + first_page
                filename = "Page[" + str(page_num) + "].png"
            else:
                break

        # Render the page as a PNG image
        pic = page.get_pixmap(alpha=False)

        # Define the filename for the PNG file
        filepath = os.path.join(output_dir, filename)

        # Save the PNG file
        pic.save(filepath)

        # Define using chrome
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        # Reach to the Transkribus site
        driver.get('https://transkribus.ai/?htrid=36202')

        # Upload the PNG
        driver.find_element(By.CLASS_NAME, 'dropzone__input').send_keys(os.getcwd()+'/'+output_dir+'/'+filename)

        # Wait for the transcription
        time.sleep(45)

        # Get the result
        res_lines = driver.find_elements(By.CLASS_NAME, 'result__line')

        # Define digit text
        content = ""
        for line in res_lines:
            line_text = line.text

            # Change all " to ' for avoiding error
            line_text = line_text.replace('"', "'")

            content = content + line_text + '\n'

        # Close the site
        driver.quit()

        while 1:

            # If new_page equals 'beginning', it means this is a beginning of a new page.
            if new_page == 'beginning':

                # Start page number in resources.
                start_page = page_num

                # Define the text file name.
                text_name = pdf_name[:-4] + "-" + str(session) + '.txt'

                # Change text file into md file and move it into _datasets foleder.
                mdfile = text_name[:-4] + '.md'
                
                # If md_name is in the datasets, session should change.
                while 1:
                    if mdfile in datasets:
                        session += 1
                        text_name = pdf_name[:-4] + "-" + str(session) + '.txt'
                        mdfile = text_name[:-4] + '.md'
                    else:
                        break

                # Create a new session file and Write the general beginning content into text file.
                with open (text_name, 'w', encoding='utf-8') as file:
                    file.write('---')
                    file.write('\n')
                    file.write('schema: default  ')
                    file.write('\n')
                    file.write('title: ' + text_name[:-4])
                    file.write('\n')
                    file.write('organization: ' + organization)
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
                        file.write('  url: ../../' + output_dir + '/Page[' + str(num) + '].png ')
                        file.write('\n')
                    
                    # Add the category.
                    file.write('category: ')
                    file.write('\n')
                    file.write('  - ' + pdf_name[:-4] + ' ')
                    file.write('\n')
    
                    # Add the maintainer. Frank Chen who is the software developer.
                    file.write('maintainer: ' + maintainer_name)
                    file.write('\n')
                    file.write('maintainer_email: ' + maintainer_email)
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
    
    # Load the categories file and add the new category.
    with open("_data/categories.yml") as f:
        list_doc = yaml.safe_load(f)

        # Define the category_re, which means whether the category exists or not.
        category_re = 1

        # If it is not a new category. category_re = 0.
        for category in list_doc:
            if pdf_name[:-4] == category['name']:
                category_re = 0
                break
        
        # If category_re == 1, it means this is a new category, so create it.
        if category_re == 1:
            new_catagory = {'name': pdf_name[:-4], 'logo': '/img/categories/uncategorized.svg', 'logo_credit': 'Edward Boatman from the Noun Project', 'featured': True}
            list_doc.append(new_catagory)

    with open("_data/categories.yml", 'w') as f:
        yaml.dump(list_doc, f)

    # Skip out of the loop.
    break

# Delete the source file. 
try:  
    os.remove(pdf_path)
except:
    pass
    