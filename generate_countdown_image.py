from PIL import ImageFont, Image, ImageDraw
from ConfigParser import SafeConfigParser
from datetime import datetime
from praw import Reddit

def send_header(img, reddit, subreddit):
    img.save("header_cd.png")
    reddit.upload_image(subreddit, "header_cd.png", name=None, header=True)

def apply_text_on_image(image, text, font_path, pos, colour):
    rgb = parse_rgb_colour(colour)
    img = Image.open(image)
    image_font = ImageFont.truetype(font_path, 25)
    draw = ImageDraw.Draw(img)
    draw.text((pos['x'], pos['y']), text, fill=(rgb['r'], rgb['g'], rgb['b']), font=image_font)
    draw = ImageDraw.Draw(img)
    return img

def remaining_time(target):
    diff = target - datetime.now()
    days = diff.days
    hours = diff.seconds // 3600
    minutes = (diff.seconds - (hours * 3600)) // 60
    seconds = (diff.seconds - (hours * 3600) - (minutes * 60))

    if seconds < 10:
        seconds = "0%s" % seconds

    if minutes < 10:
        minutes = "0%s" % minutes

    if hours < 10:
        hours = "0%s" % hours

    return {
        'seconds': seconds,
        'minutes': minutes,
        'hours': hours,
        'days': days
    }

def parse_rgb_colour(rgb_string):
    rgb_array = rgb_string.split(',')
    return {
        'r': int(rgb_array[0]),
        'g': int(rgb_array[1]),
        'b': int(rgb_array[2])
    }

def get_reddit_properties(conf):
    return {
        'username': conf.get('reddit', 'username'),
        'password': conf.get('reddit', 'password'),
        'subreddit': conf.get('reddit', 'subreddit')
    }

def get_image_properties(conf):
    return {
        'location': conf.get('image', 'image')
    }

def get_countdown_properties(conf):
    return {
        'target': conf.get('countdown', 'target'),
        'enabled': conf.get('countdown', 'enable'),
        'pos': {
            'x': int(conf.get('countdown', 'posx')),
            'y': int(conf.get('countdown', 'posy'))
        },
        'colour': conf.get('countdown', 'rgb'),
        'font': conf.get('countdown', 'font')
    }

def get_text_properties(conf):
    return {
        'text': conf.get('text', 'text'),
        'enabled': conf.get('text', 'enable'),
        'pos': {
            'x': int(conf.get('text', 'posx')),
            'y': int(conf.get('text', 'posy'))
        },
        'colour': conf.get('text', 'rgb'),
        'font': conf.get('text', 'font')
    }

def set_up_reddit(username, password):
    r = Reddit(user_agent='linux:net.dosaki.subreddit_header_countdown:0.0.2 (by /u/dosaki)')
    r.login(username, password)
    return r

def format_time_simple(timediff):
    return "%s days, %sh %sm" % (timediff['days'], timediff['hours'], timediff['minutes'])

if __name__ == '__main__':
    conf = SafeConfigParser()
    conf.read('settings.cfg')

    reddit_cfg = get_reddit_properties(conf)
    text_cfg = get_text_properties(conf)
    countdown_cfg = get_countdown_properties(conf)
    image_cfg = get_image_properties(conf)

    r = set_up_reddit(reddit_cfg['username'], reddit_cfg['password'])

    if countdown_cfg['enabled'] == "true":
        target_datetime = datetime.strptime(countdown_cfg['target'], '%Y %m %d %H:%M:%S')
        timediff = remaining_time(target_datetime)
        image = apply_text_on_image(image_cfg['location'], format_time_simple(timediff), countdown_cfg['font'], countdown_cfg['pos'], countdown_cfg['colour'])

    if text_cfg['enabled'] == "true":
        image = apply_text_on_image(image_cfg['location'], text_cfg['text'], text_cfg['font'], text_cfg['pos'], countdown_cfg['colour'])

    send_header(image, r, subreddit)
