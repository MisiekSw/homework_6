import shutil
from pathlib import Path


def normalize(letter):
    letter = (
        letter.replace("ą", "a")
        .replace("ć", "c")
        .replace("ę", "e")
        .replace("ł", "l")
        .replace("ń", "n")
        .replace("ó", "o")
        .replace("ś", "s")
        .replace("ź", "z")
        .replace("ż", "z")
    )
    letter = "".join(
        sign if sign.isalnum() or sign in (".", "_") else "_" for sign in letter
    )

    return letter


def subfolders(folders):
    images_folder = Path(folders) / "images"
    videos_folder = Path(folders) / "videos"
    documents_folder = Path(folders) / "documents"
    audio_folder = Path(folders) / "audio"
    archives_folder = Path(folders) / "archives"

    for folder in (
        images_folder,
        videos_folder,
        documents_folder,
        audio_folder,
        archives_folder,
    ):
        try:
            folder.mkdir()
        except FileExistsError:
            pass


def sorting(path):
    subfolders(path)
    unknown = set()

    for file_path in Path(path).rglob("*.*"):
        extension = file_path.suffix[1:].upper()

        if file_path.is_dir() or not extension:
            continue

        unknown.add(extension)

        if extension in ("JPEG", "PNG", "JPG", "SVG"):
            shutil.move(file_path, Path(path) / "images" / normalize(file_path.name))
        elif extension in ("AVI", "MP4", "MOV", "MKV"):
            shutil.move(file_path, Path(path) / "videos" / normalize(file_path.name))
        elif extension in ("DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX"):
            shutil.move(file_path, Path(path) / "documents" / normalize(file_path.name))
        elif extension in ("MP3", "OGG", "WAV", "AMR"):
            shutil.move(file_path, Path(path) / "audio" / normalize(file_path.name))
        elif extension in ("ZIP", "GZ", "TAR"):
            archives = Path(path) / "archives" / normalize(file_path.stem)

            try:
                archives.mkdir()
                shutil.unpack_archive(file_path, archives)
                file_path.unlink()
            except FileExistsError:
                pass
        else:
            pass
    return unknown
