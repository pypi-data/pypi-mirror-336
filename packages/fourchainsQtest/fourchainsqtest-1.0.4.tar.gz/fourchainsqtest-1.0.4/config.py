import sys
import os

# 현재 파일이 위치한 디렉터리를 기준으로 qxenonsign 폴더를 import 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "qxenonsign"))

# PyArmor 난독화된 코드 실행을 위한 필수 파일 import
try:
    import qxenonsign.pyarmor_runtime_000000
except ModuleNotFoundError:
    print("Warning: pyarmor_runtime_000000 모듈을 찾을 수 없습니다. 난독화된 코드가 정상 작동하지 않을 수 있습니다.")

# 난독화된 core.py import
try:
    import qxenonsign.core as qxenonsign
except ModuleNotFoundError:
    print("Warning: core 모듈을 찾을 수 없습니다. core.py가 qxenonsign 폴더 안에 있는지 확인하세요.")
