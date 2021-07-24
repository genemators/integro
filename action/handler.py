import json
import os
import controller.channels
import util


async def main():
    if not os.path.isdir('JSON'):
        util.log('warn', 'Seems like a folder for JSON outputs does not exist. Let me create it for you...')
        os.mkdir('JSON')
        pass

    if not os.path.isfile('channels.txt'):
        controller.channels.main()

    with open('channels.txt') as f:
        channels = f.readlines()

    #
    # All links in channels.txt should be seperated by a new line
    # Expected parsed file results:
    # [ 'https://t.me/example', 'https://t.me/example' ]
    #

    name = "unified_file"
    posts = {}
    
    with open("translator.json", "r", encoding="UTF-8") as file:
        translator = json.load(file)
    
    for i, channel in enumerate(channels):
        try:
            async for message in util.client.iter_messages(channel, limit=2):
                message_text = message.text
                message_text_new = ""
                for char in message_text:
                    if char in translator:
                        message_text_new += translator[char]
                    else:
                        message_text_new += char
                                     
                message_id = str(i) + "-" + message.id
                posts[message_id] = message_text_new
        except Exception as excp:
            util.log('error', f"Cannot find any entity corresponding to {channel}.")
    
    # creating JSON folder for each kind of data type
    try:
        os.chdir('JSON')
        with open(f"{name}.json", "w", encoding="UTF-8") as json_file:
            json_file.write(json.dumps(posts, indent=4, sort_keys=True))

        util.log('success', f"The JSON file has been created successfully for {name} channel")
        os.chdir('..')
    except Exception as error:
        util.log('error', f"Could not create the JSON file of {name} channel: ")



