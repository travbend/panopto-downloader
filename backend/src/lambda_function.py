import os
import ffmpeg
import requests
import subprocess
import socket
def handler(event, context):
    
    hostname = 'd2y36twrtb17ty.cloudfront.net'
    ip_address = socket.gethostbyname(hostname)
    input_url = 'https://{ip_address}:443/sessions/81a498b9-55f2-49fa-b77b-b1cb0133a245/cca0e7df-04ae-4a66-bcc5-b1cb0133a254-8a0df6b1-10f8-46f1-a3c1-b1cb013b86d3.hls/master.m3u8?InvocationID=4534a3a7-6fbe-ef11-a9f7-0a1a827ad0ec&tid=00000000-0000-0000-0000-000000000000&StreamID=5d2ec785-d06e-45f2-80eb-b1cb0133a314&ServerName=utexas.hosted.panopto.com'
    output_file = 'output.mp4'

    if os.path.exists(output_file):
        os.remove(output_file)

    try:
        result = subprocess.run(["ffmpeg", "-i", input_url, "-c", "copy", "-bsf:a", "aac_adtstoasc", output_file], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        print("STDERR:", e.stderr)

    # try:
    #     (
    #         ffmpeg
    #         .input(input_url)
    #         .output(output_file, c='copy', bsf='aac_adtstoasc')
    #         .run()
    #     )
    # except:
    #     return { "error": True }
    
    return { "error": False, "url": "Testing 123" }

