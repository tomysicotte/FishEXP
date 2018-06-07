from PIL import Image
import numpy as np
import os

diff = ["3 - Tail\\"]
other_diff = ["1 - Bouche\\","2 - Nageoire Lat\\", "3 - Tail\\", "4 - Fin\\"]
cat = ["K\\", "L\\"]
path = "C:\\Users\\tsico\\Fish\\Hardest - 1 feature\\"
beg_old_folder = "Group "
new_folder = "Resized"
for ending in diff :
    for c in cat :
        my_img = os.listdir(path+beg_old_folder+ending+c)
        for n_img, this_img in enumerate(my_img):
            print(n_img)
            for i_angle in range(24):
                if n_img == 0 :
                        os.makedirs(path + new_folder +ending[4:] + str((i_angle + 1) * 15 - 10) + "\\" + c)

                im = Image.open(path+beg_old_folder+ending+c+this_img)
                pixels = np.asarray(im)
                new_im = []
                for row in pixels:
                    y = []
                    for col in row:
                        x = []
                        for i in range(3):
                            x.append(col[i])
                        y.append(x)
                    new_im.append(y)
                new_new_im = []
                av = []
                ap = []
                for y in range(100):
                    new_im[0].append(new_im[0][0])
                    av.append(new_im[0][0])
                for y in range(100):
                    new_im[0].append(new_im[0][0])
                    ap.append(new_im[0][0])
                for i in range(150):
                    new_new_im.append(new_im[0])
                for i, row in enumerate(new_im):
                    if i == 0:
                        new_new_im.append(row)
                    else:
                        new_new_im.append(av + row + ap)
                for i in range(150):
                    new_new_im.append(new_im[0])

                arrayimg = np.asarray(new_new_im)
                img = Image.fromarray(arrayimg, 'RGB')
                new = img.rotate((i_angle + 1) * 15 - 10)
                pixels = np.asarray(new)
                new_im = []
                for row in pixels:
                    y = []
                    for col in row:
                        x = []
                        for i in range(3):
                            x.append(col[i])
                        y.append(x)
                    new_im.append(y)

                good_img = []
                for i, row in enumerate(new_im):
                    if i > 99 and i < 460:
                        good_img.append(row[100:460])
                arrayimg = np.asarray(good_img)
                img = Image.fromarray(arrayimg, 'RGB')

                img.save(path + new_folder +ending[4:] + str((i_angle + 1) * 15 - 10) + "\\" + c+this_img)