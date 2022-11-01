import pytesseract
from PIL import Image, ImageDraw as ID
import os
import shutil
from datetime import datetime

pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

book_dir = os.getcwd()
chapter_dir = book_dir + '/' + 'Chapter-1'
page_dir = chapter_dir + '/' + 'Page-1'

os.chdir(page_dir)


#input_file_name = 'Page-1.png'
#input_file_name ='biform 2.gif'
input_file_name ='gallup 308 Aug Sci 1623.jpg'

input_file_path = page_dir + '/' + input_file_name

isExist = os.path.exists(input_file_path)
if not isExist:
  print('Input file ' + input_file_name + ' is non-existent')
else:
  img = Image.open(input_file_path)

  if not ('img' in locals()):
    print('Image file ' + input_file_name + ' not read')

  today_dir_name = datetime.today().strftime('%m_%d_%Y')
  isExist = os.path.exists(today_dir_name)
  if not isExist:
    os.makedirs(today_dir_name)
  os.chdir(today_dir_name)

  hours = datetime.today().strftime('%H')
  minutes = datetime.today().strftime('%M')
  seconds = datetime.today().strftime('%S')

  now_dir_name = hours + '-' + minutes + '-' + seconds
  now_dir_path = now_dir_name
  isExist = os.path.exists(now_dir_path)
  if not isExist:
    os.makedirs(now_dir_path)

  os.chdir(now_dir_path)

  # back up the input file to current directory.
  isExist = os.path.exists('../../' + input_file_name)
  # if not isExist:
  dst = os.getcwd()
  shutil.copy('../../' + input_file_name, dst)

draw = ID.Draw(img)

boxes = pytesseract.image_to_boxes(img)
letter_data = boxes.splitlines()


def save_letter(letterIndex):
  r4: list[int] = []
  for i in letter_data[letterIndex].split()[1:5]:
    r4.append(int(i))

  letter = letter_data[letterIndex][0]

  r4 = (r4[0], img.size[1] - r4[3], r4[2], img.size[1] - r4[1])
  cropped_img = img.crop(r4)

  letter_dir = os.getcwd()
  letter_path = letter_dir + '/' + 'letter' + str(letterIndex) + '_' + letter + '.png'

  cropped_img.save(letter_path)

  draw.rectangle((r4[0], r4[3], r4[2], r4[1]), outline="green")

# Dissect the original Page source image by cropping to the bounding boxes of the letters,
# saving each letter to its own png file:
text_read = range(len(letter_data))

for li in text_read:
  save_letter(li)

# Save a copy of the source Page image, now annotated, to file:
img.save('Page-1 boxes' + '.png')

