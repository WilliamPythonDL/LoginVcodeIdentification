# coding=utf-8

import os
from urllib import request

# 保存验证码文件扩展名
EXTENSION = ".txt"

# tesseract 引擎的安装路径
TESSERACT_PATH = r""

class Ocr:
    def __init__(
        self,
        tesseract_path=TESSERACT_PATH,
        *,
        out_path=None,
        mode=3,
        delete=True
    ):
        """
        :param tesseract_path: tesseract 引擎的安装路径
        :param out_path: 输出文件路径
        :param mode: 图片的切割模式
        :param delete: 是否保留生成的文本文件
        """

        """
        Page segmentation modes:
          0    Orientation and script detection (OSD) only.
          1    Automatic page segmentation with OSD.
          2    Automatic page segmentation, but no OSD, or OCR.
          3    Fully automatic page segmentation, but no OSD. (Default)
          4    Assume a single column of text of variable sizes.
          5    Assume a single uniform block of vertically aligned text.
          6    Assume a single uniform block of text.
          7    Treat the image as a single text line.
          8    Treat the image as a single word.
          9    Treat the image as a single word in a circle.
         10    Treat the image as a single character.
         11    Sparse text. Find as much text as possible in no particular order.
         12    Sparse text with OSD.
         13    Raw line. Treat the image as a single text line,
               bypassing hacks that are Tesseract-specific.
        """

        self._tesseract_path = tesseract_path
        self._outpath = out_path
        self._mode = mode
        self._delete = delete

    def exec(self, *, img_path="", img_url=None):
        """
        执行命令
        :param img_path: 本地图片路径
        :param img_url: 网络图片地址
        """
        save_img = ""
        if img_path:
            save_img = img_path
        else:
            if img_url:
                # 以网络图片的文件名和后缀名的形式保存
                save_img = img_url.split('/')[-1]
                # 在当前绝对路径下保存图片文件
                save_img=self._outpath + save_img
            try:
                #使用urllib.request.urlretrieve()将网页保存到本地
                # urllib.request.urlretrieve (url, filename=None, reporthook=None, data=None )
                request.urlretrieve(img_url, save_img)
            except Exception as e:
                print(e)
        # 如何指定路径存在文件扩展名，将去除扩展名
        if self._outpath.endswith(EXTENSION):
            self._outpath = self._outpath[:-4]
        # 如何指定模式不在范围内，将指定为self._mode=3
        if self._mode > 13 or self._mode < 0:
            self._mode = 3

        # 在当前目录的路径下，以网络图片的文件名的形式保存
        if img_url:
            path_img = save_img.split('\\')[-1]
            path_img = path_img.split('.')[0]
            self._outpath = self._outpath + path_img
        # 在当前目录的路径下，以本地图片的文件名的形式保存
        elif img_path:
            path_img = img_path.split('\\')[-1]
            path_img = path_img.split('.')[0]
            self._outpath = self._outpath + path_img
        # print(save_img, self._outpath, self._mode)
        os.chdir(self._tesseract_path)
        cmd = "tesseract.exe {save_img} {out} --psm {mode}".format(
            save_img=save_img, out=self._outpath, mode=self._mode
        )
        os.system(cmd)
        
        try:
            ## 读取保存验证码的文件并且返回结果
            txt_file = self._outpath + EXTENSION
            with open(txt_file, "r", encoding="utf-8") as f:
                ocr_text = f.read().strip()
        except IOError:
            print("无法找到该文件!")

        
        ##删除网络上验证码相关文件
        if img_url:
            if self._delete:
                ##删除保存验证码的文件
                if os.path.exists(txt_file):
                    os.remove(txt_file)
                ##删除保存验证码的图片
                if os.path.exists(save_img):
                    os.remove(save_img)
                ##删除网络上验证码相关文件
        elif img_path:
            if self._delete:
                ##删除保存验证码的文件
                if os.path.exists(txt_file):
                    os.remove(txt_file)
                # ##删除保存验证码的图片
                # if os.path.exists(save_img):
                #     os.remove(save_img)
        return ocr_text



if __name__ == "__main__":
    # 识别本地照片
    img_path = ""

    # 识别网络照片
    img_url = ""

    # 指定文件输出路径
    out_path=""

    # 如何没有指定路径，将使用默认路径
    if out_path =="":
        ## 使用当前文件路径作为 out_path
        cmd = "cd"
        ## os.popen(cmd)会把执行的cmd的输出作为值返回
        content=os.popen(cmd).read().strip()
        # 获取当前目录的绝对路径
        out_path=content +'\\'
        ocr = Ocr(out_path=out_path)
    else:
        ocr = Ocr(out_path=out_path)

    # 识别本地照片
    if img_path:
        # 识别本地照片
        result = ocr.exec(img_path=img_path)
        print(result)

    # 识别网络照片
    elif img_url:    
        # 识别网络图片
        result = ocr.exec(img_url=img_url)
        print(result)
    else:
        print("请输入本地照片路径“img_path”或者识别网络图片路径img_url")


    # ## mode参数遍历，直到返回结果
    # # ## 本地图片
    if result =="" and img_path !="":
        for mode in range(6, 13, 1):
            ocr = Ocr(out_path= out_path, mode=mode)
            result = ocr.exec(img_path=img_path)
            print(result)
            if result !="":
                break

    # ## mode参数遍历，直到返回结果
    # ## 网络图片
    elif result =="" and img_url !="":
        for mode in range(6, 13, 1):
            ocr = Ocr(out_path=out_path, mode=mode)
            result = ocr.exec(img_url=img_url)
            print(result)
            if result !="":
                break