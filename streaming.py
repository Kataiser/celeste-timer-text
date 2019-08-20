import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join('resources', 'python', 'packages')))
sys.path.append(os.path.abspath(os.path.join('resources', 'python')))
from bs4 import BeautifulSoup


def main():
    # comments aren't real

    if not os.path.exists('save_path.txt'):
        print("Enter path to the save file you'd like to use")
        print(r"(e.g. C:\Program Files (x86)\Steam\steamapps\common\Celeste\Saves\0.celeste):")
        save_path = input("")
        print("You can change that later by editing save_path.txt\n")

        with open('save_path.txt', 'w', encoding='utf-8') as save_path_txt:
            save_path_txt.write(save_path)
    else:
        with open('save_path.txt', 'r', encoding='utf-8') as save_path_txt:
            save_path = save_path_txt.read()

    sides = ['Normal', 'BSide', 'CSide']
    old_streaming_text = ""

    while True:
        if os.path.exists(save_path):
            with open(save_path, 'r', errors='replace') as current_save_file:
                current_save_file_read = current_save_file.read()
                
            xml_soup = BeautifulSoup(current_save_file_read, 'xml')
            current_area_id = int(xml_soup.find('LastArea').get('ID'))
            current_area_id = current_area_id if current_area_id != 8 else 7
            current_area_mode = xml_soup.find('LastArea').get('Mode')
            total_deaths = int(xml_soup.find('TotalDeaths').string)
            total_time = xml_soup.find('Time').string

            current_session = xml_soup.find('CurrentSession')
            if current_session:
                in_area = current_session.get('InArea') == 'true'
            else:
                in_area = True

            for area in xml_soup.find_all('AreaStats'):
                if area.get('ID') == str(current_area_id):
                    current_area_info = area.find_all('AreaModeStats')[sides.index(current_area_mode)]
                    current_area_deaths = int(current_area_info.get('Deaths'))
                    current_area_time = current_area_info.get('TimePlayed')

            streaming_text = f"{'This' if in_area else 'Last'} chapter: {format_timecode(current_area_time)}, {current_area_deaths} death{'s' if current_area_deaths != 1 else ''}" \
                             f"\nFile total: {format_timecode(total_time)}, {total_deaths} death{'s' if total_deaths != 1 else ''}"

            if streaming_text != old_streaming_text:
                print(streaming_text, end="\n\n")
        else:
            streaming_text = ""

        with open('timer.txt', 'w') as streaming_txt_file:
            streaming_txt_file.write(streaming_text)

        old_streaming_text = streaming_text

        time.sleep(2)


def format_timecode(timecode):
    try:
        minutes = int(int(timecode[:-7]) / 60)
        seconds = int(int(timecode[:-7]) % 60)
        ms = int(timecode[-7:-4])

        return f"{minutes}:{str(seconds).rjust(2, '0')}.{str(ms).rjust(3, '0')}"
    except ValueError:
        return '0:0.000'


if __name__ == '__main__':
    main()
