from PyPDF2 import PdfFileReader, PdfFileMerger, PdfFileWriter
from PIL import Image
import imghdr
import time

"""
pdfmerger.py ver. 20.9.26 by mariafshan
https://github.com/mariafshan/

This program convert image files to PDF then merge the PDF files.
HOW TO USE:
    1. Input 2 or more image or PDF files
    2. All image files will be converted to PDF
    3. All PDF files will be merged into 1 file

PyPDF2 documentation = https://pythonhosted.org/PyPDF2/ https://pythonhosted.org/PyPDF2/PageObject.html
PyPDF documentation = http://pybrary.net/pyPdf/pythondoc-pyPdf.pdf.html
img checker = https://stackoverflow.com/questions/889333/how-to-check-if-a-file-is-a-valid-image-file
pdf merger = https://medium.com/@codeforests/split-or-merge-pdf-files-with-5-lines-of-python-code-c1fa710b4902
img2pdf = https://datatofish.com/images-to-pdf-python/
imgchecker = https://www.blog.pythonlibrary.org/2020/02/09/how-to-check-if-a-file-is-a-valid-image-with-python/
Automate the Boring Stuff with Python = https://automatetheboringstuff.com/
PDF compression = https://stackoverflow.com/questions/22776388/pypdf2-compression
Extracting page size = https://stackoverflow.com/questions/6230752/extracting-page-sizes-from-pdf-in-python
Resizing PDF pages = https://stackoverflow.com/questions/6536552/resize-pdf-pages-in-python

"""

def main():
    file_name = None
    file_name = input_filename(file_name)
    print("Files to be merged:")
    for i in range(len(file_name)):
        print(str(i + 1) + ".", file_name[i])
        time.sleep(0.5)
    print("")
    new_file = pdf_merger(file_name)
    time.sleep(0.5)
    print("pdfmerger.py has completed checking, merging, scaling, and compressing. Files saved as", new_file + ".")
    return


# The actual main function of this program - merging files! Also shorter than than the compressor function haha!
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
    print("")
    compress_pdf(mergedpdf_filename)
    return mergedpdf_filename


# Prompt user to input file name and then check the file validity
def input_filename(file_name):
    if file_name == None:
        # list of file names to be merged
        file_name = list()

    # Prompting user to input file name
    while True:
        print("Enter file name or press Enter to continue.")
        filename = input("file_name.ext: ")
        time.sleep(0.5)

        # Exit the program
        if filename == "":
            if len(file_name) < 2:
                print("Please enter 2 or more files")
                input_filename(file_name)
            print("")
            break
        # Check file
        elif not file_check(filename):
            continue
        # Append file name
        file_name.append(filename)
    return file_name


# execute compress PDF, I should merge this helper function with the other helper function I think...
def compress_pdf(filename):
    # Execute PDF writer
    writer = PdfFileWriter()

    if not pdf_check(filename):
        print("Unable to compress", filename, ", merged PDF is saved uncompressed and unscaled.")

    # Open compressed PDF file
    reader = PdfFileReader(filename)

    # scale and compress PDF file
    smallest_page_width, smallest_page_height, smallest_page_area = find_smallest_page_area(reader)
    scale_page(reader, writer, filename, smallest_page_width, smallest_page_height, smallest_page_area)
    return


# resize the pages to make the PDF more uniform and easier to read, also compress the file
# I should decompose this helper function but atm I'm too lazy. Also I'm sure this helper function is still buggy.
def scale_page(reader, writer, filename, min_page_width, min_page_height, min_page_size):
    # Rezising pages
    smallestpage_orientation = orientation_check(min_page_width, min_page_height)

    for page_num in range(reader.numPages):
        page_size = reader.getPage(page_num).mediaBox
        page_width = page_size[2]
        page_height = page_size[3]
        page_area = page_width * page_height
        mintocurrwidth = float(min_page_width / page_width)
        mintocurrheight = float(min_page_height / page_height)

        # Scaling PDF file
        page = reader.getPage(page_num)
        print("smallest page width: ", str(min_page_width))
        print("smallest page height: ", str(min_page_height))
        print("smallest page area:", str(min_page_size))
        print("Current page size:", str(page_width), "x", str(page_height))
        print("")
        time.sleep(0.5)

        curr_page_orientation = orientation_check(page_width, page_height)
        print("This page is a", curr_page_orientation)
        print("")
        time.sleep(0.5)

        # if page has the same orientation
        if curr_page_orientation == smallestpage_orientation:
            if smallestpage_orientation == "square":
                resize_by = mintocurrwidth

            elif smallestpage_orientation == "portrait":
                if min_page_width >= page_width:
                    resize_by = mintocurrheight
                elif min_page_height <= page_height:
                    resize_by = mintocurrwidth
                else:
                    resize_by = mintocurrheight

            elif smallestpage_orientation == "landscape":
                if min_page_width >= page_width:
                    resize_by = mintocurrheight
                elif min_page_height <= page_height:
                    resize_by = mintocurrwidth
                else:
                    resize_by = mintocurrwidth

        # if page does not have the same orientation
        if curr_page_orientation != smallestpage_orientation:
            if smallestpage_orientation == "square":
                if curr_page_orientation == "landscape":
                    resize_by = mintocurrheight
                elif curr_page_orientation == "portrait":
                    resize_by = mintocurrwidth

            elif smallestpage_orientation == "portrait":
                resize_by = mintocurrheight

            elif smallestpage_orientation == "landscape":
                resize_by = mintocurrwidth

        print("Resizing page", str(page_num + 1), "by", str(resize_by * 100) + "%...")
        # scaling page
        try:
            page.scaleBy(resize_by)
            print("Page", str(page_num + 1), "is successfully scaled")
        except:
            print("Unable to scale page", str(page_num + 1))
        time.sleep(0.5)

        # compressing page
        print("Compressing page", str(page_num + 1) + "...")
        try:
            page.compressContentStreams()
            print("Page", str(page_num + 1), "is successfully compressed.")
            print("")
        except:
            print("Unable to compress page", str(page_num + 1))
        writer.addPage(page)
        time.sleep(1)

    # writing scaled PDF file
    with open(filename, "wb+") as file:
        writer.write(file)

    file.close()
    return


# finding the smallest page
def find_smallest_page_area(reader):
    page_sizes = dict()
    smallest_page_width = None
    smallest_page_height = None
    smallest_page_area = None

    # Measuring the page sizes
    for page in range(reader.numPages):
        page_size = reader.getPage(page).mediaBox
        page_width = page_size[2]
        page_height = page_size[3]
        page_area = page_width * page_height

        if smallest_page_area == None or page_area < smallest_page_area:
            smallest_page_area = page_area
            smallest_page_height = page_height
            smallest_page_width = page_width

        #     This dictionary might be useful someday....
        page_sizes[page] = page_sizes.setdefault(page, [page_width, page_height])

    print("Page sizes:", page_sizes)
    time.sleep(0.5)
    print("Smallest page area:", smallest_page_area)
    print("Smallest page width:", smallest_page_width)
    print("Smallest page heigt:", smallest_page_height)
    print("")
    time.sleep(0.5)
    return smallest_page_width, smallest_page_height, smallest_page_area


# Check if page is landscape/ portrait/ square
def orientation_check(width, height):
    if width > height:
        return "landscape"
    if height > width:
        return "portrait"
    if height == width:
        return "square"
    return


# Convert image file to PDF
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
        print("")
    return new_pdf


# Check if user input file is valid
def file_check(filename):
    if pdf_check(filename):
        print("File is a valid PDF file")
        print("")
        return True
    elif img_check(filename):
        imgtype = imghdr.what(filename)
        imgtype = imgtype.upper()
        print("File is a valid", imgtype, "file")
        print("")
        return True
    else:
        print("Please enter valid PDF or image file")
        print("")
        return False


# check if PDF file can be opened
def pdf_check(filename):
    try:
        filename = PdfFileReader(filename)
    except:
        return False
    return True


# check if image file can be opened
def img_check(filename):
    try:
        filename = Image.open(filename)
    except:
        return False
    return True


if __name__ == "__main__":
    main()
