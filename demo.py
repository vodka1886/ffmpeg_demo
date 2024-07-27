import subprocess  
import os
from argparse import ArgumentParser

ffmpeg_prc ='./ffmpeg/ffmpeg'
skip_file = ["modified"]



def modify_picture(input_file,output_file,commond):
    print("try convert {} to {}!!!".format(input_file,output_file))
    # 定义FFmpeg命令  
    # 注意：根据你的系统环境，ffmpeg的路径可能需要调整  
    # 这里假设ffmpeg已经添加到系统的PATH环境变量中  
    
    ffmpeg_command = [  
        ffmpeg_prc,  
        '-i', input_file,  # 输入文件  
        '-q',"50",
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

def deal_with_single_file(input_file,out_path=None,commond = "t"):
    support_list = [".jpg",".bmp",".png"]
    input_dir = os.path.dirname(input_file)
    filename = os.path.basename(input_file)
    base_name, extension = os.path.splitext(filename) 
    if extension not in support_list:
        print("not support: ",input_file)
        return
    if not out_path:
        out_path = input_dir
    out_file = os.path.join(out_path,base_name+"_modifyed"+extension)
    if commond == "c":
        if os.path.exists(out_file):
            print("try remove ",out_file)
            os.remove(out_file)
    elif commond == "t":
        modify_picture(input_file,out_file,extension)

def find_all_files(directory):  
    """  
    递归地查找给定目录下的所有文件，包括子目录中的文件。  
    :param directory: 要搜索的目录的路径  
    :return: 一个包含所有找到的文件完整路径的列表  
    """  
    all_files = []  
    for root, dirs, files in os.walk(directory):  
        for file in files:  
            # os.path.join用于安全地构建文件路径  
            file_path = os.path.join(root, file)  
            all_files.append(file_path)  
    return all_files  

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('input_path', help='Root path')
    parser.add_argument(
        '--output_path', default=None, help='version of datasets')
    parser.add_argument('-c', '--clear', action='store_true', help='开启特定功能')  
  
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
    commond = "t"
    if(call_args['clear']):
        commond = "c"
    assert(os.path.exists(input_path))
    if os.path.isdir(input_path):
        for file in find_all_files(input_path):
            deal_with_single_file(file,out_path,commond)
    elif os.path.isfile(input_path):
        deal_with_single_file(input_path,out_path,commond)