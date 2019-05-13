import sys, os
import glob
from PIL import Image


def paste_image(input_path, col_num, row_num, out_path):
    listdir = os.listdir(input_path)
    img_files = []
    for files in listdir:
        file_name = files.split('.')
        if file_name[-1] == 'jpg':
            img_files.append(files)

    # print(img_files)

    img_size_w = []
    img_size_h = []
    for i in range(len(img_files)):
        img = Image.open(os.path.join(input_path, img_files[i]))
        width, height = img.size
        img_size_w.append(width)
        img_size_h.append(height)

    # print(img_size_w, img_size_h)

    result_w = sum(img_size_w) / int(col_num)
    result_h = sum(img_size_h) / int(row_num)

    print(result_w, result_h)

    result = Image.new("RGB", (int(result_w), int(result_h)))
    img_idx = 0
    for iters in range(int(col_num)):
        for i in range(int(row_num)):
            piece = Image.open(os.path.join(input_path, img_files[img_idx]))
            img_idx += 1
            piece = piece.convert('RGB')
            i_width, i_height = piece.size
            box_x = int(i * i_width)
            box_y = int(iters * i_height)
            print("--------------")
            print(i)
            print(iters)
            print("--------------")
            print(box_x, box_y)
            result.paste(im=piece, box=(box_x, box_y))

    result.save(os.path.join(out_path, 'pasted.jpg'))


if __name__ == '__main__':
    input_path = sys.argv[1]
    column_number = sys.argv[2]
    row_number = sys.argv[3]
    out_path = sys.argv[4]

    paste_image(input_path, column_number, row_number, out_path)