# headers.py
import subprocess
import sys

def download_with_classx_headers(url, output_name=None):
    print(f"[+] ClassX Protected URL Detected!\n[+] Using Special Headers → {url[:70]}...")

    if output_name is None:
        # Smart filename banao
        filename = url.split("/")[-1].split("?")[0].split("*")[0]
        output_name = f"ClassX_{filename}"

    command = [
        "yt-dlp",
        "--referer", "https://appx-play.akamai.net.in/",
        "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
        "--add-header", "Origin:https://appx-play.akamai.net.in",
        "--add-header", "Accept:*/*",
        "--add-header", "Accept-Language:en-US,en;q=0.9",
        "-o", output_name,
        url
    ]

    try:
        subprocess.run(command, check=True)
        print(f"[✓] SUCCESS → {output_name} downloaded!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[✗] Download failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        download_with_classx_headers(sys.argv[1])
    else:
        url = input("Paste ClassX static URL: ").strip()
        download_with_classx_headers(url)
