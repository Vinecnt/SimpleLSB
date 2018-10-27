# SimpleLSB
Simple Least Significant Bit Encoder and Decoder

According to https://en.wikipedia.org/wiki/Bit_numbering#Least_significant_bit_in_digital_steganography,

You can store information (secret text) into a target file (cover text) using the least signficant bits of the covertext and replacing
it with the most significant bits of the secret text. 


# Improvements
- [ ] Utilize numpy array functions. Currently iterating through all elements. Is there a way to perform a function on all elements and return the a result into an array of the same size. map? np.vectorize()?
- [ ] This simple LSB isn't resistant to noise. How to decode information from a bilinear interpolated image. "Simplest" way would be to invert cv2 resize fuction. But with if the resize shape wasn't known? Brute force?
