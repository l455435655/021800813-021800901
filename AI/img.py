import os
import base64
from PIL import Image
from PIL import ImageChops


class Img:

    def __init__(self):
        self.__b64str = ''
        self.__path = ''
        self.__directory = ''
        self.__filename = ''

        # self.__sample_image_path = ''

        self.__status = ''
        self.__target_image_path = ''

        self.__sample_images = []
        root, dirs, files = list(os.walk(r'.\data\sample_img'))[0]
        for sample_image_path in [os.path.join(root, file) for file in files]:
            self.__sample_images.append(self.__cut_image(img=Image.open(sample_image_path)))

    def load(self, b64str: str, path: str):
        self.__b64str = b64str
        self.__path = path
        self.__directory, self.__filename = os.path.split(self.__path)
        self.__saveb64str2png()
        self.__image2status()

    def __saveb64str2png(self):
        # make directory
        if not os.path.exists(self.__directory):
            os.makedirs(self.__directory)
        # write to file
        with open(self.__path, 'wb') as file:
            file.write(base64.b64decode(self.__b64str))

    def __image2status(self):
        orign_image = self.__cut_image(img=Image.open(self.__path))
        for sample_image in self.__sample_images:
            status = self.__cmp_images(orign_image, sample_image)
            if status:
                self.__status = status
                return

    def __cmp_images(self, images: list, sample_images: list):
        blank_image = Image.open(r'.\data\white.png')
        status = ''
        for i in range(9):
            if ImageChops.difference(images[i], blank_image).getbbox() is None:
                status = status + '0'
            else:
                found = False
                for j in range(9):
                    if ImageChops.difference(images[i], sample_images[j]).getbbox() is None:
                        status = status + str(j + 1)
                        found = True
                        break
                if not found:
                    break

        if len(status) == 9:
            return status

    # cut image to 3 * 3 images
    def __cut_image(self, img) -> list:
        images = []
        width = img.size[0] // 3
        height = img.size[1] // 3
        for i in range(3):
            for j in range(3):
                left = j * width
                upper = i * height
                right = (j + 1) * width
                lower = (i + 1) * height
                img_c = img.crop(box=(left, upper, right, lower))
                images.append(img_c)
        return images


    def get_status(self) -> str:
        return self.__status
