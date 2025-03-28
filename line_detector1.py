1| import cv2  # OpenCV 라이브러리 임포트
2| import numpy as np  # NumPy 라이브러리 임포트
3| 
4| def main():  # 메인 함수 정의
5|     # 카메라 초기화
6|     cap = cv2.VideoCapture(0)  # 기본 카메라 장치 열기
7| 
8|     while True:  # 무한 루프 시작
9|         ret, frame = cap.read()  # 카메라로부터 프레임 읽기
10|         if not ret:  # 프레임을 읽지 못하면 루프 종료
11|             break
12| 
13|         # ROI 설정 (이미지 크기에 따라 조정 필요)
14|         height, width, _ = frame.shape  # 프레임의 높이, 너비 가져오기
15|         roi = frame[height//2:, :]  # 하단 절반을 ROI로 설정
16| 
17|         # HSV 변환 및 노란색 범위 필터링
18|         hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)  # ROI를 HSV 색공간으로 변환
19|         lower_yellow = np.array([20, 100, 100])  # 노란색 범위의 하한값
20|         upper_yellow = np.array([30, 255, 255])  # 노란색 범위의 상한값
21|         mask = cv2.inRange(hsv, lower_yellow, upper_yellow)  # 노란색 영역 마스크 생성
22| 
23|         # 컨투어 탐색
24|         contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 마스크에서 컨투어 찾기
25|         if contours:  # 컨투어가 있으면
26|             # 가장 큰 컨투어 선택
27|             largest_contour = max(contours, key=cv2.contourArea)  # 가장 큰 컨투어 선택
28|             M = cv2.moments(largest_contour)  # 가장 큰 컨투어의 모멘트 계산
29| 
30|             if M["m00"] != 0:  # 모멘트의 0차 모멘트가 0이 아니면
31|                 # cx: 노란 라인의 중심 x 좌표
32|                 cx = int(M["m10"] / M["m00"])  # 중심 x 좌표 계산
33|                 # x1: 로봇 중심 기준 x 좌표
34|                 x1 = width // 2  # 화면의 중심 x 좌표
35|                 # error 계산
36|                 error = x1 - cx  # 중심 좌표와 화면 중심의 차이 계산
37| 
38|                 # 방향 메시지 결정
39|                 if error > 10:
40|                     direction = "Turn Left"  # 기준보다 오른쪽 -> 왼쪽으로 회전
41|                 elif error < -10:
42|                     direction = "Turn Right"  # 기준보다 왼쪽 -> 오른쪽으로 회전
43|                 else:
44|                     direction = "Go Straight"  # 기준과 거의 일치 -> 직진
45| 
46|                 # 화면 표시
47|                 cv2.line(roi, (cx, 0), (cx, height//2), (255, 0, 0), 2)  # 노란선 중심선 표시
48|                 cv2.line(roi, (x1, 0), (x1, height//2), (0, 255, 0), 2)  # 로봇 기준선 표시
49|                 cv2.putText(roi, f"Error: {error}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)  # 오차 표시
50|                 cv2.putText(roi, direction, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)  # 방향 표시
51| 
52|                 # ROS 제어 명령 생성 (가상)
53|                 print(f"Control Command: {direction}, Error: {error}")  # 제어 명령 출력
54| 
55|         # 결과 출력
56|         cv2.imshow("ROI", roi)  # ROI 화면에 표시
57|         cv2.imshow("Mask", mask)  # 마스크 화면에 표시
58| 
59|         # 종료 조건
60|         if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' 키를 누르면 루프 종료
61|             break
62| 
63|     cap.release()  # 카메라 자원 해제
64|     cv2.destroyAllWindows()  # 모든 OpenCV 창 닫기
65| 
66| if __name__ == "__main__":  # 스크립트가 직접 실행될 경우
67|     main()  # main 함수 호출
68| 
