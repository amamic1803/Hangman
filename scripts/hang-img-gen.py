import numpy as np
import cv2


def main():
	image = np.zeros((250, 200, 3), np.uint8)
	image[:] = (230, 250, 255)

	for i in range(1, 10):
		match i:
			case 1:
				image = cv2.line(image, (32, 30), (32, 220), (0, 0, 0), thickness=8, lineType=cv2.LINE_AA)
			case 2:
				image = cv2.line(image, (32, 30), (132, 30), (0, 0, 0), thickness=8, lineType=cv2.LINE_AA)
			case 3:
				image = cv2.line(image, (133, 30), (133, 70), (0, 0, 0), thickness=5, lineType=cv2.LINE_AA)
			case 4:
				image = cv2.circle(image, (133, 91), 20, (0, 0, 0), thickness=3, lineType=cv2.LINE_AA)
			case 5:
				image = cv2.line(image, (133, 111), (133, 176), (0, 0, 0), thickness=3, lineType=cv2.LINE_AA)
			case 6:
				image = cv2.line(image, (133, 150), (98, 120), (0, 0, 0), thickness=3, lineType=cv2.LINE_AA)
			case 7:
				image = cv2.line(image, (133, 150), (168, 120), (0, 0, 0), thickness=3, lineType=cv2.LINE_AA)
			case 8:
				image = cv2.line(image, (133, 175), (98, 205), (0, 0, 0), thickness=3, lineType=cv2.LINE_AA)
			case 9:
				image = cv2.line(image, (133, 175), (168, 205), (0, 0, 0), thickness=3, lineType=cv2.LINE_AA)

		cv2.imwrite(f"../resources/images/hangman_{i}.png", image, [cv2.IMWRITE_PNG_COMPRESSION, 9])


if __name__ == '__main__':
	main()
