def get_captcha(driver, url):
    driver.implicitly_wait(10)
    driver.get(url)
    img = driver.find_element_by_id('imgCode')

    img.screenshot('./captcha.png')  
    
def recognize_captcha():
    
    image = Image.open('./captcha.png')
    image = image.convert('L') # greyscale
    image_data = image.load()
    w,h = image.size
    for x in range(w):
        for y in range(h):
            if image_data[x, y]<120:
                image_data[x, y] = 0
            else:
                image_data[x, y]=255
#     image.show()
    code = pytesseract.image_to_string(image)
    return code


def captcha_helper(driver, url):
    get_captcha(driver, url)
    code = recognize_captcha()
    driver.find_element_by_id('code').send_keys(code)
    

if __name__ == '__main__':
    driver_path = r' '
    driver = webdriver.Chrome(executable_path=driver_path)
    url = 'https://so.gushiwen.org/user/login.aspx?from=http://so.gushiwen.org/user/collect.aspx'
    
    captcha_helper(driver, url)
