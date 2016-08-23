#!/usr/bin/env python

'''Slack Dataset Reader

This python script will read the JSON files. 
The JSON files pose three unique problems. 
First of all, most people don't have the right programs to read JSON files. 
Second, even if you open the JSON files with notepad, because ICISTS uses
Korean as its inner communication language, the JSON files are exported with
unicode. This is completely unreadable to the ordinary user. 
Third, the usernames are encoded in a strange way. Thus in the messages,
it is difficult to check who actually sent the messages. 

This script will solve all of the above problems whiz-bang. To run it, 
place the file next to the directory containing the json files, and run
python archive-reader.py on the command line. It will print a list of all
channels, then print --Script over-- when finished. 

After running this script, look to (data-directory)/parsed/for the 
results. to change this, change the desig_path variable in the Paths 
global variable area to wherever you want.
If you don't have the parsed directory, the script will give an error;
in this case the problem will be solved by making the directory in the
desired place. 
The script uses current directory as a starting point, so you should run
it accordingly.  

Got any questions? Contact 010-2972-7927 for the creator.

Oh, and by the way, while I think this is improbable, running the code 
at somewhere that is not Korea may not get correct time. '''

## Modules
import json # needed to understand all the json files simply
import time # needed to convert the UNIX time to readable time
import os   # needed to read the file lists and make directories

## Paths
dat_path = 'SlackDat-toJune05/'
desig_path = dat_path + 'parsed/'

## Functions
def user_dat():
    '''This function gathers the user data from the folder's "users.json"
    file, and returns list of user dictionaries. '''
    f = open(dat_path + 'users.json')
    json_content = f.read()
    return json.loads(json_content)

def user_hash(user_list):
    '''Takes the user data list and returns a dictionary that connects
    the user id and real name.'''
    return { usr['id'] : usr['real_name'] for usr in user_list 
             if usr['name'] != 'subcurrent'}

def single_file_decoder(file_path, filehandle, user_decoder):
    '''decodes a single json file to a readable format. 
    
    takes input the file's path from the dat_path. for example, if 
    one were trying to access the 2016-03-09 entry of the 
    timetable-tf channel, the input would be 'timetable-tf/2016-03-09.json'
    also takes the filehandle to which the program should be writing to. 
    in the above example, an appropreate filehandle would be a filehandle 
    pointing to something like timetable-tf.txt .
    
    the output will be like the follows: 
    -----YYYY DDD MMM DD-----
    [username1][HH:MM] message
    [username2][HH:MM] message
    which is very similar to the format KakaoTalk exports take. '''
    f = open(dat_path + file_path)
    json_content = f.read()
    decode_content = json.loads(json_content)
    filehandle.write('-----%s-----\n' %
                     (time.asctime(
                         time.localtime(float(decode_content[0]['ts']))
                         )[20:] + ' ' + \
                     time.asctime(
                         time.localtime(float(decode_content[0]['ts']))
                         )[:10])
                     )

    for message in decode_content:
        try:
            basic_string = ''
            basic_string += '[%s]' % user_decoder[message['user']]
            basic_string += '[%s]' % time.asctime(
                time.localtime(float(message['ts']))
                )[11:19]
            msg = message['text']
            for key in user_decoder.keys():
                if '@' + key in msg:
                    pass
                msg = msg.replace('@' + key, user_decoder[key].decode('utf-8'))
            basic_string += msg
            filehandle.write(basic_string.encode('utf-8') + '\n')
        except KeyError:
            continue

def channel_decoder(chan_path, user_decoder, new_place = None):
    '''Decodes an entire channel(directory). 
    
    Takes chan_path as input. chan_path takes two roles in this function:
    giving a name to the output text file and designating where to find
    the json files. chan_path should be a single channel name, like 
    "timetable-tf/". 
    user_decoder is needed to dispatch the single_file_decoder stuff. 
    When new_place is None, the text file will just be saved within the 
    channel directory. To do otherwise, one should designate a new directory.
    If the directory does not exist, this function will cause an error.
    
    Will make a text file bearing the name of file_path(without the slash)'''
    full_path = dat_path + chan_path
    if new_place:
        channel_handle = open(new_place + chan_path[:-1] + '.txt', 'w')
    else:
        channel_handle = open(full_path + chan_path[:-1] + '.txt', 'w')
    
    for json_file in os.listdir(full_path):
        if not '.json' in json_file:
            continue
        else:
            single_file_decoder(chan_path + json_file, channel_handle, 
                                user_decoder)
    channel_handle.close()

def main():
    '''collects all the data and puts in into the desig_path directory.
    takes no input or output.'''
    
    print os.listdir(dat_path)
    
    user_list = user_dat()
    user_decoder = user_hash(user_list)
    
    for direc in os.listdir(dat_path):
        if '.' in direc:
            continue
        channel_decoder(direc + '/', user_decoder, new_place = desig_path)
    print '--Script over--'

if __name__ == '__main__':
    main()