import streamlit as st
import cv2
import numpy as np
import os

# --- [0] 이미지 읽기 함수 (웹 환경 최적화) ---
def imread_web(path):
    try:
        # 웹 환경에서는 한글 경로 처리가 필요 없으므로 일반적인 imread를 사용하되
        # 파일이 있는지 확인하는 절차를 거칩니다.
        if not os.path.exists(path):
            return None
        img = cv2.imread(path)
        return img
    except Exception:
        return None

# 웹 페이지 넓게 설정
st.set_page_config(page_title="OpenCV 과제 최종", layout="wide")
st.title("🖼️ OpenCV 이미지 처리 (500x500 고정 모드)")

# --- [1] 이미지 경로 설정 (중요: C:\ 주소를 모두 지웠습니다!) ---
# GitHub 저장소에 같이 올린 파일 이름만 적어주면 됩니다.
path1 = "lizard.jpg"
path2 = "bieber.jpg"
path_obj = "object.jpg"
path_back = "background.png"

# 이미지 로드
raw_img1 = imread_web(path1)
raw_img2 = imread_web(path2)
raw_obj = imread_web(path_obj)
raw_back = imread_web(path_back)

# --- [2] 모든 이미지 크기를 500x500으로 조절 ---
def resize_500(img):
    if img is not None:
        return cv2.resize(img, (500, 500))
    return None

img1 = resize_500(raw_img1)
img2 = resize_500(raw_img2)
img_obj = resize_500(raw_obj)
img_back = resize_500(raw_back)

# --- [3] 사이드바 메뉴 ---
menu = st.sidebar.selectbox(
    "기능 선택",
    ["메인 화면", "이미지 더하기", "이미지 블렌딩", "차영상 (Subtract)", "차이 영상 (Absdiff)", "회전 (Rotation)", "사이즈 변경", "이동 (Translation)"]
)

# 이미지 파일이 하나라도 없을 경우 안내 메시지 출력
if img1 is None:
    st.error(f"❌ '{path1}' 파일을 찾을 수 없습니다.")
    st.info("GitHub 저장소에 lizard.jpg 파일이 업로드되어 있는지 확인해주세요!")
    st.stop()

# 고정된 크기 정보
h, w = 500, 500

# --- [4] 기능 구현 ---
if menu == "메인 화면":
    st.subheader("원본 이미지 확인 (500x500 확대됨)")
    col1, col2 = st.columns(2)
    col1.image(img1, channels="BGR", caption="Lizard (500x500)", use_container_width=True)
    if img2 is not None:
        col2.image(img2, channels="BGR", caption="Bieber (500x500)", use_container_width=True)
    else:
        st.warning("bieber.jpg 파일이 업로드되지 않았습니다.")

elif menu == "이미지 더하기":
    st.subheader("이미지 더하기")
    if img2 is not None:
        res_add = cv2.add(img1, img2)
        res_plus = img1 + img2
        c1, c2 = st.columns(2)
        c1.image(res_add, channels="BGR", caption="cv2.add() (Saturation)", use_container_width=True)
        c2.image(res_plus, channels="BGR", caption="Numpy + (Modulo)", use_container_width=True)
    else:
        st.error("bieber.jpg가 없습니다.")

elif menu == "이미지 블렌딩":
    st.subheader("이미지 블렌딩")
    if img2 is not None:
        alpha = st.slider("Alpha (투명도 조절)", 0.0, 1.0, 0.5)
        res_blend = cv2.addWeighted(img1, alpha, img2, 1-alpha, 0)
        st.image(res_blend, channels="BGR", caption=f"결과 이미지 (Alpha: {alpha})")
    else:
        st.error("bieber.jpg가 없습니다.")

elif menu == "차영상 (Subtract)":
    st.subheader("차영상 (Subtract)")
    if img_obj is not None and img_back is not None:
        res_sub = cv2.subtract(img_obj, img_back)
        c1, c2, c3 = st.columns(3)
        c1.image(img_obj, channels="BGR", caption="Object", use_container_width=True)
        c2.image(img_back, channels="BGR", caption="Background", use_container_width=True)
        c3.image(res_sub, channels="BGR", caption="Subtract 결과", use_container_width=True)
    else:
        st.warning("object.jpg 또는 background.png가 없어 시연이 불가능합니다.")

elif menu == "차이 영상 (Absdiff)":
    st.subheader("차이 영상 (Absdiff)")
    if img_obj is not None and img_back is not None:
        res_diff = cv2.absdiff(img_obj, img_back)
        c1, c2, c3 = st.columns(3)
        c1.image(img_obj, channels="BGR", caption="Image A", use_container_width=True)
        c2.image(img_back, channels="BGR", caption="Image B", use_container_width=True)
        c3.image(res_diff, channels="BGR", caption="Absdiff 결과", use_container_width=True)

elif menu == "회전 (Rotation)":
    st.subheader("이미지 회전")
    angle = st.slider("각도", -180, 180, 0)
    M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1)
    res = cv2.warpAffine(img1, M, (w, h))
    st.image(res, channels="BGR")

elif menu == "사이즈 변경":
    st.subheader("사이즈 변경 (500x500 기준)")
    scale = st.slider("배율 조절", 0.1, 2.0, 1.0)
    res = cv2.resize(img1, None, fx=scale, fy=scale)
    st.image(res, channels="BGR")

elif menu == "이동 (Translation)":
    st.subheader("이미지 이동")
    tx = st.slider("X축 이동", -250, 250, 0)
    ty = st.slider("Y축 이동", -250, 250, 0)
    M = np.float32([[1, 0, tx], [0, 1, ty]])
    res = cv2.warpAffine(img1, M, (w, h))
    st.image(res, channels="BGR")
