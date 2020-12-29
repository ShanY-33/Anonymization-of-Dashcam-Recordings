from . import convert_coordinate


def merge_boxes(img_height, img_width, boxes, threshold=0.1):
    '''
    merge bound boxes
    Args:
        locs-->list: [[x_min1,y_min1,x_max2,y_max2],...,[x_min1,y_min1,x_max2,y_max2]]
        w: the width of the image
        h: the height of the image
        thre: threshold for judging if two bound box is near enough
    '''

    locs = convert_coordinate.rel_to_abs(img_height, img_width, boxes).tolist()

    # #1: person; 3: car; 4: motorcycle; 6: bus; 8: truck
    # detection_classes = (1, 3, 4, 6, 8)
    # for i in range(boxes.shape[0]):
    #     if (output_dict['detection_classes'][i] in detection_classes 
    #          and output_dict['detection_scores'][i] > threshold): 
    #          locs.append(boxes[i])

    # print(locs)

    flag = False
    while not flag:
        if_modify = False
        locs_num = len(locs)
        for i in range(len(locs)-1):
            x_min, y_min, x_max, y_max = locs[i]
            for j in range(i+1, len(locs)):
                # if i == j:
                #     continue
                x_min2, y_min2, x_max2, y_max2 = locs[j]
                # if (not is_small_box(locs[i], img_width,img_height)) & (not is_small_box(locs[j], img_width,img_height)):
                #     continue

                # same
                if __is_almost_same_box(img_height, img_width, locs[i], locs[j]):
                    locs[i] = [min(x_min, x_min2), min(y_min, y_min2),max(x_max, x_max2),max(y_max, y_max2)]
                    del locs[j]
                    if_modify = True
                    break

                # near
                if __is_near(img_height, img_width, locs[i], locs[j]):
                        locs[i] = [min(x_min, x_min2),min(y_min, y_min2),max(x_max, x_max2),max(y_max, y_max2)]
                        del locs[j]
                        if_modify = True
                        break

                # include
                if __is_included(img_height, img_width, locs[i], locs[j]):
                    locs[i] = [min(x_min, x_min2), min(y_min, y_min2), max(x_max, x_max2), max(y_max, y_max2)]
                    del locs[j]
                    if_modify = True
                    break

            if if_modify:
                break
        if not if_modify:
            flag = True

    return locs


def __is_almost_same_box(img_height, img_width, box1, box2, threshold=0.01):
    x_min, y_min, x_max, y_max = box1
    x_min2, y_min2, x_max2, y_max2 = box2
    if ((abs(x_min-x_min2) < threshold * img_width) and
       (abs(x_max-x_max2) < threshold * img_width) and
       (abs(y_max-y_max2) < threshold*img_height) and
       (abs(y_min-y_min2) < threshold*img_height)):
        return True
    return False


def __is_near(img_height, img_width, box1, box2, threshold=0.01):
    x_min, y_min, x_max, y_max = box1
    x_min2, y_min2, x_max2, y_max2 = box2
    if ((__is_small_box(img_height, img_width, box1)) or
       (__is_small_box(img_height, img_width, box2))):
        y_near = abs((y_min+y_max)/2-(y_min2+y_max2)/2) < threshold * img_height + (y_max-y_min)/2+(y_max2-y_min2)/2
        x_near = abs((x_min+x_max)/2-(x_min2+x_max2)/2) < threshold * img_width + (x_max-x_min)/2+(x_max2-x_min2)/2
        if y_near & x_near:
            return True
    return False


def __is_small_box(img_height, img_width, box, threshold=0.1):
    return ((box[3]-box[1]) < threshold*img_height) & ((box[2]-box[0]) < threshold*img_width)


def __is_included(img_height, img_width, box1, box2, extend=0.1):
    x_min, y_min, x_max, y_max = box1
    x_min2, y_min2, x_max2, y_max2 = box2
    if((x_min < x_min2 + extend * img_width and y_min < y_min2+extend*img_height and x_max > x_max2 - extend * img_width and y_max > y_max2-extend*img_height) or
       (x_min > x_min2 - extend * img_width and y_min > y_min2-extend*img_height and x_max < x_max2 + extend * img_width and y_max < y_max2 + extend * img_height)):
        return True
    return False

