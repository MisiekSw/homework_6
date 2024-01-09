import os
import shutil


def normalize(filename):
    filename = (
        filename.replace("ą", "a")
        .replace("ć", "c")
        .replace("ę", "e")
        .replace("ł", "l")
        .replace("ń", "n")
        .replace("ó", "o")
        .replace("ś", "s")
        .replace("ź", "z")
        .replace("ż", "z")
    )  # Zastępuje polskie znaki
    filename = "".join(
        char if char.isalnum() or char in (".", "_") else "_" for char in filename
    )
    # Pomija cyfry, zwykłe znaki, kropkę i _, a resztę zastępuje _
    return filename


def create_directory(directory):  # Tworzy folder, jeśli nie istnieje
    if not os.path.exists(directory):
        os.makedirs(directory)


def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        # Funkcja przechodzi po folder_path i tworzy 3 elementy: foldery, podfoldery i pliki
        dirs[:] = [
            d
            for d in dirs
            if d not in ("archives", "video", "audio", "documents", "images")
        ]  # Sprawdza czy podfoldery nie są w określonej liście, jeżeli nie, przypisuje je do listy

        for file in files:
            file_path = os.path.join(root, file)  # Utworzenie ścieżki do pliku
            _, file_extension = os.path.splitext(file)  # Pobranie rozszerzeń plików
            file_extension = file_extension[
                1:
            ].upper()  # Usuwa kropkę i zamienia na wielkie litery

            # Kategorie plików
            images_ext = ("JPEG", "PNG", "JPG", "SVG")
            video_ext = ("AVI", "MP4", "MOV", "MKV")
            documents_ext = ("DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX")
            music_ext = ("MP3", "OGG", "WAV", "AMR")
            archives_ext = ("ZIP", "GZ", "TAR")

            if (
                file_extension in images_ext
            ):  # Przypisuje pliki na podstawie rozszerzenia
                dest_folder = "images"
            elif file_extension in video_ext:
                dest_folder = "video"
            elif file_extension in documents_ext:
                dest_folder = "documents"
            elif file_extension in music_ext:
                dest_folder = "audio"
            elif file_extension in archives_ext:
                dest_folder = "archives"
            else:
                dest_folder = "unknown"

            normalized_name = normalize(file)
            dest_path = os.path.join(
                folder_path, dest_folder, normalized_name
            )  # Tworzy ścieżkę do folderu

            # Tworzy folder docelowy, jeżeli nie istnieje
            create_directory(os.path.dirname(dest_path))

            # Przenosi plik do odpowiedniego folderu
            shutil.move(file_path, dest_path)

    for root, dirs, files in os.walk(folder_path, topdown=False):
        # Przechodzi po folderach, podfolderach i plikach od najdalszych
        for folder in dirs:
            folder_path = os.path.join(root, folder)  # Tworzy ścieżkę do podfolderu
            if not os.listdir(folder_path):  # Sprawdza czy folder jest pusty
                os.rmdir(folder_path)  # Usuwa pusty folder


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        # Sprawdza czy komenda w terminalu ma 2 pozycje (nazwa skryptu i ścieżka do folderu), jeżeli nie, daje komunikat o poprawnej formie i wyrzuca błąd
        print("Użycie: python sort.py <ścieżka_do_folderu>")
        sys.exit(1)

    folder_to_sort = sys.argv[1]
    # Przypisanie do pozycji 2 w terminalu folderu do posortowania
    process_folder(folder_to_sort)
    print("Sortowanie zakończone pomyślnie.")

