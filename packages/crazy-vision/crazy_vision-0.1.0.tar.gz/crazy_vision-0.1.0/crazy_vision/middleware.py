import cv2

class FrameResizer:
    def __init__(self, target_width=1344, target_height=760, interpolation=cv2.INTER_AREA):
        self.target_width = target_width
        self.target_height = target_height
        self.interpolation = interpolation

    def resize_frame(self, frame):
        """
        Resize the given frame to a fixed size.
        """
        return cv2.resize(frame, (self.target_width, self.target_height), interpolation=self.interpolation)


def process_frame(frame, target_width=1344, target_height=760, interpolation=cv2.INTER_AREA):
    """
    Convenience function to resize a frame without instantiating the class.
    """
    return cv2.resize(frame, (target_width, target_height), interpolation=interpolation)
