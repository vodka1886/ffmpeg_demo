import subprocess  
import os
from argparse import ArgumentParser
import cv2
import shutil

ffmpeg_prc ='./ffmpeg/ffmpeg'
skip_file = ["modified"]
max_image_size = 800
min_size_bytes = 1 * 1024 * 1024 

def modify_picture(input_file,output_file,quality = "10"):
    if not os.path.exists(input_file):
        return
    if os.path.exists(output_file):
        print("try remove ",output_file)
        os.remove(output_file)
    # do copy for small file
    if os.path.getsize(input_file) < min_size_bytes:
        print("copy small file {} to {}!!!".format(input_file,output_file))
        shutil.copy(input_file,output_file)
        return 
    # do transform    
    print("try convert {} to {}!!!".format(input_file,output_file))
    
    # resize
    image = cv2.imread(input_file)
    image = cv2.imread(input_file)
    image_H,image_W,channel = image.shape
    if image_W > max_image_size:
        WH_ratio = float(image_W) / image_H
        image_W = max_image_size
        image_H = int (max_image_size / WH_ratio)
    elif image_H > max_image_size:
        WH_ratio = float(image_W) / image_H
        image_H = max_image_size
        image_W = int (max_image_size * WH_ratio)
    # image = cv2.resize(image,(image_W,image_H))

    # input_dir = os.path.dirname(input_file)
    # filename = os.path.basename(input_file)
    # base_name, extension = os.path.splitext(filename) 
    # tmp_image_file = os.path.join(input_dir,base_name+"_tmp"+extension)
    # if os.path.exists(tmp_image_file):
    #     os.remove(tmp_image_file)
    # cv2.imwrite(tmp_image_file,image)
    
    # 定义FFmpeg命令  
    # 注意：根据你的系统环境，ffmpeg的路径可能需要调整  
    # 这里假设ffmpeg已经添加到系统的PATH环境变量中  
    
    ffmpeg_command = [  
        ffmpeg_prc,  
        '-i', input_file,  # 输入文件  
        '-vf', "scale={}:{}".format(image_W,image_H),
        '-q', quality,
        output_file        # 输出文件  
    ]  
    
    # 使用subprocess.run执行FFmpeg命令  
    # 注意：stdout和stderr参数设置为subprocess.PIPE可以捕获命令的输出  
    # 但对于FFmpeg来说，通常设置为None或subprocess.DEVNULL以避免不必要的输出  
    result = subprocess.run(ffmpeg_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  
    
    # 检查命令是否成功执行  
    if result.returncode == 0:  
        print("FFmpeg命令执行成功！")  
    else:  
        print("FFmpeg命令执行失败，返回码：", result.returncode)
    # os.remove(tmp_image_file)

def deal_with_single_file(input,output=None,commond = "t",quality = "10"):
    assert(os.path.isfile(input) and os.path.exists(input))
    # check is support
    support_list = [".jpg",".bmp",".png"]
    input_dir = os.path.dirname(input)
    filename = os.path.basename(input)
    base_name, extension = os.path.splitext(filename) 
    if extension not in support_list:
        print("not support: ",input)
        return
    # prepare output path
    out_path = output
    if out_path == None: 
        out_path = input_dir  
    if os.path.isdir(out_path):
        if out_path == input_dir:
            out_file = os.path.join(out_path,base_name+"_modified"+extension)
        else:
            out_file = os.path.join(out_path,filename)
    else:
        out_file = out_path
        
    if commond == "c" :
        for ele in skip_file:
            if ele in input:
                print("try remove: ",input)
                os.remove(input)
    if commond == "t":
        skiped = False
        for ele in skip_file:
            if ele in input:
                skiped = True
                break
        if not skiped:
            modify_picture(input,out_file,quality)

def prepare_file_paths(input_path,output_path:str=None,file_list:list = None):  
    """  
    递归地查找给定目录下的所有文件，包括子目录中的文件。  
    :param directory: 要搜索的目录的路径  
    :return: 一个包含所有找到的文件完整路径的列表  
    """  
    assert(os.path.isdir(input_path))
    if not output_path:
        output_path = input_path
    if file_list == None:
        file_list = []
    for item in os.listdir(input_path):
        if os.path.isdir(os.path.join(input_path,item)):
            if not os.path.exists(os.path.join(output_path,item)):
                os.makedirs(os.path.join(output_path,item))
            prepare_file_paths(os.path.join(input_path,item),os.path.join(output_path,item),file_list)
        if os.path.isfile(os.path.join(input_path,item)):
            file_list.append((os.path.join(input_path,item),os.path.join(output_path,item)))
    return file_list

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('input_path', help='Root path')
    parser.add_argument(
        '-o','--output_path', default=None, help='version of datasets')
    parser.add_argument('-c', '--clear', action='store_true', help='开启特定功能')  
    parser.add_argument(
        '-q','--quality', default="10", help='version of datasets')
  
    # parser.add_argument(
    #     '--dst_version',
    #     type=str,
    #     default='v1.0-demo',
    #     help='dst version')
   
    call_args = vars(parser.parse_args())
    return call_args

if __name__=='__main__':
    call_args = parse_args()
    input_path = call_args['input_path']
    out_path = call_args['output_path']
    quality = call_args['quality']
    commond = "t"
    if(call_args['clear']):
        commond = "c"
    assert(os.path.exists(input_path))
    if os.path.isdir(input_path):
        if out_path != None and os.path.exists(out_path):
            out_path = os.path.join(out_path,"output")
            if os.path.exists(out_path):
                shutil.rmtree(out_path)
            os.makedirs(out_path)
        for file_pare in prepare_file_paths(input_path,out_path):
            deal_with_single_file(file_pare[0],file_pare[1],commond,quality)
    elif os.path.isfile(input_path):
        deal_with_single_file(input_path,out_path,commond,quality)