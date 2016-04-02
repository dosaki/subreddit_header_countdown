from PIL import ImageFont, Image, ImageDraw
from ConfigParser import SafeConfigParser
from datetime import datetime
from praw import Reddit

def now(fake=None):
    if fake != None:
        return datetime.strptime(fake, '%Y %m %d %H:%M:%S')
    return datetime.now()

def send_header(img):
    reddit_cfg = get_reddit_properties(conf)
    if reddit_cfg['upload'].lower() == "true":
        reddit = set_up_reddit(reddit_cfg['username'], reddit_cfg['password'])
        reddit.upload_image(reddit_cfg['subreddit'], img, name=None, header=True)
        return True
    return False

def apply_text_on_image(image, text, font_path, pos, colour):
    rgb = parse_rgb_colour(colour)
    img = Image.open(image)
    image_font = ImageFont.truetype(font_path, 25)
    draw = ImageDraw.Draw(img)
    draw.text((pos['x'],
        pos['y']), text, fill=(
            rgb['r'],
            rgb['g'],
            rgb['b']
        ), font=image_font)
    draw = ImageDraw.Draw(img)
    return img


def remaining_time(target, fake=None):
    diff = target - now(fake)
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

def force_number(string):
    try:
        return int(string)
    except:
        return 0

def parse_rgb_colour(rgb_string):
    rgb_array = rgb_string.split(',')

    return {
        'r': force_number(rgb_array[0]),
        'g': force_number(rgb_array[1]),
        'b': force_number(rgb_array[2])
    }

def get_reddit_properties(conf):
    return {
        'username': conf.get('reddit', 'username'),
        'password': conf.get('reddit', 'password'),
        'subreddit': conf.get('reddit', 'subreddit'),
        'upload': conf.get('reddit', 'upload')
    }

def get_image_properties(conf):
    return {
        'source': conf.get('image', 'source'),
        'output': conf.get('image', 'output')
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

def generate_image(input_path, text, font, pos, colour, output_path):
    image = apply_text_on_image(input_path, text, font, pos, colour)
    image.save(output_path)
    return {
        'image': image,
        'path': output_path
    }

if __name__ == '__main__':
    conf = SafeConfigParser()
    conf.read('settings.cfg')

    text_cfg = get_text_properties(conf)
    countdown_cfg = get_countdown_properties(conf)
    image_cfg = get_image_properties(conf)
    image = None

    if countdown_cfg['enabled'].lower() == "true":
        target_datetime = datetime.strptime(countdown_cfg['target'], '%Y %m %d %H:%M:%S')
        timediff = remaining_time(target_datetime)
        image = generate_image(image_cfg['source'], format_time_simple(timediff), countdown_cfg['font'], countdown_cfg['pos'], countdown_cfg['colour'], image_cfg['output'])

    if text_cfg['enabled'].lower() == "true":
        image = generate_image(image_cfg['output'], text_cfg['text'], text_cfg['font'], text_cfg['pos'], countdown_cfg['colour'], image_cfg['output'])

    if image != None:
        send_header(image['path'])
    else:
        print "Couldn't generate an image."
