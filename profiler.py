from instaloader.exceptions import ProfileNotExistsException
from itertools import islice
import pandas as pd
import instaloader
# import random
import json
import time
import re


# mask my ip 
# def get_random_proxy():
#     with open('proxies.json', 'r') as f:
#         proxies = json.load(f)
#     proxy = random.choice(proxies)
#     port = proxy['port']
#     ip = proxy['ip']
#     print(f"Your proxy is IP:{ip} and your PORT:{port}")
#     return proxy, ip, port

# Read urls.csv 

def read_csv():
    with open('data/urls.csv', 'r') as f:
        urls_df = pd.read_csv(f)
        
        # filter rows where 'URL' is 'USER URL'
        urls_df = urls_df[urls_df['Type'] == 'USER URL']
    return urls_df

usernames = []

# Extracting usernames

def parse_usernames(urls):
    pattern = r"https://www\.instagram\.com/([^/?#&]+)"
    usernames = []  # Initialize usernames list here to ensure it's local to the function

    for url in urls:
        match = re.search(pattern, url)
        if match:
            username = match.group(1)  # The captured username
            usernames.append(username)

    # print each username with index enumerate
    for i, username in enumerate(usernames):
        print(f"{i+1}. {username}")

    return usernames

loader = instaloader.Instaloader()

# Login to Instagram
try:
    loader.login('inkerscraper', 'inkertattoo')  # Your Instagram credentials
  #  loader.load_session_from_file('inkerscraper')
except Exception as e:
    print(f"An error occurred while logging in: {e}")
    

def download_profile_data(usernames, loader):
    users = []  # Initialize the list to ensure it's always a list
    for username in usernames:
        try:
            profile = instaloader.Profile.from_username(loader.context, username)
            user_data = {
                'name': profile.full_name,
                'username': username,
                'followers': profile.followers,
                'followees': profile.followees,
                'bio': profile.biography,
                'posts': profile.mediacount,
                'url': f"https://www.instagram.com/{profile.username}/",
                'profile_pic_url': profile.profile_pic_url
            }
            users.append(user_data)
        except ProfileNotExistsException:
            print(f"Profile {username} does not exist or is not accessible.")
        except Exception as e:
            print(f"An error occurred with {username}: {e}")
    return users 

# save users in json file
def save_users(users, filepath='data/users.json'):
    with open(filepath, 'w') as f:
        json.dump(users, f, indent=4)
        
    # return users.json file
    return filepath

# Downloading profile media
def download_profile_media(loader, usernames, filepath):
    media_data = []  # Outer list holding media data for all users

    for username in usernames:
        profile_media_data = [{'username': username}]  # Start with username

        try:
            profile = instaloader.Profile.from_username(loader.context, username)
            # print X if succeeded loading and Y else failed loading
            print(f"Profile Loaded: {username} with great success --- very nice i like")
            
            # if profile is not None than run loop
            if profile is not None:
                for post in profile.get_posts():
                    loader.download_post(post, target=username)  # Optional: remove if only metadata is needed
                    # print if succeed downloading post
                    print(f"Post downloaded: {post.caption}, from user: {username} -- very nice")
                    
                    post_metadata = {
                        # 'date_utc': post.date_utc.isoformat(),  # Uncomment if date in ISO format is needed
                        'date_utc': str(post.date_utc),
                        'url': post.url,
                        'caption': post.caption if post.caption else "",
                        'likes': post.likes,
                        'comments': post.comments,
                        'is_video': post.is_video,
                        'video_url': post.video_url if post.is_video else None
                    }

                    profile_media_data.append(post_metadata)  # Append each post's metadata to the user's list
                # time sleep for 10 seconds
                time.sleep(10)
                print("Now recharging for 10 secs.... you can power nap for a bit...")

        except ProfileNotExistsException:
            print(f"Profile {username} does not exist or is not accessible.")
            continue  # Skip to next username
        except Exception as e:
            print(f"An error occurred with {username}: {e}")
            continue

        media_data.append(profile_media_data)  # Append the user's list to the outer list

    # Saving each user's media data into separate JSON files
    for user_media in media_data:
        username = user_media[0]['username']
        with open(f'data/{username}.json', 'w') as f:
            json.dump(user_media, f, indent=4)

    return media_data


    

# # run all functions, add new functions to main
def main():
    # get_random_proxy()
    # print("Random Proxy Generated")
    urls_df = read_csv()
    print("URLS csv filtered with users only")
    urls = urls_df['URL']
    
    usernames = parse_usernames(urls)
    print("Usernames parsed form URLs")
    
    user_data = download_profile_data(usernames[1:2], loader)
    user_data = [user for user in user_data if user]  # Filter out None values
    print("Downloading user data from Instagram")
    
    filepath = save_users(user_data)
    print("User data saved in users.json")
    
    media_data = download_profile_media(loader, usernames[1:2])
    print("Retrieving all profile's media data")
    

# #run main function without calling main
if __name__ == "__main__":
    main()



        
# import subprocess

# def download_instagram_profile(target_username):
#     username = 'inkerscraper'  # Your Instagram username for login
#     password = 'inkertattoo'  # Your Instagram password

#     # Login to Instaloader and save the session file
#     login_command = f'instaloader --login={username} --sessionfile=my_session'
#     subprocess.run(login_command, shell=True, input=password, text=True, capture_output=True)
    
#     # Use the session file to download the target profile without needing to login again
#     download_command = f'instaloader --sessionfile=my_session {target_username}'
#     subprocess.run(download_command, shell=True)