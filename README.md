# capture-scheduler
자사 모니터링 플랫폼을 일정시간 마다 캡처 하기 위하여 해당 동작을 자동화 시킨 캡처 스케줄러 프로그램 입니다.

저같은 경우 일일3회 회사의 지시사항으로 캡처를 진행하라는 업무를 받아서
이 귀찮은 일을 현명하게 해결할 방법을 모색하다 직접 개발을 하게되었습니다.

사용된 언어는 python 이며

사용된 라이브러리는 아래와 같습니다

import os

import time

from datetime import datetime

import tkinter as tk

from tkinter import filedialog, messagebox  # messagebox 추가

from selenium import webdriver

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

import threading

프로그램 UI는 사진을 참조 바랍니다.
![image](https://github.com/Jaemm/capture-scheduler/assets/94304285/8099d265-c9f4-4d62-81f2-95119cea71b5)

기능 구성은
- 현재 시간
- 예약 캡처 기능
- 즉시 캡처 기능
- 예약 리스트 추가, 삭제
- 캡처 기록(log)
으로 구성된 간단한 프로그램 입니다.

소스코드를 사용하실분은 해당 박스 부분 코드를 입맛에 맞게 변경하시면 됩니다.
![image](https://github.com/Jaemm/capture-scheduler/assets/94304285/cc39d023-7606-46a6-8f3c-08032f4418b0)
