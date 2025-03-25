"""
pyneople에서 사용되는 함수와 클래스입니다.
"""

import time
import json
import aiohttp
import asyncio  
import requests
from .METADATA import JOBCLASS, SETTINGS, TOTAL_ID_2_SERVER_ID

__all__ = ['change_settings', 'get_request', 'jobname_equalize', 'get_job_info', 'NeopleOpenAPIError', 'ServerMaintenanceError', 'value_flatten', 'attr_flatten']

class NeopleOpenAPIError(Exception):
    """
    Error 핸들링을 위한 Class
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ServerMaintenanceError(Exception):
    """
    Error 핸들링을 위한 Class
    """    
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def change_settings(arg_time_out : int = 5, arg_time_sleep : float = 0.0015):
    """
    request에 필요한 설정 값을 바꾸는 함수

    초기 설정 값은 각각 5초, 0.0015초
        Args :
            arg_time_out(int) : 해당 시간동안 응답이 없으면 에러 처리한다
            
            arg_time_sleep(float) : 한 번의 요청 후 쉬는 시간
    """
    global SETTINGS
    SETTINGS['request_time_out'] = arg_time_out
    SETTINGS['request_time_sleep'] = arg_time_sleep

def get_request(arg_url : str):
    """
    url 입력시 data 가져오는 함수
        Args :
            arg_url(str) : 원하는 url 주소
    """
    start_time = time.time()
    data = requests.get(arg_url, timeout = SETTINGS['request_time_out'])
    data = json.loads(data.text)
    # Neople Open API 상에서 규정된 에러가 발생할 경우 에러를 발생시킨다.
    if data.get("error"):
        if data.get("error").get('status') == 503:
            raise ServerMaintenanceError
        else:
            raise NeopleOpenAPIError(data.get("error"))
    elapsed_time = time.time() - start_time
    if elapsed_time < SETTINGS['request_time_sleep']:
        time.sleep(SETTINGS['request_time_sleep'] - elapsed_time)
    return data

async def async_get_request(arg_url : str):
    """
    url 입력시 data 가져오는 함수
        Args :
            arg_url(str) : 원하는 url 주소
    """
    async with aiohttp.ClientSession(timeout = aiohttp.ClientTimeout(total=SETTINGS['request_time_out'])) as session:
        print(f"요청{time.time()}")
        async with session.get(arg_url) as response:
            await asyncio.sleep(SETTINGS['request_time_sleep'])
            data = await response.json()
            if data.get("error"):
                if data.get("error").get('status') == 503:
                    raise ServerMaintenanceError
                else:
                    raise NeopleOpenAPIError(data.get("error"))
            return data

def _next(arg_dict : dict, arg_list : list):
    """
    get_job_info 함수를 위해 쓰이는 함수
    """
    if 'next' in arg_dict.keys():
        arg_list.append(arg_dict["jobGrowName"])
        return _next(arg_dict['next'], arg_list)
    else :
        arg_list.append(arg_dict["jobGrowName"])
        return arg_dict["jobGrowName"]

def split_total_id(arg_total_id):
    return TOTAL_ID_2_SERVER_ID[arg_total_id[:1]], arg_total_id[1:]

def get_job_info(arg_api_key : str):
    """
    직업 정보를 받아오는 함수
        Args :
            arg_api_key(str) : Neople Open API key
        Retruns :
            Neople Open API 직업 정보 조회 데이터
    """
    return get_request(f"https://api.neople.co.kr/df/jobs?apikey={arg_api_key}")

def get_job_list_for_fame_producer(arg_data):
    """
    직업정보를 받아서 명성 조회에 쓸 list of tuple 반환
        Args :
            arg_data(dict) : Neople Open API 직업 정보 조회 데이터
        Returns :
            [(귀검사(남)_웨펀마스터, 귀검사(남)ID, 웨펀마스터ID) .....]
    """
    job_list = []

    for job in arg_data["rows"]:
        job_name = job["jobName"]
        job_id = job["jobId"]

        for grow in job["rows"]:
            job_grow_name = grow["jobGrowName"]
            job_grow_id = grow["jobGrowId"]

            # 크리에이터와 다크나이트는 "자각1"을 제외하고 표기   
            if job_name in ["크리에이터", "다크나이트"]:
                job_list.append((job_name, job_id, job_grow_id))
            else:
                job_list.append((f"{job_name}_{job_grow_name}", job_id, job_grow_id))

    return job_list

def get_jobname_mapping_dict(arg_data):
    """
    직업정보를 받아서 jobname_equalize에 필요한 mapping dict반환
        Args :
            arg_data(dict) : Neople Open API 직업 정보 조회 데이터
        Returns :
            모든 전직명을 key, 1차 전직명을 value로 가지는 dict
            ex) {'검신' : 웨펀마스터, '검성' : '웨펀마스터' ...}
    """
    mapping_dict = {}

    for job in arg_data['rows']:
        for job_grow in job['rows']:
            base_job_grow_name = job_grow['jobGrowName']
            while job_grow:
                mapping_dict[job_grow['jobGrowName']] = base_job_grow_name
                job_grow = job_grow.get('next')    

    return mapping_dict                

# def jobname_equalize(arg_job_name : str, arg_job_grow_name : str , arg_mapping_dict : dict):
#     """
#     직업명과 전직명을 받으면 해당 전직명으로 반환
#         Args :
#             arg_job_name(str) : 직업명 ex) 총검사
#             arg_job_grow_name(str) : 전직명 ex) 빅보스
#             arg_mapping_dict(dict) : get_job_data_for_jobname_equalize를 통해 가공한 dict
#         Retruns :
#             해당 직업의 1차 전직명 ex) 히트맨
#     """
#     if (arg_job_name in ["다크나이트", "크리에이터"]) or (arg_job_grow_name in list(JOBCLASS.keys())):
#         output = arg_job_name
#     else:    
#         for job in arg_job_info[arg_job_name]:
#             if arg_job_grow_name in job:
#                 output = job
#                 break
#         output = output[0]
#     return output

def explain_enchant(arg_enchant_dict : dict):
    """
    마법부여 정보를 정리해주는 함수
        Args :
            arg_enchant_dict(dict) : 마법부여 정보 dict
    """
    if arg_enchant_dict == {} or arg_enchant_dict == None:
        return None
    output = ""
    if "status" in arg_enchant_dict.keys():
        output = ", ".join([f"{s['name']} {s['value']}" for s in arg_enchant_dict['status']])
    if "reinforceSkill" in arg_enchant_dict.keys():
        output = ", ".join([f"{s['name']} {s['value']}" for r in arg_enchant_dict['reinforceSkill'] for s in r['skills']]) + ", " + output 
    if "explain" in arg_enchant_dict.keys():
        output = arg_enchant_dict['explain'] + ", " + output
    return output

def _is_attr(arg_object):
    """
    하위 속성이 있는지 확인하는 함수
    """
    try:
        arg_object.__dict__.keys()
        return True
    except:
        return False

def _get_attr(arg_object, te = ""):
    """
    객체의 하위 속성명을 list로 만들어주는 함수
    """
    st = []
    for sub in list(arg_object.__dict__.keys()):
        if _is_attr(getattr(arg_object, sub)) == False:
            if sub[0] != "_":
                st.append(te + sub)
        else :     
            st.append(_get_attr(getattr(arg_object, sub), te + sub + "."))    
    return st    

def _get_values(arg_object):
    """
    객체의 하위 속성값을 list로 만들어주는 함수
    """
    st = []
    for sub in list(arg_object.__dict__.keys()):
        if _is_attr(getattr(arg_object, sub)) == False:
            if sub[0] != "_":
                st.append(getattr(arg_object, sub))
        else:
            st.append(_get_values(getattr(arg_object, sub)))    
    return st    

def _flatten(arg_list):
    result = []
    for item in arg_list:
        if isinstance(item, list):
            result += _flatten(item)
        else:
            result.append(item)
    return result

def attr_flatten(arg_object):
    """
    객체를 입력받으면 모든 하위속성의 이름을 문자열 list로 반환한다
    """
    arg_object = _get_attr(arg_object)
    arg_object = _flatten(arg_object)
    return arg_object

def value_flatten(arg_object):
    """
    객체를 입력받으면 모든 하위속성의 값을 list로 반환한다
    """
    arg_object = _get_values(arg_object)
    arg_object = _flatten(arg_object)
    return arg_object