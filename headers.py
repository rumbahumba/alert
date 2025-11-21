import subprocess
def download_with_headers(url):
    cmd = [
        "yt-dlp",
        "--add-header", "Referer: https://appx-play.akamai.net.in/",
        "--add-header", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        url
    ]
    try:
        subprocess.run(cmd, check=True)
        print("Download completed!")
    except subprocess.CalledProcessError as e:
        print(f"Download failed: {e}")
if __name__ == "__main__":
    input_url = input("Enter the video URL to download: ").strip()
    download_with_headers(input_url)
