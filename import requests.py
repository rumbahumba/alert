import requests
import os
import m3u8
import subprocess

# Yeh headers wahi hain jo browser ne bheje the
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
    "Origin": "https://appx-play.akamai.net.in",
    "Referer": "https://appx-play.akamai.net.in/",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br, zstd"
}

def download_video(m3u8_url, output_file="output.mp4"):
    # Step 1: Fetch playlist
    print("[*] Fetching playlist...")
    m3u8_obj = m3u8.load(m3u8_url, headers=headers)

    # Step 2: Collect segment URLs
    base_url = m3u8_url.rsplit("/", 1)[0] + "/"
    segment_urls = [seg.uri if seg.uri.startswith("http") else base_url + seg.uri for seg in m3u8_obj.segments]
    print(f"[*] Found {len(segment_urls)} segments.")

    os.makedirs("segments", exist_ok=True)
    ts_files = []

    # Step 3: Download segments
    for i, url in enumerate(segment_urls):
        ts_file = f"segments/{i}.ts"
        ts_files.append(ts_file)

        if not os.path.exists(ts_file) or os.path.getsize(ts_file) == 0:
            print(f"Downloading {i+1}/{len(segment_urls)} ...")
            r = requests.get(url, headers=headers, stream=True)
            if r.status_code == 200:
                with open(ts_file, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024*1024):
                        f.write(chunk)
            else:
                print(f"[!] Failed to download {i+1}, status {r.status_code}")

    # Step 4: Merge into mp4 using ffmpeg
    print("[*] Merging into MP4...")
    with open("segments/files.txt", "w", encoding="utf-8") as f:
        for ts in ts_files:
            f.write(f"file '{os.path.abspath(ts)}'\n")

    subprocess.run([
        "ffmpeg", "-f", "concat", "-safe", "0", "-i",
        "segments/files.txt", "-c", "copy", output_file
    ])

    print(f"[*] Done! Saved as {output_file}")


if __name__ == "__main__":
    m3u8_url = "https://transcoded-videos.classx.co.in/videos/neetkakajee-data/2501380-1757319951/hls-f82d14/480p/master-3556399.922749027.m3u8?edge-cache-token=URLPrefix=aHR0cHM6Ly90cmFuc2NvZGVkLXZpZGVvcy5jbGFzc3guY28uaW4vdmlkZW9zL25lZXRrYWthamVlLWRhdGEvMjUwMTM4MC0xNzU3MzE5OTUxL2hscy1mODJkMTQ~Expires=1757341187~Signature=37BshrWZxFuPXqipMooRg1K3_ExQiSggzXqfRdDgKINSvQzrYtnZ7rIpuKQXRG0Ttq8TmbWkWfVo0hmQSvg0Bg"
    download_video(m3u8_url, "final_video.mp4")
