import cv2
from pyzbar import pyzbar
import csv

# 然后我们设置一个变量，来存放我们扫到的码的信息，我们每次扫描一遍都会要检测扫描到的码是不是之前扫描到的，
# 如果没有就存放到这里。接着我们调用opencv的方法来实例化一个摄像头，
# 最后我们设置一些我们存放码信息的表格的路径。
found = set()
# 打开摄像头，0代表本地摄像头
capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
# 存放数据的表格
PATH = "test.csv"
# 不停的用摄像头来采集条码，
while capture.isOpened():
    # 首先我们要用刚才实例化的摄像头来采集实时的照片，
    ret, frame = capture.read()
    # 用pyzbar的函数解析图像里的二维码和条形码
    test = pyzbar.decode(frame)

    # 循环检测到的条形码
    for tests in test:
        # 获取到的条形码数据转换成字符串
        testdate = tests.data.decode('utf-8')
        # 获取条形码类型
        testtype = tests.type

        # 绘出图像上条形码的数据和条形码类型
        printout = "{} ({})".format(testdate, testtype)

        if testdate not in found:
            # 向终端打印条形码数据和条形码类型
            print("[INFO] Found {} barcode: {}".format(testtype, testdate))
            print(printout)
        # 存放扫描数据
        if testdate not in found:
            with open(PATH, 'a+',encoding='utf-8') as f:
                # a+ 以附加方式打开可读写的文件。若文件不存在，则会建立该文件，如果文件存在，写入的数据会被加到文件尾后，即文件原先的内容会被保留。
                csv_write = csv.writer(f)
                date = [testdate]
                csv_write.writerow(date)
            found.add(testdate)
    #显示预览窗口
    cv2.imshow('Scanning', frame)
    #按q退出
    if cv2.waitKey(1) == ord('q'):
        break

#释放摄像头
capture.release()
#释放所有显示窗口
cv2.destroyAllWindows()