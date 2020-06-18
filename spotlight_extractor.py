## Spotlight Extractor: Automaticlly save Win 10 Spotlight Wallpapers
## 自动转存win10锁屏壁纸

class spotlightExtractor:

    def __init__(self, spotlight_path, new_path, check_duplicates=True):
        ''' spotlight_path: location of the spotlight images.
            new_path: new saving location for the spotlight images.
            check_duplicates: if True, check duplicates before saving.'''

        self.spotlight_path = spotlight_path
        self.new_path = new_path
        self.check_duplicates = check_duplicates

        self.run_extractor()


    def obtain_key_px(self, img_data):
        '''Obtian pixel data that can distinguishe an image.'''
        first, last = img_data[0], img_data[-1]
        first, last = first[len(first)//5*4:], last[:len(last)//5]
        return np.concatenate((first, last))   # img_data[len(img_data)//2]


    def get_px_dataset(self):
        '''Get key pixels data of images that are already saved in `new_path`.
           Return a list containing key pixels of every exising image.'''

        if 'img_ref.npz' not in os.listdir(self.new_path):
            print('>> Creating image references...')
            px_dataset = []

            for folder in ['desktop/', 'phone/', 'ignore/']:
                for img in os.listdir(self.new_path+folder):
                    pixel_data = self.obtain_key_px(plt.imread(self.new_path+folder+img))
                    px_dataset.append(pixel_data)

            with open(self.new_path+'img_ref.npz', 'wb') as f:
                np.savez(f, *px_dataset)

        else:
            with open(self.new_path+'img_ref.npz','rb') as f:
                px_dataset = np.load(f)
                px_dataset = [px_dataset[key] for key in px_dataset]

        return px_dataset


    def move_img_file(self, img, folder):
        ''' Move an image file to a new path.

               img: the name of image file to be relocated.
               folder: name of the saving folder in `new_path`.'''

        os.rename(img, self.new_path+folder+'/'+img)
        print('>> .\\'+folder+'\\'+img)


    def find_new_images(self):
        '''Check if there are new pictures in the spotlight folder
           since the last time the program was run.'''

        try:
            push_date = datetime.fromtimestamp(os.path.getmtime(self.spotlight_path)).date()
            parse_date = datetime.fromtimestamp(os.path.getmtime(self.new_path+'img_ref.npz')).date()
            return (push_date != parse_date)
        except:
            return True


    def run_extractor(self):
        '''Main Function.'''

        if not self.find_new_images():
            return print('>> No new pics...')

        for folder in ['desktop/', 'phone/', 'ignore/']:
            if not os.path.exists(self.new_path+folder):
                os.makedirs(self.new_path+folder)

        os.chdir(self.spotlight_path)

        start_saving = False

        if self.check_duplicates:
            print('>> Checking duplicates...')
            px_dataset = self.get_px_dataset()


        for num, img in enumerate(os.listdir()):
            dup = False
            img_data = plt.imread(img)

            if self.check_duplicates:
                new_key_px = self.obtain_key_px(img_data)

                for data in px_dataset:
                    if np.array_equal(data, new_key_px):
                    # if the two arrays have the same shape and elements
                        dup = True
                        break

            if not dup:
            # if not a duplicate image or if not checking duplicates
                
                if self.check_duplicates:
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
                        self.move_img_file(img_, 'desktop')

                    else:                                  # vertical image
                        self.move_img_file(img_, 'phone')

                except:    
                    print(f'Error while moving the image file {img_}...')
                    os.remove(img_)

        if not start_saving:
            print('>> No new pics...')

        elif self.check_duplicates: 
            with open(self.new_path+'img_ref.npz', 'wb') as f:
                np.savez(f, *px_dataset)
            print('>> Image reference file updated.')



if __name__ == '__main__':
    
    new_path = r'/new_path/'
    spotlight_path = r'/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets/'
    spotlightExtractor(spotlight_path, new_path, check_duplicates=True)
