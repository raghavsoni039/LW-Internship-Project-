import boto3
import streamlit as st
import cv2
from cvzone.HandTrackingModule import HandDetector
def create_aws():
    st.subheader("🖥️ Launch EC2 Instance Using Hand Gestures")
    cap = cv2.VideoCapture(0)
    if st.button("📸 Capture Hand Gesture"):
        handDetector = HandDetector()
        success, img = cap.read()
        if not success:
            st.error("❌ Failed to access webcam")
        hands, img = handDetector.findHands(img)
        if hands:
            fingers = handDetector.fingersUp(hands[0])
            total_fingers = sum(fingers)
            cap.release()
            cv2.destroyAllWindows()
            st.success(f"🖐️ Fingers Detected: {total_fingers}")
            region = st.text_input("Enter AWS Region", value="ap-south-1")
            ami_id = st.text_input("Enter AMI ID", value="ami-0a3ece531caa5d49d")
            instance_type = st.text_input("Instance Type", value="t2.micro")
            if st.button("Launch EC2 Instances"):
                try:
                    ec2 = boto3.resource("ec2", region_name=region)
                    instances = ec2.create_instances(
                        ImageId=ami_id,
                        MinCount=total_fingers,
                        MaxCount=total_fingers,
                        InstanceType=instance_type
                    )
                    ids = [inst.id for inst in instances]
                    st.success(f"✅ Launched {total_fingers} EC2 Instance(s): {', '.join(ids)}")
                except Exception as e:
                    st.error(f"❌ AWS Error: {str(e)}")