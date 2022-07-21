import numpy as np
import cv2

if __name__ == '__main__':
	image = np.zeros((250, 200, 3), np.uint8)
	image[:] = (230, 250, 255)

	image = cv2.line(image, (32, 30), (32, 220), 0, thickness=8, lineType=cv2.LINE_AA)
	cv2.imwrite("../images/hangman_1.png", image)

	image = cv2.line(image, (32, 30), (132, 30), 0, thickness=8, lineType=cv2.LINE_AA)
	cv2.imwrite("../images/hangman_2.png", image)

	image = cv2.line(image, (133, 30), (133, 70), 0, thickness=5, lineType=cv2.LINE_AA)
	cv2.imwrite("../images/hangman_3.png", image)

	image = cv2.circle(image, (133, 91), 20, 0, thickness=3, lineType=cv2.LINE_AA)
	cv2.imwrite("../images/hangman_4.png", image)

	image = cv2.line(image, (133, 111), (133, 176), 0, thickness=3, lineType=cv2.LINE_AA)
	cv2.imwrite("../images/hangman_5.png", image)

	image = cv2.line(image, (133, 150), (98, 120), 0, thickness=3, lineType=cv2.LINE_AA)
	cv2.imwrite("../images/hangman_6.png", image)

	image = cv2.line(image, (133, 150), (168, 120), 0, thickness=3, lineType=cv2.LINE_AA)
	cv2.imwrite("../images/hangman_7.png", image)

	image = cv2.line(image, (133, 175), (98, 205), 0, thickness=3, lineType=cv2.LINE_AA)
	cv2.imwrite("../images/hangman_8.png", image)

	image = cv2.line(image, (133, 175), (168, 205), 0, thickness=3, lineType=cv2.LINE_AA)
	cv2.imwrite("../images/hangman_9.png", image)
