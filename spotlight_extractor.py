import os
from shutil import copyfile
from matplotlib import pyplot as plt
from datetime import date


os.chdir(r'/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets')

new_path = r'/new_path/'

print('saving...')
for num, img in enumerate(os.listdir()):
    img_ = date.today().strftime('%Y%m%d')+'_'+str(num)+'.jpg'
    copyfile(img, img_)

    try:
        if plt.imread(img_).shape == (1080, 1920, 3):
            os.rename(img_, new_path+'desktop/'+img_)
            print('.\\desktop\\'+img_)
        else:
            os.rename(img_, new_path+'phone/'+img_)
            print('.\\phone\\'+img_)

    except:
        os.remove(img_)


