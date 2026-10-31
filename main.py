import cv2
import numpy as np
import mediapipe as mp


color_index = (50,50,255) #the color of the lines
lines_width = 5 #width lines in pixels
rainbow_status = False

#keybinds
# q --> close
# e --> erase 
# p --> take a picture of the canvas + frame


class Camera():
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.frame_size = [int(self.cam.get(3)), int(self.cam.get(4))]
        self.canva = None
        self.erase()
        self.past = None
        self.frame = None
        self.i = 0

    def get_frame(self):
        success, self.frame = self.cam.read() 
        if success:
            self.frame = cv2.flip(self.frame, 1)
            RGB_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            result = hand.process(RGB_frame)
            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    index_coord = hand_landmarks.landmark[8]
                    thumb_coord = hand_landmarks.landmark[4]

                    dist = math.hypot(index_coord.x - thumb_coord.x, index_coord.y - thumb_coord.y)
                    if dist < 0.06:
                        status = "pinching" 
                        point = (int((index_coord.x + thumb_coord.x)/2 * self.frame_size[0]), int((index_coord.y + thumb_coord.y)/2 * self.frame_size[1]))

                        if self.past != None:
                            cv2.line(self.canva, self.past, point, self.get_rainbow_color(rainbow_status), lines_width)
                            print((self.i//255)%6, self.get_rainbow_color())
                        self.past = point
                        self.i +=2 #speed at which colors change
                    else:
                        status = "Neutral"
                        self.past = None

                    print(dist, status)

                    mp_drawing.draw_landmarks(self.frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            mask = self.canva.any(axis=2) #adds every pixel that has color (so doesnt have (0,0,0) for the 3rd variable in canva (so axis=2)) to mask
            self.frame[mask] = self.canva[mask] #boolean indexing --> replace all the pixels that are in the mask in frame by the ones in canva 
            cv2.imshow('frame', self.frame)

    def get_rainbow_color(self, status = True, color = color_index):
        if status:
            index = (self.i//256 %6) #256*6 total colors?
            t = (self.i)%256
            return [(255, t%255, 0), (255 - t%255, 255, 0), (0, 255, t%255), (0, 255-t%255, 255), (t%255,0,255), (255, 0, 255-t%255)][index]
        else:
            return color

            
    def return_frame_photo(self):
        return self.frame

    def erase(self):
        self.canva = np.zeros((self.frame_size[1], self.frame_size[0], 3), dtype=np.uint8)

if __name__ == "__main__":
    mp_drawing =mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    hand = mp_hands.Hands(max_num_hands = 1, model_complexity = 0, min_detection_confidence = 0.6, min_tracking_confidence = 0.7)

    p = Camera()

    while True:
        p.get_frame()
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('p'):
            cv2.imwrite('frame.png', p.return_frame_photo())
            print("Frame saved as frame.png")
        elif key == ord('e'):
            p.erase()
            print("erased canvas")
