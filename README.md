# PROJECT NAME
 Team Charlie --- Auto-transcribe and open-data system in Fraktur.

## Vision
 Once the user upload a PDF file, the application will do following things:  
 1. Split the PDF by pages and save all pages as PNG.  
 2. Scan every page and transcribe the words from Fraktur to modern German.  
 3. Group the content and pages by session flexibly and generate many source files according to the sessions.  
 4. Upload those files onto site and make them accessible.
 5. The site allows user to search and highlight keywords to locate their target quickly.
 6. All things will be done automatically.  
  
## Requirements
 The system uses github actions to install packages.  
 If running the system locally. Packages below are reuqired:  
    pyyaml  
    mdutils  
    pillow  
    PyMuPDF  
    beautifulsoup4  
    pandas  
    webdriver-manager  
    selenium  
  
## Building the application
 There are three periods during our project with many steps:
 1. Django system  
   1.1 Find the OCR library  
   1.2 Use tesseract for transcribing (But not accurate)  
   1.3 Build Django work  
   1.4 Use Mongodb for database
   1.5 Use Transkribus for OCR library instead  
   1.6 Remove Mongodb and use JSON instead  
   1.7 Build many functions basing on Django (Creating, catagorying, searching, editing, deleting)  
 2. Jkan system  
   2.1 Build open data system basing on Jkan  
   2.2 Immigrate data gradually  
   2.3 Adjust the layout/categories/organization and many other configs  
   2.4 Add more functions according to requirements of client  
 3. Automatic Jkan system  
   3.1 Use github actions  
   3.2 Write a python script to achieve all things automatically  

## Testing the build
How do I test the code to ensure the build is correct?
  
## Running the application
 The application will rerun it automatically powered by github actions.
  
## Team Members 
 
 Chen Zhaoqi

 Deborah Duke  

 Gulnoza Khamidova

 Henry Lutterodt

 Isaac Laryea

 Tao Luo

# Usage Manual

Before you make any difference to the repo, please check STEP and CAUTION below!!!
 
# STEP

## If you are adding/uploading some files onto the site on github, please follow the step below.  
1. Check your file, and it should be PDF type and at most 40 pages. The category and created data will be named according to the name of PDF.  
2. Find the script.py in the base path of the repo, and check the content from line-14 to line-36.  
3. Follw the comments, if the values are not correct, please adjust them manually.  
4. Fine and open the 'Source' dirctory in the  base path of the repo, and upload your file into the dirctory.  
5. Wait for a while and everything will be done automatically.  
6. You can check the github actions (click 'actions' above the repo and below the repo name). Please do not make any change before all actions finish.  
7. After all actions are done, you can check the created data files in '_datasets', and all created data files will name like 'PDFName-1.md', you can change it directly as you like, and you'd better change the title name as well when you change the file name, but please don't change the file type.  

## If you are adding/uploading some files onto the site on local device, please follow the step below. 
1-3. Same as the step 1 above.  
4. Please paste your PDF file in the Source directory.  
5. Then use git add/ git commit/git push(to the main branch) to make difference.  
6-7. Same as the step 1 above. 

# CAUTION
## Before you make difference, please check cautions below if you are not familiar with them.
1. Only PDF file can be accepted.  
2. To make the system work well, only 40 pages can be processed within 24 hours. If your file includes more than 40 pages, only the first 40 pages will be processed. If there are multiple PDFs are uploaded together, the total pages can not exceed 40.   
3. Your PDF will be deleted after the process done automatically to keep the source dirctory clear.  
4. The time of processing is according to how many pages in the PDF, generally 50 seconds for each page.  
5. Only main branch will call the github actions, so any change in sub-branch won't make difference to the site.  

# For administrator (the repo owner)
## Manage the repo and site
1. Upload files: the ways introduced above are suitable for both administrator and collaborators.  
2. Delete/Edit files: Go to the '_dataset' directory, then find and delete/edit the files you want directly.  
3. Delete/Edit categories: Go to the '_data' directory and fine 'categories.yml', then you can delete or hide categories as you want.  
4. Add organizations: Find the '_organizations' directory and create one .md type file as the form of existed file.  
## Give permission
### If you want to give others permission to contribute the repo. Please follow the step below.
1. Go to 'Setting' --> 'Collaborators' --> Check your account --> 'Manage access' Add people. Invite your collaborators into the repo. Then they could make changes.  
2. 'Setting' --> 'Actions' --> 'General' --> 'Workflow permissions'. Switch to 'Read and write permission' from 'Read repository contents and packages permissions'.  
## Maintainance Manual
### We strongly suggest you to maintain the site regularly for long-term usability.
1. Restart the site regularly (2-4 weeks). Go to Github repo --> Actions --> pages-build-deployment --> find the highest running process and click it --> Re-run all jobs.
2. Remove unneccessary datasets and images (any time if need). Go to Github repo --> fine '_datasets' and 'data_img' directories --> find the non-needed files and remove them.  

# Q&A
#### Q: I upload a PDF file, but I can not find the result files on the site.
A: In this case, please go to the '_datasets' dirctory and try to find the result files in it. The created files always name like 'PDFname-1.md'. If you can find some files in the directory and there are some contents in them, it means all things are alright, you can refresh the site page or try to clear your browser cookies and then open the site again. If you can not find any file names as the form, it means the process failed. Please check the step and caution above, and ensure that your input file and operating steps are in rule.
#### Q: When I upload a file and fail with 'that’s a big file. Try again with a file smaller than 25MB.  
A: Because github doesn't allow user to upload a file bigger than 25MB directly on github site. You can try to clone the repo to you local repo and move your PDF into the directory 'Source' and push it onto remote repo. If your PDF is larger than 100MB, please use Git LFS (Large File Storage).
#### Q: The github actions fail, the error is nothing to commit.
A: This situation always happen when you make changes but not upload file in 'Source' directory. Take it easy, it won't lead to any crash or unexpected.
#### Q: I upload a PDF file but no content in the result (created files).
A: It may happen if the system has processed more than 40 pages within 24 hours. When a same IP uses Trancribus frequently in a period, it will always receive a ban (last for 24 hours) from Transcribus. If so, please try your work after the ban, and notice that the existed files in '_dataset' may need to be deleted manually.
#### Q: I change the file name in the datasets, but it doesn't work on the site.
A: Please check whether you keep the title value same as the file name after you change. The name on the site is according to the title value, which is part of the content of files in datasets. You can find the line very easily in the '_datasets' --> open the file you change and edit it. We strongly suggest you to change the title value whenever you change the dataset filename.
#### Q: I want to immigrate the system into my repo or make another copy, how could I do?
A: We strongly suggest you to use github fork for this. Or you can clone the repo onto your local machine and then push onto your github repo. Next, go to [github application registration page](https://github.com/settings/applications/new) and register an application. You can name your application whatever you want, but you should keep Homepage URL and Authorization callback URL same and follow the form https://your-github-username.github.io/jkan . Notice that if you have already owned an application taking up the URL, then you should change another one like https://your-github-username.github.io/appname . Finally, copy the Client ID code, and go to '_config.yml' in repo and change the github_client_id to your application Client ID and change the baseURL to your appname in your Homepage URL entered above.
# Any other IT question:
#### Please contact team Charlie
#### Frank Chen (z.chen5.21@abdn.ac.uk / frankchen2202@163.com)
