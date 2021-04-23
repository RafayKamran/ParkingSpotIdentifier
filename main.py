import numpy as np
import cv2

# Base variables for the canvas size and colours

CANVAS_SIZE = (600, 800)

FINAL_LINE_COLOR = (0, 255, 0)

WORKING_LINE_COLOR = (0, 0, 0)

# Insert the path to the image here
path = r'C:\Users\Rafay\Desktop\Surrey University\AI\parkingLot.jpg'
img = cv2.imread(path)

isDone = False


class ParkingSpotIdentifier(object):
    def __init__(self, window_name):
        self.window_name = window_name # Sets window name
        self.done = False  # Tracks if you are finished
        self.completed = True
        self.points = []  # List of points that the user has clicked

    def on_mouse(self, event, x, y, buttons, user_param):
        # Handles mouse events
        if self.done:
            return

        if event == cv2.EVENT_LBUTTONDOWN:
            # Left click adds the point to the list
            print("Adding point #%d with position(%d,%d)" % (len(self.points), x, y))
            self.points.append((x, y))
        elif event == cv2.EVENT_RBUTTONDOWN:
            # Right click finishes the drawing
            print("Completing parking spot with %d points." % len(self.points))
            self.done = True

    def run(self):
        # Makes the window and sets mouse callback
        cv2.namedWindow(self.window_name, flags=cv2.WINDOW_AUTOSIZE)
        cv2.imshow(self.window_name, np.zeros(CANVAS_SIZE, np.uint8))
        cv2.waitKey(1)
        cv2.setMouseCallback(self.window_name, self.on_mouse)

        while not self.done:
            canvas = img
            if len(self.points) > 0:
                # Draw current lines
                cv2.polylines(canvas, np.array([self.points]), False, WORKING_LINE_COLOR, 3)
            # Update window
            cv2.imshow(self.window_name, canvas)
            # Esc to cancel current drawing
            if cv2.waitKey(50) == 27:
                self.done = True
                self.completed = False

        # Points have been entered
        canvas = img
        if len(self.points) > 0:
            if (self.completed):
                cv2.fillPoly(canvas, np.array([self.points]), FINAL_LINE_COLOR)
        # Show canvas
        cv2.imshow(self.window_name, canvas)
        # Wait for user to press a key

        print("Press q to quit if you are finished, anything else will start a new drawing")

        if cv2.waitKey() == ord('q'):
            print("pressed q")
            global isDone
            isDone = True
        self.completed = True
        cv2.destroyWindow(self.window_name)
        return canvas


if __name__ == "__main__":
    fh = open('points.txt', 'w+')
    while not isDone:
        pd = ParkingSpotIdentifier("Parking Spot")
        image = pd.run()
        cv2.imwrite("ParkingSpot.png", image)
        print("Parking Spot = %s" % pd.points)
        fh.write('\n'.join('%s %s' % x for x in pd.points) + '\n' + '\n')
    fh.truncate()
