import numpy as np
import os,sys
import PIL.Image as pilimg
import math
import operator
import cv2


def paste_img(input_path):
    listdir = os.listdir(input_path)
    img_list = []
    for i in listdir:
        if i.split('.')[-1] == 'jpg':
            img_list.append(i)
    print(img_list)

    edges_dict = {}
    pieces_dict = {}
    for img in img_list:
        open_img = pilimg.open(os.path.join(input_path, img))
        img_w, img_h = open_img.size
        img_array = np.array(open_img)
        pieces_dict[img.split('.')[0]] = img_array
        edge1 = img_array[0, :]
        edge2 = img_array[:, int(img_w - 1)]
        edge3 = img_array[int(img_h - 1), :]
        edge4 = img_array[:, 0]
        edges = [edge1, edge2, edge3[::-1], edge4[::-1]]
        edges_dict[img.split('.')[0]] = edges

    cost_dict = {}
    for key1, edges1 in edges_dict.items():
        for key2, edges2 in edges_dict.items():
            if key1 == key2:
                continue
            if key1 < key2:
                name1 = key1
                name2 = key2
                tmp_edges1 = edges1
                tmp_edges2 = edges2
            else:
                name1 = key2
                name2 = key1
                tmp_edges1 = edges2
                tmp_edges2 = edges1

            for idx1 in range(0, len(tmp_edges1)):
                for idx2 in range(0, len(tmp_edges2)):
                    cost_key = name1 + str(idx1) + name2 + str(idx2)
                    cost_key_2 = name1 + name2
                    if cost_key in cost_dict:
                        continue
                    cost_dict[cost_key, cost_key_2] = get_distance_between(tmp_edges1[idx1], tmp_edges2[idx2])

    cost_dict_sort = sorted(cost_dict.items(), key=operator.itemgetter(1))

    final_dict = {}
    used_list = []
    for i in range(len(cost_dict_sort)):
        if cost_dict_sort[i][0][1] in used_list:
            continue
        else:
            final_dict[cost_dict_sort[i][0][0]] = cost_dict_sort[i][1]
            used_list.append(cost_dict_sort[i][0][1])

    print(final_dict)

    pieces = []
    piece_num_edge = {}
    for key, val in final_dict.items():

        piece1_num = key[0:2]
        piece1_edge = key[2]
        piece2_num = key[3:5]
        piece2_edge = key[5]

        update_piece_edge_dict(piece1_num, piece1_edge, piece_num_edge)
        update_piece_edge_dict(piece2_num, piece2_edge, piece_num_edge)

    list1 = ['1', '2']
    list2 = ['2', '3']
    list3 = ['0', '1']
    list4 = ['0', '3']
    sorted_val_list = []
    for i in piece_num_edge.items():
        sorted_val_list.append(i)
        sorted_val = sorted(i[1])
        if sorted_val == list1:
            pieces.append(i[0])
        else:
            continue

    for i in piece_num_edge.items():
        sorted_val_list.append(i)
        sorted_val = sorted(i[1])
        if sorted_val == list2:
            pieces.append(i[0])
        else:
            continue

    for i in piece_num_edge.items():
        sorted_val_list.append(i)
        sorted_val = sorted(i[1])
        if sorted_val == list3:
            pieces.append(i[0])
        else:
            continue

    for i in piece_num_edge.items():
        sorted_val_list.append(i)
        sorted_val = sorted(i[1])
        if sorted_val == list4:
            pieces.append(i[0])
        else:
            continue

    pieces_in_order = []
    for piece in pieces:
        pieces_in_order.append(pieces_dict[piece])
    return pieces_in_order


def update_piece_edge_dict(piece_num, piece_edge, piece_num_edge):
    if piece_num not in piece_num_edge:
        piece_num_edge[piece_num] = [piece_edge]
    else:
        if len(piece_num_edge[piece_num]) >= 2:
            return
        else:
            piece_num_edge[piece_num].append(piece_edge)


def get_distance_between(edge1, edge2):

    if len(edge1) != len(edge2):
        return 9999999999

    distance = 0
    length = len(edge1)
    for index in range(length):
        distance += math.sqrt( (float(edge1[index][0]) - float(edge2[length-index-1][0])) ** 2 +
                               (float(edge1[index][1]) - float(edge2[length-index-1][1])) ** 2 +
                               (float(edge1[index][2]) - float(edge2[length-index-1][2])) ** 2)
    distance = int(distance)
    return round(distance, 2)


def combine(col, row, pieces, out_path):
    long_pieces = []
    idx = 0
    for i in range(int(row)):
        for j in range(int(col)-1):
            long_piece = np.hstack((pieces[idx], pieces[idx+1]))
            long_pieces.append(long_piece)
            idx = idx + 1
        idx = idx + 1

    final_piece = None

    for j in range(int(col)):
        if final_piece is None:
            final_piece = long_pieces[j]
        else:
            final_piece = np.vstack((final_piece, long_pieces[j]))

    cv2.imwrite(os.path.join(out_path, 'final.jpg'), cv2.cvtColor(final_piece, cv2.COLOR_RGB2BGR))


if __name__ == '__main__':
    in_path = sys.argv[1]
    col_num = sys.argv[2]
    row_num = sys.argv[3]
    out_path = sys.argv[4]
    pieces = paste_img(in_path)
    combine(col_num, row_num, pieces, out_path)