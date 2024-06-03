from PIL import Image
import bitarray as ba


def modify_bit(b, v):
    return (b & ~1) | v


# Hide a bitstring in an image by changing the least significant bit of each byte
def hide(message: str, image: str, outName: str):
    hideBytes = message.encode('utf-8')
    allBits = list(iter_bits(hideBytes))
    with Image.open(image) as im:
        im_bytes = im.tobytes()

        if len(allBits) > len(im_bytes):
            raise ValueError("Message too long")

        new_im_bytes = bytearray(len(im_bytes))
        for i, b in enumerate(im_bytes):
            if len(allBits) != 0:
                new_im_bytes[i] = modify_bit(b, allBits[0])  # Modify the bit
                allBits.pop(0)
            else:
                new_im_bytes[i] = b

        new_im = Image.frombytes('RGB', im.size, new_im_bytes)
        # new_im.show()
        new_im.save(outName)

    return new_im_bytes


def decode_image(image: str = None):
    decodedBits = []
    with Image.open(image) as im:
        im_bytes = bytearray(im.tobytes())

        for i, b in enumerate(im_bytes):
            decodedBits.append(bool(b & 1))

    bs = ba.bitarray(decodedBits).tobytes()
    return bs.split(b"\0")[0].decode('utf-8', errors='ignore')


def example():
    with Image.open("grayson.jpg") as im:
        im_bytes = im.tobytes()  # Convert image to raw bytes

        print(len(im_bytes) / 3)  # Length of im_bytes should be divisible by 3.

        new_im_bytes = bytearray(len(im_bytes))  # Make a byte array to store my modified data
        for i, b in enumerate(im_bytes):
            new_im_bytes[i] = b ^ 0b10010110

        new_im = Image.frombytes('RGB', im.size, new_im_bytes)  # Make a new image
        new_im.show()  # Let's see what we did!

        for bit in iter_bits(bytes([0b00001111, 0b11110000])):
            print(bit)


def main():
    #msg = 'A news release from the Charleston County Coroner’s Office said John Barnett, 62, died on March 9, from “what appears to be a self-inflicted gunshot wound.” The city’s police department says detectives are investigating the case and “awaiting the formal cause of death, along with any additional findings that might shed further light on the circumstances surrounding the death of Mr. Barnett.”\0'
    #hide(msg, "despair.jpg", "hiddenMessage.png")
    print(decode_image("hiddenMessage.png"))


# Return one bit at a time from a bytes or bytearray
def iter_bits(inbytes):
    for b in inbytes:
        for i in range(8):
            yield b >> (7 - i) & 1


if __name__ == '__main__':
    main()
