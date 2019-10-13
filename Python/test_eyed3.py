import eyed3
import os
import sys
import re


def main():
    search_directory_set = check_path(
        'Which directory would you like to search? ')
    series_title = get_series_title('What is the name of the book? ')
    path_walked = walk_the_path(search_directory_set)
    check_tags(path_walked, series_title)
    terminate()


def ask(confirmation_prompt, default_answer_no=False):
    while True:
        answer = (input(confirmation_prompt).strip()).lower()
        if default_answer_no and answer == '' or answer.startswith('n'):
            return False
        elif answer == '' or answer.startswith('y'):
            return True
        elif answer == 'exit':
            terminate()
        else:
            print('Invalid Input: Please enter yes or no.')


def terminate():
    print('Exiting script.')
    sys.exit()


def check_path(directory_path_prompt):
    search_directory_set = set([])
    while True:
        input_directory = input(directory_path_prompt)
        if input_directory.lower() == 'exit':
            terminate()
        if (input_directory.strip()).startswith('.\\'):
            input_directory = (input_directory.strip()).replace('.\\', '', 1)
        input_directory = os.path.join((os.getcwd()), input_directory)
        if os.path.isdir(input_directory):
            search_directory_set.add(input_directory)
            if ask('Add another directory to search (y/N)? ', True):
                continue
            else:
                return search_directory_set
        else:
            print('Invalid Path: Please enter a valid directory path.')
            continue


def walk_the_path(valid_directory_set):
    path_walked = {}
    extension_list = ['mp3']
    for valid_dir in valid_directory_set:
        for root, subdirs, files in os.walk(valid_dir):
            for file in files:
                if file.endswith(tuple(extension_list)):
                    path_walked[file] = root
    if len(path_walked) == 0:
        print('No files found.')
        terminate()
    elif len(path_walked) >= 1:
        return path_walked


def get_series_title(series_title_prompt):
    series_title = input(series_title_prompt)
    series_title = series_title.strip().replace('  ', ' ')
    return series_title


def check_tags(path_walked_dictionary, series_title):
    for file, root in path_walked_dictionary.items():
        audioFile = eyed3.load(os.path.join(root, file))
        tag = audioFile.tag
        print(f'Series: {series_title}')
        print(f'Title: {tag.title}')
        print(f'Artist: {tag.artist}')
        print(f'Album Artist: {tag.album_artist}')
        print(f'Album: {tag.album}')
        print(f'Track Number: {tag.track_num}')
        print(f'Disc: {tag.disc_num}')
        if tag.disc_num:
          print('Disc is true')
        else:
          print('Disc is false')


if __name__ == '__main__':
    main()