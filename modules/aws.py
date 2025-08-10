import re
import boto3
import streamlit as st
import cv2
from cvzone.HandTrackingModule import HandDetector

# -----------------------
# Helper / AWS functions
# -----------------------
def launch_instances(count, ami_id, instance_type, region, tag_name):
    """Launch `count` EC2 instances and return list of (id, public_ip)."""
    try:
        ec2 = boto3.resource("ec2", region_name=region)
        with st.spinner(f"Launching {count} instance(s)..."):
            instances = ec2.create_instances(
                ImageId=ami_id,
                MinCount=count,
                MaxCount=count,
                InstanceType=instance_type,
                TagSpecifications=[
                    {
                        "ResourceType": "instance",
                        "Tags": [{"Key": "Name", "Value": tag_name}]
                    }
                ]
            )

            results = []
            for inst in instances:
                inst.wait_until_running()
                inst.reload()
                results.append((inst.id, inst.public_ip_address))
        return results, None
    except Exception as e:
        return None, str(e)

def terminate_instance_by_id(instance_id, region):
    """Terminate instance and wait until terminated."""
    try:
        ec2 = boto3.resource("ec2", region_name=region)
        instance = ec2.Instance(instance_id)
        with st.spinner(f"Terminating {instance_id}..."):
            instance.terminate()
            instance.wait_until_terminated()
        return True, None
    except Exception as e:
        return False, str(e)

# -----------------------
# Streamlit UI & logic
# -----------------------
st.set_page_config(page_title="AWS EC2 Manager (Hand Gestures)", layout="centered")
st.title("🖥️ AWS EC2 Manager — Hand Gesture Launcher")

# Initialize session state keys
if "total_fingers" not in st.session_state:
    st.session_state.total_fingers = None
if "captured_image" not in st.session_state:
    st.session_state.captured_image = None
if "last_launched" not in st.session_state:
    st.session_state.last_launched = []

action = st.radio("Choose Action", ["Launch Instance(s)", "Terminate Instance"])

# ------ Launch Flow ------
if action == "Launch Instance(s)":
    st.markdown("**Step 1 — Capture hand gesture**")
    col1, col2 = st.columns([1, 2])

    with col1:
        if st.button("📸 Capture Hand Gesture"):
            cap = None
            try:
                cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # CV_DSHOW reduces some webcam issues on Windows
                if not cap or not cap.isOpened():
                    st.error("❌ Could not open webcam. Make sure it is not used by another app.")
                else:
                    success, img = cap.read()
                    if not success or img is None:
                        st.error("❌ Failed to read from webcam.")
                    else:
                        handDetector = HandDetector(maxHands=1)
                        hands, img = handDetector.findHands(img)  # returns hands, img
                        # show captured frame (convert BGR -> RGB)
                        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        st.session_state.captured_image = img_rgb
                        if hands:
                            fingers = handDetector.fingersUp(hands[0])
                            total_fingers = sum(fingers)
                            # enforce minimum 1
                            total_fingers = max(1, total_fingers)
                            st.session_state.total_fingers = total_fingers
                            st.success(f"🖐️ Fingers Detected: {total_fingers} (minimum 1 enforced)")
                        else:
                            # No hands detected -> store 1 as default but warn user
                            st.session_state.total_fingers = 1
                            st.warning("No hands detected. Defaulting to 1 instance. Try again for more accurate count.")
            except Exception as e:
                st.error(f"Error during webcam capture: {e}")
            finally:
                if cap:
                    cap.release()

    with col2:
        if st.session_state.captured_image is not None:
            st.image(st.session_state.captured_image, caption="Captured frame")
        else:
            st.info("No image captured yet. Click the camera button to capture a frame.")

    st.markdown("---")
    st.markdown("**Step 2 — AWS configuration / Launch**")
    region = st.text_input("AWS Region", value="ap-south-1", key="launch_region")
    ami_id = st.text_input("AMI ID", value="ami-0d54604676873b4ec", key="launch_ami")
    instance_type = st.text_input("Instance Type", value="t2.micro", key="launch_type")
    tag_name = st.text_input("Tag Name", value="MyBoto3Instance", key="launch_tag")

    if st.button("Launch EC2 Instances"):
        if not st.session_state.total_fingers:
            st.error("No finger count available — capture a gesture first.")
        else:
            count = int(st.session_state.total_fingers)
            # additional safety: limit max to a reasonable number to avoid accidental large launches
            if count > 10:
                st.warning("Requested count > 10. Limiting to 10 instances for safety.")
                count = 10
            results, err = launch_instances(count, ami_id, instance_type, region, tag_name)
            if err:
                st.error(f"AWS Error: {err}")
            else:
                launched_info = []
                for iid, ip in results:
                    launched_info.append(f"{iid} (IP: {ip})")
                st.success(f"✅ Launched {len(results)} instance(s):")
                st.write("\n".join(launched_info))
                # save to session state for future reference
                st.session_state.last_launched = launched_info

# ------ Terminate Flow ------
else:
    st.markdown("**Terminate an EC2 instance**")
    term_region = st.text_input("AWS Region", value="ap-south-1", key="term_region")
    instance_id = st.text_input("Instance ID to terminate (e.g. i-0123456789abcdef0)", key="term_id")

    # basic validation for EC2 instance id
    def valid_instance_id(iid: str):
        return bool(re.match(r"^i-[0-9a-fA-F]{8,}$", iid.strip()))

    if st.button("Terminate EC2 Instance"):
        if not instance_id or not valid_instance_id(instance_id):
            st.error("Please enter a valid EC2 Instance ID (example: i-0123456789abcdef0).")
        else:
            ok, err = terminate_instance_by_id(instance_id.strip(), term_region)
            if ok:
                st.success(f"✅ Instance {instance_id.strip()} terminated.")
            else:
                st.error(f"AWS Error: {err}")

# Show last launched info (if any)
if st.session_state.get("last_launched"):
    st.markdown("---")
    st.markdown("**Recently launched**")
    for info in st.session_state.last_launched:
        st.write(info)
