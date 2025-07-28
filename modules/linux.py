import streamlit as st
import subprocess

def run_ssh_command(user, ip, command):
    full_cmd = f'ssh {user}@{ip} "{command}"'
    try:
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)



def linux_operations():
    st.subheader("🐧 Linux Remote Shell")
    user = st.text_input("Enter Username")
    ip = st.text_input("Enter Remote IP")

    if "linux_path" not in st.session_state:
        st.session_state.linux_path = "~"

    options = [
        "Create Directory","Know Current Date","Show Free RAM Status","Show System Uptime","Show Current User","Print Calendar","Change Directory","Check IP Address","Check Internet Connectivity","Create Empty File","Create File","Create Variable","Show Current Logged-in Users","Delete a File","Delete a Folder","Disk Usage","Edit File in Gedit","Edit File in Vim","Go One Folder Back","Show First N Lines of a File","Help Command","Know Current Directory","List Files & Directories","Manual for Commands","Monitor Real-Time Memory Usage","Pipe Example","Print Date","Print Message on Terminal","Print Variable","Read/View File Content","Reboot the System","Redirect Output to File","Remove Directory","Search Text in File","Search for a File","Show Last Logins","Show Network Statistics","Show System Information","Stop Firewall","Terminate Task","Show Running Processes"]
    choice = st.selectbox("Choose Operation", options)
    extra_input = st.text_input("Enter Filename/Directory/Command (if needed):")
    extra_input2 = st.text_input("Extra Input (e.g., lines, text to search)", key="extra2")

    if st.button("Execute"):
        current_path = st.session_state.linux_path
        cmd = ""
        if choice == "Know Current Directory":
            cmd = f"cd {current_path} && pwd"

        elif choice == "List Files & Directories":
            cmd = f"cd {current_path} && ls"

        elif choice == "Change Directory":
            test = run_ssh_command(user, ip, f"cd {current_path}/{extra_input}")
            if "No such file" not in test:
                st.session_state.linux_path = f"{current_path}/{extra_input}".replace("//", "/")
                cmd = f"echo 'Changed to {st.session_state.linux_path}'"
            else:
                cmd = "echo 'Directory does not exist.'"

        elif choice == "Go One Folder Back":
            st.session_state.linux_path = "/".join(current_path.split("/")[:-1])
            cmd = f"cd {st.session_state.linux_path} && pwd"

        elif choice == "Create Directory":
            cmd = f"cd {current_path} && mkdir {extra_input}"

        elif choice == "Create File":
            cmd = f"cd {current_path} && touch {extra_input}"

        elif choice == "Create Empty File":
            cmd = f"cd {current_path} && touch {extra_input}"

        elif choice == "Delete a File":
            cmd = f"cd {current_path} && rm {extra_input}"

        elif choice == "Delete a Folder":
            cmd = f"cd {current_path} && rm -r {extra_input}"

        elif choice == "Edit File in Gedit":
            cmd = f"gedit {extra_input}"

        elif choice == "Edit File in Vim":
            cmd = f"cd {current_path} && vi {extra_input}"

        elif choice == "Read/View File Content":
            cmd = f"cd {current_path} && cat {extra_input}"

        elif choice == "Print Calendar":
            cmd = "cal"

        elif choice == "Print Date":
            cmd = "date"

        elif choice == "Know Current Date":
            cmd = "date"

        elif choice == "Print Message on Terminal":
            cmd = f"echo \"{extra_input}\""

        elif choice == "Create Variable":
            cmd = f"{extra_input}={extra_input2}"

        elif choice == "Print Variable":
            cmd = f'echo "${extra_input}"'

        elif choice == "Check IP Address":
            cmd = "ifconfig"

        elif choice == "Check Internet Connectivity":
            cmd = f"ping -c 4 {extra_input or 'google.com'}"

        elif choice == "Help Command":
            cmd = f"{extra_input} --help"

        elif choice == "Manual for Commands":
            cmd = f"man {extra_input}"

        elif choice == "Show Free RAM Status":
            cmd = "free -h"

        elif choice == "Show System Uptime":
            cmd = "uptime"

        elif choice == "Show Current User":
            cmd = "whoami"

        elif choice == "Show Current Logged-in Users":
            cmd = "who"

        elif choice == "Show Running Processes":
            cmd = "ps aux"

        elif choice == "Show First N Lines of a File":
            cmd = f"head -n {extra_input2} {extra_input}"

        elif choice == "Pipe Example":
            cmd = f"head -n 10 {extra_input} | grep {extra_input2}"

        elif choice == "Reboot the System":
            cmd = "sudo reboot"

        elif choice == "Redirect Output to File":
            cmd = f'echo "Hello World" > {extra_input}'

        elif choice == "Remove Directory":
            cmd = f"cd {current_path} && rmdir {extra_input}"

        elif choice == "Search Text in File":
            cmd = f"grep '{extra_input2}' {extra_input}"

        elif choice == "Search for a File":
            cmd = f"find {current_path} -name '{extra_input}'"

        elif choice == "Show Last Logins":
            cmd = "last"

        elif choice == "Show Network Statistics":
            cmd = "netstat -tuln"

        elif choice == "Show System Information":
            cmd = "uname -a"

        elif choice == "Stop Firewall":
            cmd = "sudo systemctl stop firewalld"

        elif choice == "Disk Usage":
            cmd = f"cd {current_path} && du -sh ."

        elif choice == "Monitor Real-Time Memory Usage":
            cmd = "top -n 1 -b"

        output = run_ssh_command(user, ip, cmd)
        st.text_area("📤 Command Output:", output, height=300)