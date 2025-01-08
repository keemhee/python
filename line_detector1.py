import cv2
import numpy as np

def main():
    # 카메라 초기화
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # ROI 설정 (이미지 크기에 따라 조정 필요)
        height, width, _ = frame.shape
        roi = frame[height//2:, :]  # 하단 절반

        # HSV 변환 및 노란색 범위 필터링
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # 컨투어 탐색
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # 가장 큰 컨투어 선택
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)

            if M["m00"] != 0:
                # cx: 노란 라인의 중심 x 좌표
                cx = int(M["m10"] / M["m00"])
                # x1: 로봇 중심 기준 x 좌표
                x1 = width // 2
                # error 계산
                error = x1 - cx

                # 방향 메시지 결정
                if error > 10:
                    direction = "Turn Left"  # 기준보다 오른쪽 -> 왼쪽으로 회전
                elif error < -10:
                    direction = "Turn Right"  # 기준보다 왼쪽 -> 오른쪽으로 회전
                else:
                    direction = "Go Straight"

                # 화면 표시
                cv2.line(roi, (cx, 0), (cx, height//2), (255, 0, 0), 2)  # 노란선 중심선
                cv2.line(roi, (x1, 0), (x1, height//2), (0, 255, 0), 2)  # 로봇 기준선
                cv2.putText(roi, f"Error: {error}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(roi, direction, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                # ROS 제어 명령 생성 (가상)
                print(f"Control Command: {direction}, Error: {error}")

        # 결과 출력
        cv2.imshow("ROI", roi)
        cv2.imshow("Mask", mask)

        # 종료 조건
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
