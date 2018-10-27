import cv2
import numpy as np
from matplotlib import pyplot as plt

cover = cv2.imread('MonaLisa.png')
secret = cv2.imread('dbz.png')


# encode secret image into cover image
def LSB_encode(cover_img, secret_img, bits):
    # the return variable
    stego = np.zeros(secret_img.shape, dtype=np.uint8)
    for color in range(0, 3):
        # extract the color channels
        cover_color = cover_img[:, :, color]
        secret_color = secret_img[:, :, color]
        stego_color = stego[:, :, color]

        # for each pixel extract host and secret bits to form stego pixel. Then store in color channel
        for height in range(0,cover_color.shape[0]):
            for width in range(0, cover_color.shape[1]):
                # turn the int pixel value into binary and truncated desired of bits
                host_px = np.binary_repr(cover_color[height, width], width=8)[:-bits]
                secret_px = np.binary_repr(secret_color[height, width], width=8)[:bits]
                stego_px = host_px+secret_px
                stego_color[height, width] = np.packbits(np.array(list(stego_px), dtype=np.uint8))[0]
        # store each color channel in return variable
        stego[:, :, color] = stego_color
    return stego

# recover image from stego img
def LSB_decode(stego_img, bits):
    # return variable
    extract_img = np.zeros(stego_img.shape, dtype=np.uint8)
    for color in range(0,3):
        # pull out the color channels
        stego_color = stego_img[:, :, color]
        extract_color = extract_img[:, :, color]
        # for each pixel, pull out the secret pixel and pad to the right since the have less impact
        # store the extracted pixel into the color channel
        for height in range(0, stego_img.shape[0]):
            for width in range(0, stego_img.shape[1]):
                secret_px = np.binary_repr(stego_color[height, width], width=8)[-bits:]
                padded_px = secret_px + '0'*(8-bits)
                extract_px = np.packbits(np.array(list(padded_px), dtype=np.uint8))[0]
                extract_color[height, width] = extract_px
        # store color channel into return image
        extract_img[:, :, color] = extract_color
    return extract_img


# show how the image encodes and decodes from using 1 to 7 bits
def from_1_to_7_bits(cover_im, secret_im):
    # for creating the image
    f, axarr = plt.subplots(4, 4)
    for x in range(1,8):
        stego_text = LSB_encode(cover_im, secret_im, x)
        extracted_text = LSB_decode(stego_text, x)
        x_cord = (x-1) % 4
        y_cord = 0
        if x < 5:
            y_cord = 1
        else:
            y_cord = 3
        axarr[x_cord, y_cord-1].imshow(cv2.cvtColor(stego_text, cv2.COLOR_BGR2RGB))
        axarr[x_cord, y_cord-1].set_title("stego, bits=" + str(x))
        axarr[x_cord, y_cord - 1].axis('off')
        axarr[x_cord, y_cord].imshow(cv2.cvtColor(extracted_text, cv2.COLOR_BGR2RGB))
        axarr[x_cord, y_cord].set_title("extract, bits=" + str(x))
        axarr[x_cord, y_cord].axis('off')

# shows why the image fails at decoding a resize stegotext (bilinear interpolation in the resize fn)
def why_this_fails_at_resizing(cover_im, secret_im ):
    stego_text = LSB_encode(cover_im, secret_im, 1)
    stego_text = cv2.resize(stego_text, (stego_text.shape[1]+2, stego_text.shape[0]+2))
    extracted_text = LSB_decode(stego_text, 1)
    plt.imshow(cv2.cvtColor(extracted_text, cv2.COLOR_BGR2RGB))
    plt.title("Decoding stegotext after it been resized by two pixels in both axises")
    plt.show()


from_1_to_7_bits(cover, secret)
why_this_fails_at_resizing(cover, secret)