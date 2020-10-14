from PIL import Image


path = './data/image/'



def cut_image(path, image) -> list:
    images = []
    width = image.size[0] // 3
    height = image.size[1] // 3
    for i in range(3):
        for j in range(3):
            left = j * width
            upper = i * height
            right = (j + 1) * width
            lower = (i + 1) * height
            img_c = image.crop(box=(left, upper, right, lower))
            images.append(img_c)
            img_c.save(path[:-4] + str(i+1) + str(j+1) + '.jpg')
    return images
for i in range(1, 10):
    file_path = path + str(i) + '.jpg'
    orign_image = Image.open(file_path)
    images_after_cut = cut_image(path=file_path, image=orign_image)
# for image_after_cut in images_after_cut:
#     image_after_cut.sa
