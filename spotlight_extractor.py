## Spotlight Extractor: Automaticlly save Win 10 Spotlight Wallpapers
## 自动转存win10锁屏壁纸

import os
from shutil import copyfile
import numpy as np
from matplotlib import pyplot as plt
from datetime import date


def define_key_pixels(img_data):
    '''Define and return the key pixels that distinguishes an image.'''
    return np.concatenate((img_data[0], img_data[-1]))


def get_key_px_dataset(new_path):
    '''Get key data of images that are already saved in `new_path`.
       Return a list containing key pixels of every exising image.

           new_path: new saving location for the spotlight images.'''

    key_px_dataset = []
    for folder in ['desktop/', 'phone/', 'ignore/']:
        new_path_ = new_path+folder
        for img in os.listdir(new_path_):
            img_data = plt.imread(new_path_+img)
            key_px_dataset.append(define_key_pixels(img_data))

    return key_px_dataset


def move_img_files(img, folder, new_path):
    ''' Move an image file from the current directory to `new_path`.

           img: the image file to be relocated.
           new_path: new saving location for the spotlight images.
           folder: name of the saving folder.'''

    os.rename(img, new_path+folder+'/'+img)
    print('>> .\\'+folder+'\\'+img)



def run_extractor(spotlight_path, new_path, check_duplicates=True):
    '''Main function.

           spotlight_path: location of the spotlight images.
           new_path: new saving location for the spotlight images.
           check_duplicates: if True, check duplicates before saving.'''

    start_saving = False

    if check_duplicates:
        print('>> Checking duplicates...')
        key_px_dataset = get_key_px_dataset(new_path)

    os.chdir(spotlight_path)

    for num, img in enumerate(os.listdir()):
        flag = False
        img_data = plt.imread(img)

        if check_duplicates:
            new_key_pixels = define_key_pixels(img_data)

            for data in key_px_dataset:
                if data.shape == new_key_pixels.shape and (new_key_pixels == data).all:
                    flag = True
                    break

        if not flag:
            if not start_saving:
                print('>> Saving...')
                start_saving = True
            
            img_ = date.today().strftime('%Y%m%d')+'_'+str(num)+'.jpg'
            copyfile(img, img_)

            try:
                if img_data.shape == (1080, 1920, 3):
                    move_img_files(img_, 'desktop', new_path)

                else:
                    move_img_files(img_, 'phone', new_path)

            except:
                os.remove(img_)


    if not start_saving:
        print('>> No new pics...')



if __name__ == '__main__':
    
    new_path = r'/new_path/'
    spotlight_path = r'/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets'
    run_extractor(spotlight_path, new_path, check_duplicates=True)
