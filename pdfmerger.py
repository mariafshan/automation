from PyPDF2 import PdfFileReader, PdfFileMerger
from PIL import Image
import imghdr
import time

"""
pdfmerger.py ver. 20.9.25
This program convert image files to PDF then merge the PDF files.
HOW TO USE:
    1. Input 2 or more image or PDF files
    2. All image files will be converted to PDF
    3. All PDF files will be merged into 1 file

img checker = https://stackoverflow.com/questions/889333/how-to-check-if-a-file-is-a-valid-image-file
pdf merger = https://medium.com/@codeforests/split-or-merge-pdf-files-with-5-lines-of-python-code-c1fa710b4902
img2pdf = https://datatofish.com/images-to-pdf-python/
imgchecker = https://www.blog.pythonlibrary.org/2020/02/09/how-to-check-if-a-file-is-a-valid-image-with-python/
Automate the Boring Stuff with Python = https://automatetheboringstuff.com/
"""


def main():
    file_name = None
    file_name = input_filename(file_name)
    print("Files to be merged:")
    for i in range(len(file_name)):
        print(str(i + 1) + ".", file_name[i])
        time.sleep(0.5)
    pdf_merger(file_name)
    return


def pdf_merger(file_name):
    # list of files to be merged
    output = PdfFileMerger()
    for i in range(len(file_name)):
        # convert image files to pdf
        if img_check(file_name[i]):
            file = convert_image(file_name[i])
            file_name[i] = file
            time.sleep(0.5)

        # append file name to output list
        output.append(file_name[i])

    # save merged file
    mergedpdf_filename = file_name[0][:file_name[0].find(".p")] + "_merged.pdf"
    try:
        output.write(mergedpdf_filename)
    except:
        print("Files failed to merge.")
        return
    print(len(file_name), "files merged successfully. Merged file is saved as",
          mergedpdf_filename)
    return


def input_filename(file_name):
    if file_name == None:
        # list of file names to be merged
        file_name = list()

    # Prompting user to input file name
    while True:
        print("Enter file name or press Enter to continue.")
        filename = input("file_name.ext: ")
        time.sleep(1)

        # Exit the program
        if filename == "":
            if len(file_name) < 2:
                print("Please enter 2 or more files")
                input_filename(file_name)
            break
        # Check file
        elif file_check(filename) == False:
            continue

        # Append file name
        file_name.append(filename)
    return file_name

def file_check(filename):
    if pdf_check(filename):
        print("File is a valid PDF file")
        return True
    elif img_check(filename):
        imgtype = imghdr.what(filename)
        imgtype = imgtype.upper()
        print("File is a valid", imgtype, "file")
        return True
    else:
        print("Please enter valid PDF or image file")
        return False

def pdf_check(filename):
    try:
        # check PDF file
        filename = PdfFileReader(filename)
    except:
        return False
    return True

def img_check(filename):
    try:
        # check image file
        filename = Image.open(filename)
    except:
        return False
    return True

def convert_image(img_file):
    img = Image.open(img_file)
    new_pdf = img_file[:img_file.find(".")] + "_convert.pdf"
    print("Converting", img_file, "to", new_pdf + "...")
    imgtopdf = img.convert("RGB")
    try:
        imgtopdf.save(new_pdf)
        print("Conversion successful.")
    except:
        print("Failed to convert", img_file)
    return new_pdf

if __name__ == "__main__":
    main()
