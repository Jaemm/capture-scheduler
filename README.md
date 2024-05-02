# capture-scheduler
모니터링 플랫폼을 일정시간 마다 캡처 하기 위하여 해당 동작을 자동화 시킨 캡처 스케줄러 프로그램 입니다.

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
