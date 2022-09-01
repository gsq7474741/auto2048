import subprocess
import pathlib
from PIL import Image
import pytesseract

adb_path = pathlib.Path(r'D:\"Program Files"\MuMu\emulator\nemu\vmonitor\bin\adb_server.exe')
adb = str(adb_path) + ' '


def init_adb():
    r = subprocess.Popen(adb + 'kill-server', shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    prt_out(r)
    r2 = subprocess.Popen(adb + 'connect 127.0.0.1:7555', shell=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    prt_out(r2)


def prt_out(r):
    print(r.stdout.read().decode('gbk'))
    print(r.stderr.read().decode('gbk'))


def get_cap():
    cap_path = './caps/tmp.jpg'
    do_cap = subprocess.Popen(adb + 'shell screencap -p /storage/emulated/0/tmp.jpg', shell=True,
                              stdout=subprocess.PIPE)
    while True:
        if do_cap.stdout.readline() is not None:
            # prt_out(do_cap)
            break
    # time.sleep(1)
    do_pull = subprocess.Popen(adb + 'pull /storage/emulated/0/tmp.jpg ' + cap_path, shell=True, stdout=subprocess.PIPE)
    while True:
        if do_pull.stdout.readline() is not None:
            # prt_out(do_pull)
            break
    # time.sleep(1)
    img = Image.open(cap_path)
    return img


def get_mat(img):
    ox = 126
    oy = 139
    squ = 184 + 13
    wgap = 13
    boxes = []
    for i in range(5):
        for j in range(7):
            box = [ox + i * squ, oy + j * squ, ox + (i + 1) * squ, oy + (j + 1) * squ]
            boxes.append(box)

    crops = []
    for box in boxes:
        imc = img.crop(box)
        crops.append(imc)

    mat = []

    for c in crops:
        # r=c.ocr
        r = pytesseract.image_to_string(c, lang='eng')
        mat.append(r)

    return mat


if __name__ == '__main__':
    init_adb()
    img = get_cap()
    mat = get_mat(img)
    print(f'mat:{mat}')
# crops[6].show()
