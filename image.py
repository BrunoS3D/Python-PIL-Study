from PIL import Image, ImageDraw, ImageColor

print('=== START ===')

def open_image(path):
    newImage = Image.open(path)
    return newImage

def save_image(image, path):
    image.save(path, 'png')

def create_image(width, height):
    image = Image.new("RGB", (width, height), "white")
    return image

def get_pixel(image, x, y):
    width, height = image.size
    if x >= width:
        x = width - 1
    if y >= height:
        y = height - 1

    pixel = image.getpixel((x, y))
    return pixel


def apply_blur_filter(image, grid_size = 3):
    width, height = image.size

    new = create_image(width, height)
    pixels = new.load()

    for x in range(width):
        for y in range(height):
            pixel_grid = []
            for i in range(grid_size):
                for j in range(grid_size):
                    pixel_grid.append(get_pixel(image, x + i, y + j))
            
            red = 0
            green = 0
            blue = 0

            for pixel in pixel_grid:
                red += pixel[0]
                green += pixel[1]
                blue += pixel[2]

            grid_length = pixel_grid.__len__()

            red /= grid_length
            green /= grid_length
            blue /= grid_length

            color = (int(red), int(green), int(blue))

            for i in range(grid_size):
                for j in range(grid_size):
                    p1 = x + i
                    p2 = y + j

                    if p1 >= width:
                        p1 = width - 1
                    if p2 >= height:
                        p2 = height - 1

                    pixels[p1, p2] = color
            
    
    return new


def apply_pixel_filter(image, grid_size = 3):
    width, height = image.size

    new = create_image(width, height)
    pixels = new.load()

    grid_length = grid_size * grid_size

    for x in range(0, width, grid_size):
        for y in range(0, height, grid_size):
            pixel_grid = []
            for i in range(grid_size):
                for j in range(grid_size):
                    pixel_grid.append(get_pixel(image, x + i, y + j))
            
            red = 0
            green = 0
            blue = 0

            for pixel in pixel_grid:
                red += pixel[0]
                green += pixel[1]
                blue += pixel[2]

            red /= grid_length
            green /= grid_length
            blue /= grid_length
            # grayscale = (red + green + blue) / 3
            
            color = (int(red), int(green), int(blue))
            # color = (int(grayscale), int(grayscale), int(grayscale))

            for i in range(grid_size):
                for j in range(grid_size):
                    p1 = x + i
                    p2 = y + j

                    if p1 >= width:
                        p1 = width - 1
                    if p2 >= height:
                        p2 = height - 1

                    pixels[p1, p2] = color
            
    
    return new


def apply_hog_filter(image, grid_size = 3):
    width, height = image.size

    new = create_image(width, height)
    pixels = new.load()

    for x in range(0, width, grid_size):
        for y in range(0, height, grid_size):
            p1 = 0
            p2 = 0
            max_grayscale = 0
            for i in range(grid_size):
                for j in range(grid_size):
                    pixel = get_pixel(image, x + i, y + j)

                    grayscale = pixel[0]
                    grayscale += pixel[1]
                    grayscale += pixel[2]
                    grayscale /= 3

                    if grayscale > max_grayscale:
                        p1 = x + i
                        p2 = y + j

                        if p1 >= width:
                            p1 = width - 1
                        if p2 >= height:
                            p2 = height - 1
                        max_grayscale = grayscale

            color = (int(grayscale), int(grayscale), int(grayscale))
            pixels[p1, p2] = color

            for i in range(grid_size):
                for j in range(grid_size):
                    p3 = x + i
                    p4 = y + j

                    if p3 >= width:
                        p3 = width - 1
                    if p4 >= height:
                        p4 = height - 1

                    pixels[p3, p4] = color

    return new


def apply_negative_filter(image):
    width, height = image.size

    new = create_image(width, height)
    pixels = new.load()

    for x in range(width):
        for y in range(height):
            pixel = get_pixel(image, x, y)

            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]

            color = (255 - int(red), 255 - int(green), 255 - int(blue))
            pixels[x, y] = color

    return new


src_image = open_image('./image.png')

print('Escolha um dos filtros a seguir:')
print('1 - Blur (exige mais performance)')
print('2 - Pixelize')
print('3 - HOG Pixelize')
print('4 - Negative')

filter = input('Digite o numero do filtro (Blur): ')


def get_intensity():
    return int(input('Digite o valor de intensidade do filtro (3): ') or 3)

if '2' in filter:
    result_image = apply_pixel_filter(src_image, get_intensity())
elif '3' in filter:
    result_image = apply_hog_filter(src_image, get_intensity())
elif '4' in filter:
    result_image = apply_negative_filter(src_image)
else:
    result_image = apply_blur_filter(src_image, get_intensity())

save_image(result_image, './output.png')

print('=== EXIT  ===')
input('Pressione ENTER para sair...')