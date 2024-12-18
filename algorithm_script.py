# each of the circuits has only one 𝑋 rotation gate with a random angle. The circuit is repeated five times with different random rotations
#0번째 큐비트에 임의의 각도로 X 회전 게이트를 적용한 5개의 양자 회로를 실행하고, 측정 결과와 각도 값, 그리고 실행 비용을 저장하는 작업을 수행

import os
import numpy as np

from braket.aws import AwsDevice
from braket.circuits import Circuit

#양자 작업 결과 저장
from braket.jobs import save_job_result

#양자 작업 추적 및 모니터링
from braket.tracking import Tracker

t = Tracker().start()

print("Test job started!")

# Use the device declared in the creation script
device = AwsDevice(os.environ["AMZN_BRAKET_DEVICE_ARN"])

#측정 결과(0/1)와 각도 값을 저장할 빈 리스트를 초기화
counts_list = []
angle_list = []

for _ in range(5):
    # 임의의 각도 값을 생성
    # 고전 컴퓨팅 리소스 사용
    angle = np.pi * np.random.randn()
    
    # 양자 컴퓨팅 리소스 사용
    # 임의의 각도로 X 회전 게이트를 적용한 양자 회로를 생성
    random_circuit = Circuit().rx(0, angle)

     # 회전 이후 결과를 측정
    task = device.run(random_circuit, shots=100)
    counts = task.result().measurement_counts

    # 각도와 측정 결과를 리스트에 추가
    # 고전 리소스(메모리) 사용
    angle_list.append(angle)
    counts_list.append(counts)
    print(counts)

# Save the variables of interest so that we can access later
# 측정 결과, 각도 값, 그리고 예상 실행 비용을 키 밸류 형태로 저장
# 고전 리소스 사용
save_job_result({"counts": counts_list, "angle": angle_list, "estimated cost": t.qpu_tasks_cost() + t.simulator_tasks_cost()})


print("Test job completed!")
