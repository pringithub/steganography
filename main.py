
# TODO add functionality for more than 256 bytes to be encoded (need to change "packet")

import numpy as np
import cv2

import argparse
# Create the parser
my_parser = argparse.ArgumentParser(description='Get a cleartext string')
# Add the arguments
my_parser.add_argument('cleartext',
                       type=str,
                       help='cleartext to encode')
# Execute the parse_args() method
args = my_parser.parse_args()
phrase = args.cleartext


#phrase = 'one small step for man, one giant leap for mankind'
phrase_len = len(phrase)
phrase_len_byte = chr(phrase_len)
phrase = phrase_len_byte+phrase
phrase = np.frombuffer(phrase, dtype=np.uint8)


img = cv2.imread('cat.jpeg')

num_bits_phrase = len(phrase)*8
num_bytes_image = img.shape[0]*img.shape[1]*img.shape[2]
print( 'Total num of bits: '+str(num_bits_phrase) )
print( 'Total num of bytes in which to place: '+str(num_bytes_image) )


def encode(img, phrase):

    # extract bits from phrase 
    bits = []
    for char in phrase:
        for i in range(8): # bit length
            y = ((1<<i) & char) >> i
            bits.append(y)

    # replace lsbs with bits
    it = 0
    num_bytes_image = img.shape[0]*img.shape[1]*img.shape[2]
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(img.shape[2]): 
                if it == num_bits_phrase:
                    break

                x = 1 & img[i][j][k]
                y = bits[it]
                img[i][j][k] = x ^ (x^y)
		assert(y == img[i][j][k])

	        it += 1

    cv2.imwrite('cat_encoded.jpeg', img) 

    return img

def decode(img):

    # extract bits from image
    bits = []
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(img.shape[2]): 

                x = 1 & img[i][j][k]
		bits.append(x)

    # create chars from bits
    char = 0b0
    for j in range(8):
        char += bits[j] << j
    num_chars = char
    print(num_chars)

    phrase = '' 
    for i in range(8, num_chars*8+8, 8):
        char = 0b0
	#print(bits[i:i+8])
        for j in range(8):
            char += bits[i+j] << j
	#print(chr(char))
        phrase += chr(char)
 
    return phrase


img    = encode(img, phrase)
phrase_decoded = decode(img)
print(phrase_decoded)



