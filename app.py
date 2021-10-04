import cv2
import streamlit as st
from streamlit_webrtc import VideoProcessorBase, webrtc_streamer, RTCConfiguration,WebRtcMode


RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

class VideoTransformer(VideoProcessorBase):
    def __init__(self):
        self.threshold1 = 100
        self.threshold2 = 200

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")

        img = cv2.cvtColor(cv2.Canny(img, self.threshold1, self.threshold2), cv2.COLOR_GRAY2BGR)

        return img

class CameraFrame(VideoProcessorBase):

    def camera(self, frame):
        cam = frame.to_ndarray(format="bgr24")
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        return cam


playing1 = st.checkbox("Playing1", value=False)

camf = webrtc_streamer(key="media-constraints1", video_processor_factory=CameraFrame,
                        desired_playing_state=playing1,
                        mode=WebRtcMode.SENDRECV,
                        rtc_configuration=RTC_CONFIGURATION)

playing2 = st.checkbox("Playing2", value=False)
ctx = webrtc_streamer(key="media-constraints2", video_processor_factory=VideoTransformer,
                        desired_playing_state=playing2,
                        mode=WebRtcMode.SENDRECV,
                        rtc_configuration=RTC_CONFIGURATION)


if ctx.video_transformer:
    ctx.video_transformer.threshold1 = st.slider("Threshold1", 0, 1000, 100)
    ctx.video_transformer.threshold2 = st.slider("Threshold2", 0, 1000, 200)
