from typing import List
import random

def gener_id_from_list(some_list: List):
    flag = False
    id = int(random.uniform(0,100))
    for k,v in some_list.items():
        if k == id:
            flag = True
            
    if flag:
        return gener_id_from_list(some_list)
    else:
        return id

def read_dict_in_list(some_list: List, return_value: str, value: int | str):
    for object in some_list:
            for k,v in object.items():
                if k == return_value:
                    if v == value:
                        return object