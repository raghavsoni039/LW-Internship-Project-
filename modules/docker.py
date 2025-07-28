import streamlit as st
from modules.linux import run_ssh_command

def docker_operations():
    st.subheader("🐳 Docker Control Panel")
    user = st.text_input("Enter Username")
    ip = st.text_input("Enter Remote IP")
    docker_options = [
        "Launch New Container", "Stop Container", "Remove Container", "Start Container",
        "See All Images", "List All Containers", "Pull Image from Docker Hub",
        "Exec into Container", "Run Command in Container"
    ]
    choice = st.selectbox("Choose Docker Operation", docker_options)
    c1, c2 = st.columns(2)
    name = c1.text_input("Container/Image Name (if needed)")
    image = c2.text_input("Image Name (for launching container)")
    command_in_container = st.text_input("Command to run inside container (for exec)", key="dock_cmd")

    if st.button("Execute Docker Command"):
        if choice == "Launch New Container":
            output = run_ssh_command(user, ip, f"docker run -dit --name {name} {image}")
        elif choice == "Stop Container":
            output = run_ssh_command(user, ip, f"docker stop {name}")
        elif choice == "Remove Container":
            output = run_ssh_command(user, ip, f"docker rm -f {name}")
        elif choice == "Start Container":
            output = run_ssh_command(user, ip, f"docker start {name}")
        elif choice == "See All Images":
            output = run_ssh_command(user, ip, "docker images")
        elif choice == "List All Containers":
            output = run_ssh_command(user, ip, "docker ps -a")
        elif choice == "Pull Image from Docker Hub":
            output = run_ssh_command(user, ip, f"docker pull {name}")
        elif choice == "Exec into Container":
            output = run_ssh_command(user, ip, f"docker exec -it {name} /bin/bash")
        elif choice == "Run Command in Container":
            output = run_ssh_command(user, ip, f"docker exec {name} {command_in_container}")
        else:
            output = "Invalid Choice"
        st.text_area("📤 Docker Output:", output, height=300)