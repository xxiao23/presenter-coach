
# 导入系统库并定义辅助函数
from pprint import pformat

# import PythonSDK
from PythonSDK.facepp import API,File

# 导入图片处理类
import PythonSDK.ImagePro

test_img = 'D:\Downloads\eyeclose.jfif'       # 用于创建faceSet


# 此方法专用来打印api返回的信息
def print_result(hit, result):
    print(hit)
    print('\n'.join("  " + i for i in pformat(result, width=75).split('\n')))

def printFuctionTitle(title):
    return "\n"+"-"*60+title+"-"*60;

# 初始化对象，进行api的调用工作
api = API()
# -----------------------------------------------------------人脸识别部分-------------------------------------------

# 人脸检测：https://console.faceplusplus.com.cn/documents/4888373
res = api.detect(image_file=File(test_img), return_attributes="headpose,facequality,eyestatus,emotion,mouthstatus,eyegaze")
print("face area")
print(res['faces'][0]['face_rectangle']['width'] * res['faces'][0]['face_rectangle']['height'])
print("head pose")
print(res['faces'][0]['attributes']['headpose'])
print("mouth occlusion")
print(res['faces'][0]['attributes']['mouthstatus']['other_occlusion'])
print("left eye occlusion")
print(res['faces'][0]['attributes']['eyestatus']['left_eye_status'])
print("right eye occlusion")
print(res['faces'][0]['attributes']['eyestatus']['right_eye_status'])
print(res['faces'][0]['attributes']['eyegaze'])