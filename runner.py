from pathlib import Path 
from s3_object import S3_object
from enum import Enum
from dotenv import dotenv_values

test_paths = [
     '~/iCloud/Downloads/Weight History'
    ,'~/iCloud/Downloads/Weight History/Data Frame-Weight Input.csv'
    ,'~/iCloud/Downloads/Weight History/*.csv'
    ,'~/bogus'
]

class outcome(Enum):
    NOEXIST = 1
    NOTARGET = 2
    SINGLETARGET = 3
    MULTITARGET = 4
    UNKNOWN = 9

"""  
for item in test_paths:
    path = Path(item).expanduser()
    if path.name.count('*') > 0 and path.parent.exists():
        status = outcome.MULTITARGET
    elif not path.exists(): 
        status = outcome.NOEXIST
    elif path.is_dir():
        status = outcome.NOTARGET
    else:
        status = outcome.SINGLETARGET
    print(item, status)
"""

s3_object = S3_object()
config = dotenv_values(".env")
print(s3_object.upload_s3('~/iCloud/Downloads/Budget Input.csv', config['S3_BUCKET'], key_prefix=config['DATA_SETS']))










#p = Path(test_path)
#print ((p := Path(test_path)).parent)
#print(p.name)
#print(p.glob())




#print(*object.upload_s3('~/iCloud/Downloads/Empty', None))