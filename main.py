import io
from PIL import Image
import mss

def print_hi(name):
    print(f'Hi, {name}')
    with mss.mss() as sct:
        # Capture the screen
        screenshot = sct.grab(sct.monitors[1])
        img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)

        byte_arr = io.BytesIO()
        img.save(byte_arr, format='JPEG')
        img_bytes = byte_arr.getvalue()
        size = len(img_bytes)

        print(size)

if __name__ == '__main__':
    print_hi('PyCharm')
