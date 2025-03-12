import ftplib
import os
import time
from datetime import datetime


def connect_ftp(host, username, password):
    ftp = ftplib.FTP(host)
    ftp.login(user=username, passwd=password)
    return ftp


def files_in(path):
    return next(os.walk(path))[2]


def check_and_upload_files(ftp, file_dict):
    need_to_upload = []
    for ftp_path, local_path in file_dict.items():
        try:
            size = ftp.size(ftp_path)
            local_size = os.path.getsize(local_path)
            if size != local_size:
                reason = f"different size (FTP: {size}, local: {local_size})"
                need_to_upload.append((ftp_path, local_path, reason))
                continue
            with open(local_path, "rb") as local_file:
                local_content = local_file.read()
            ftp_content = []
            ftp.retrbinary(f"RETR {ftp_path}", ftp_content.append)
            ftp_content = b"".join(ftp_content)
            if local_content != ftp_content:
                reason = "dirrerent content"
                need_to_upload.append((ftp_path, local_path, reason))
        except ftplib.error_perm:
            reason = "file was missing"
            need_to_upload.append((ftp_path, local_path, reason))

    for ftp_path, local_path, reason in need_to_upload:
        with open(local_path, "rb") as file:
            ftp.storbinary(f"STOR {ftp_path}", file)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Uploaded: {local_path} as {ftp_path} because {reason}")


def main():
    host = "wh23.rackhost.hu"
    username = "c25631Benke"
    password = "@SvrabcNB8kLVzn"

    local_upload_dir = "/Users/benke/Downloads/sziamuhely_wp/"
    ftp_upload_dir = "/"

    file_dict = {
        "/wp-includes/html-api/class-wp-html-processor.php": "/Users/benke/Downloads/sziamuhely_wp/wp-includes/html-api/class-wp-html-processor.php",
        "/wp-includes/html-api/class-wp-html-doctype-info.php": "/Users/benke/Downloads/sziamuhely_wp/wp-includes/html-api/class-wp-html-doctype-info.php",
        **{
            f"{ftp_upload_dir}{filename}": f"{local_upload_dir}{filename}"
            for filename in files_in(local_upload_dir)
        },
        # "/de/proba.jpg": "/Users/benke/Downloads/kepzesek.jpg",
    }

    ftp = connect_ftp(host, username, password)
    print("Connected to FTP server!")

    try:
        while True:
            check_and_upload_files(ftp, file_dict)
            time.sleep(30)  # wait for 5 minutes
    except KeyboardInterrupt:
        ftp.quit()
        print("Exited!")


if __name__ == "__main__":
    main()
