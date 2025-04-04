import cv2  # OpenCV 라이브러리 임포트
import numpy as np  # NumPy 라이브러리 임포트

def main():  # 메인 함수 정의
    # 카메라 초기화
    cap = cv2.VideoCapture(0)  # 기본 카메라 장치 열기

    while True:  # 무한 루프 시작
        ret, frame = cap.read()  # 카메라로부터 프레임 읽기
        if not ret:  # 프레임을 읽지 못하면 루프 종료
            break

        # ROI 설정 (이미지 크기에 따라 조정 필요)
        height, width, _ = frame.shape  # 프레임의 높이, 너비 가져오기
        roi = frame[height//2:, :]  # 하단 절반을 ROI로 설정

        # HSV 변환 및 노란색 범위 필터링
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)  # ROI를 HSV 색공간으로 변환
        lower_yellow = np.array([20, 100, 100])  # 노란색 범위의 하한값
        upper_yellow = np.array([30, 255, 255])  # 노란색 범위의 상한값
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)  # 노란색 영역 마스크 생성

        # 노이즈 제거 (Step 2에서 추가)
        kernel = np.ones((5, 5), np.uint8)  # 5x5 커널 생성
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # 열림 연산으로 노이즈 제거
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # 닫힘 연산으로 작은 구멍 메우기

        # 컨투어 탐색
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 마스크에서 컨투어 찾기
        if contours:  # 컨투어가 있으면
            # 가장 큰 컨투어 선택
            largest_contour = max(contours, key=cv2.contourArea)  # 가장 큰 컨투어 선택
            M = cv2.moments(largest_contour)  # 가장 큰 컨투어의 모멘트 계산

            if M["m00"] != 0:  # 모멘트의 0차 모멘트가 0이 아니면
                # cx: 노란 라인의 중심 x 좌표
                cx = int(M["m10"] / M["m00"])  # 중심 x 좌표 계산
                # x1: 로봇 중심 기준 x 좌표
                x1 = width // 2  # 화면의 중심 x 좌표
                # error 계산
                error = x1 - cx  # 중심 좌표와 화면 중심의 차이 계산

                # 방향 메시지 결정
                if error > 10:
                    direction = "Turn Left"  # 기준보다 오른쪽 -> 왼쪽으로 회전
                elif error < -10:
                    direction = "Turn Right"  # 기준보다 왼쪽 -> 오른쪽으로 회전
                else:
                    direction = "Go Straight"  # 기준과 거의 일치 -> 직진

                # 화면 표시
                cv2.line(roi, (cx, 0), (cx, height//2), (255, 0, 0), 2)  # 노란선 중심선 표시
                cv2.line(roi, (x1, 0), (x1, height//2), (0, 255, 0), 2)  # 로봇 기준선 표시
                cv2.putText(roi, f"Error: {error}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)  # 오차 표시
                cv2.putText(roi, direction, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)  # 방향 표시

                # ROS 제어 명령 생성 (가상)
                print(f"Control Command: {direction}, Error: {error}")  # 제어 명령 출력

        # 결과 출력
        cv2.imshow("ROI", roi)  # ROI 화면에 표시
        cv2.imshow("Mask", mask)  # 마스크 화면에 표시

        # 종료 조건
        if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' 키를 누르면 루프 종료
            break

    cap.release()  # 카메라 자원 해제
    cv2.destroyAllWindows()  # 모든 OpenCV 창 닫기

if __name__ == "__main__":  # 스크립트가 직접 실행될 경우
    main()  # main 함수 호출
