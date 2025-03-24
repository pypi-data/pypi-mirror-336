# -*- coding: utf-8 -*-
#---------------------------------------------------------
# TITLE : Utils Library
#         각종 유틸리티 라이브러리
# 최종수정일 : 2021.05.23
# 버전: 0.0.5
#---------------------------------------------------------
import logging
import os, glob
import tarfile
import re

## 로거 파일 정의
#log = logging.getLogger(__name__)


def exist_directory(directory, flag=False):
    '''
        디렉토리가 존재하는지 확인한다.
        flag = True면 미존재시 생성
    '''

    if os.path.exists(directory):
        if os.path.isdir(directory):
            return True
    os.makedirs(directory) if flag else ''
    return False



def check_fullpath(file_path, flag_mkfile=False):
    """ 
        디렉토리를 포함한 파일명 받아서 디렉토리 및 파일을 자동으로 생성
        Args:
            file_path: 디렉토리를 포함한 full_path 지정
            flag_mkfile: 파일생성여부 True/False(default)
        return: None
        주의: 디렉토리명만 주면 문제발생
    """
    directory, filename = os.path.split(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    if flag_mkfile:
        if not os.path.exists(file_path):
            open(file_path, 'w').close()


def scan_directory(path, ext=[], recursive=True):
    """ 
        전체디렉토리 검색 (하위디렉토리 포함)

        Argument:
        path: 검색할 디렉토리	
        ext: ['.png','.css'] 특정 파일만 검색시
        recursive: 하위디렉토리 검색여부 True, False
    """
    files = []
    for f in glob.iglob(path + '/**/*',recursive=recursive):		
        if os.path.isdir(f):  
            #print("It is a directory:"+f)
            pass
        elif os.path.isfile(f):
            if ext:
                if os.path.splitext(f)[1].lower() in ext:
                    files.append(f)
            else:
                print("It is a normal file:"+f)
                files.append(f)
        else:  
            print("It is a special file (socket, FIFO, device file)")

    return files


def readConfigFile(filename):
    """
        config용 파일을 읽고 # 또는 공백라인을 제거하고 리스트로 반환한다.
    """

    tmp_list = []

    with open(filename, 'r', encoding='utf8') as f:
        
        for line in f.readlines():
            
            line = line.strip()
                
            if line.startswith('#') or not line:
                continue
            
            tmp_list.append(line)

    return tmp_list


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename+'.tgz', "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def get_file_from_tar(targz, filename):

    tar = tarfile.open(targz, "r:gz")
    try:
        #content = str(tar.extractfile(filename).read().decode('euc-kr'))
        content = tar.extractfile(filename).read()
    #except UnicodeDecodeError:
    #	content = str(tar.extractfile(filename).read()).encode('cp949', 'ignore').decode('cp949')
    except UnicodeDecodeError:
        content = tar.extractfile(filename).read()

    #print('===>', len(content), type(content), targz, filename)
    return content


def exist_file_in_tar(targz, filename):
    """
        Tar 압축파일에 파일에 존재하는지 확인
    """
    tar = tarfile.open(targz, "r:gz")
    try:
        name = tar.getmember(filename)
    except KeyError:
        return False

    return True


def cleanhtml(raw_html):
    """ HTML 태그 없애기 """
    cleanr = re.compile('<.*?>')
    #cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});') # &nbsp; & 시작하는 것도 삭제
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def set_logger(method, logfile, loglevel=logging.DEBUG):
    '''
        root logger 설정
    '''

    #
    # 1. ROOT logger을 만든다.
    #
    logger = logging.getLogger()

    # Create a Formatter for formatting the log messages
    file_formatter = logging.Formatter('[%(asctime)s] %(name)s:%(lineno)s:%(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    if method == 'rotate':
        from logging.handlers import RotatingFileHandler

        # Create the Handler for logging data to a file
        rotate_handler = RotatingFileHandler(logfile, maxBytes=1*1024*1024, backupCount=10, encoding='utf-8')
        rotate_handler.setLevel(loglevel)
        # Add the Formatter to the Handler
        rotate_handler.setFormatter(file_formatter)	
        
        # Add the Handler to the Logger
        logger.addHandler(rotate_handler)
    
    elif method == 'file':
        from logging import FileHandler
        #화면으로 출력하는 부분이지만 사용하지 않음.
        #Create the Handler for logging data to console.
        file_handler = FileHandler(logfile)
        file_handler.setLevel(loglevel)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    else:
        from logging import StreamHandler
        #화면으로 출력하는 부분이지만 사용하지 않음.
        #Create the Handler for logging data to console.
        console_handler = StreamHandler()
        console_handler.setLevel(loglevel)
        stream_formatter = logging.Formatter('%(name)s:%(lineno)s:%(levelname)s >>> %(message)s')
        console_handler.setFormatter(stream_formatter)
        logger.addHandler(console_handler)

    return logger


def add_to_excel(list_to_save, excel_filename):
    
    import openpyxl

    links_excel = openpyxl.load_workbook(filename=excel_filename) 
    sheet = links_excel['Sheet']
    sheet.append(list_to_save)
    links_excel.save(excel_filename)
    links_excel.close()
    return


#
# Datetime 관련 라이브러리
#
def integerToDatetime(timestamp):
		"""integer to datetime"""
		import datetime
		
		date = datetime.datetime.fromtimestamp(timestamp)
		return date


def today(timezone='America/Vancouver'):
    """today 날짜 가져오기"""
    import datetime, pytz

    return datetime.datetime.now(pytz.timezone(timezone)).replace(microsecond=0, tzinfo=None).strftime('%Y%m%d')
    #return datetime.datetime.today().strftime('%Y%m%d')

def now(timezone='America/Vancouver'):
    """현재시간 가져오기"""
    import datetime, pytz

    return datetime.datetime.now(pytz.timezone(timezone)).replace(microsecond=0, tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')