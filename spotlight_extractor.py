## Spotlight Extractor: Automaticlly save Win 10 Spotlight Wallpapers
## 自动转存win10锁屏壁纸

import os
from shutil import copyfile
import numpy as np
from matplotlib import pyplot as plt
from datetime import date


def obtain_key_px(img_data):
    '''Obtian pixel data that can distinguishe an image.'''
    first, last = img_data[0], img_data[-1]
    first, last = first[len(first)//5*4:], last[:len(last)//5]
    return np.concatenate((first, last))   # img_data[len(img_data)//2]


def get_px_dataset(new_path):
    '''Get key pixels data of images that are already saved in `new_path`.
       Return a list containing key pixels of every exising image.

           new_path: new saving location for the spotlight images.'''

    if 'img_ref.npz' not in os.listdir(new_path):
        print('>> Creating image references...')
        px_dataset = []

        for folder in ['desktop/', 'phone/', 'ignore/']:
            for img in os.listdir(new_path+folder):
                pixel_data = obtain_key_px(plt.imread(new_path+folder+img))
                px_dataset.append(pixel_data)

        with open(new_path+'img_ref.npz', 'wb') as f:
            np.savez(f, *px_dataset)

    else:
        with open(new_path+'img_ref.npz','rb') as f:
            px_dataset = np.load(f)
            px_dataset = [px_dataset[key] for key in px_dataset]

    return px_dataset


def move_img_file(img, new_path, folder):
    ''' Move an image file to a new path.

           img: the name of image file to be relocated.
           new_path: new saving location for the spotlight images.
           folder: name of the saving folder in `new_path`.'''

    os.rename(img, new_path+folder+'/'+img)
    print('>> .\\'+folder+'\\'+img)



def run_extractor(spotlight_path, new_path, check_duplicates=True):
    '''Main function.

           spotlight_path: location of the spotlight images.
           new_path: new saving location for the spotlight images.
           check_duplicates: if True, check duplicates before saving.'''

    for folder in ['desktop/', 'phone/', 'ignore/']:
        if not os.path.exists(new_path+folder):
            os.makedirs(new_path+folder)

    os.chdir(spotlight_path)

    start_saving = False

    if check_duplicates:
        print('>> Checking duplicates...')
        px_dataset = get_px_dataset(new_path)


    for num, img in enumerate(os.listdir()):
        flag = False
        img_data = plt.imread(img)

        if check_duplicates:
            new_key_px = obtain_key_px(img_data)

            for data in px_dataset:
                if np.array_equal(data, new_key_px):
                # if the two arrays have the same shape and elements
                    flag = True
                    break

        if not flag:
        # if not a duplicate image or if not checking duplicates
            
            if check_duplicates:
                # append the key pixels of the new image for later dup checks
                px_dataset.append(new_key_px)  

            if not start_saving:
                print('>> Saving...')
                start_saving = True


            # copy the image and rename it using current date and its number
            img_ = date.today().strftime('%Y%m%d')+'_'+str(num)+'.jpg'
            copyfile(img, img_)

            try:
                if img_data.shape[0] < img_data.shape[1]:
                    # horizontal image, normally with a shape of (1080, 1920, 3)
                    move_img_file(img_, new_path, 'desktop')

                else:                                  # vertical image
                    move_img_file(img_, new_path, 'phone')

            except:    
                print(f'Error while moving the image file {img_}...')
                os.remove(img_)

    if not start_saving:
        print('>> No new pics...')

    elif check_duplicates: 
        with open(new_path+'img_ref.npz', 'wb') as f:
            np.savez(f, *px_dataset)
        print('>> Image reference file updated.')



if __name__ == '__main__':
    
    new_path = r'/new_path/'
    spotlight_path = r'/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets/'
    run_extractor(spotlight_path, new_path, check_duplicates=True)
