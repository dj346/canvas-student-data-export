import os
import string

# Directory in which to download course information to (will be created if not present)
DL_LOCATION = "./output"
# List of Course IDs that should be skipped (need to be integers)
COURSES_TO_SKIP = [288290, 512033]

DATE_TEMPLATE = "%B %d, %Y %I:%M %p"

class moduleItemView():
    id = 0
    
    title = ""
    content_type = ""
    
    url = ""
    external_url = ""


class moduleView():
    id = 0

    name = ""
    items = []

    def __init__(self):
        self.items = []


class pageView():
    id = 0

    title = ""
    body = ""
    created_date = ""
    last_updated_date = ""


class topicReplyView():
    id = 0

    author = ""
    posted_date = ""
    body = ""


class topicEntryView():
    id = 0

    author = ""
    posted_date = ""
    body = ""
    topic_replies = []

    def __init__(self):
        self.topic_replies = []


class discussionView():
    id = 0

    title = ""
    author = ""
    posted_date = ""
    body = ""
    topic_entries = []

    url = ""
    amount_pages = 0

    def __init__(self):
        self.topic_entries = []


class submissionView():
    id = 0

    attachments = []
    grade = ""
    raw_score = ""
    submission_comments = ""
    total_possible_points = ""
    attempt = 0
    user_id = "no-id"

    preview_url = ""
    ext_url = ""

    def __init__(self):
        self.attachments = []

class attachmentView():
    id = 0

    filename = ""
    url = ""

class assignmentView():
    id = 0

    title = ""
    description = ""
    assigned_date = ""
    due_date = ""
    submissions = []

    html_url = ""
    ext_url = ""
    updated_url = ""
    
    def __init__(self):
        self.submissions = []


class courseView():
    course_id = 0
    
    term = ""
    course_code = ""
    name = ""
    assignments = []
    announcements = []
    discussions = []
    modules = []

    def __init__(self):
        self.assignments = []
        self.announcements = []
        self.discussions = []
        self.modules = []

def makeValidFilename(input_str):
    if(not input_str):
        return input_str

    # Remove invalid characters
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    input_str = input_str.replace("+"," ") # Canvas default for spaces
    input_str = input_str.replace(":","-")
    input_str = input_str.replace("/","-")
    input_str = "".join(c for c in input_str if c in valid_chars)

    # Remove leading and trailing whitespace
    input_str = input_str.lstrip().rstrip()

    # Remove trailing periods
    input_str = input_str.rstrip(".")

    ##Splits strings to prevent extremely long names
    #input_str=input_str[:40]

    return input_str

def makeValidFolderPath(input_str):
    # Remove invalid characters
    valid_chars = "-_.()/ %s%s" % (string.ascii_letters, string.digits)
    input_str = input_str.replace("+"," ") # Canvas default for spaces
    input_str = input_str.replace(":","-")
    input_str = "".join(c for c in input_str if c in valid_chars)

    # Remove leading and trailing whitespace, separators
    input_str = input_str.lstrip().rstrip().strip("/").strip("\\")

    # Remove trailing periods
    input_str = input_str.rstrip(".")

    # Replace path separators with OS default
    input_str=input_str.replace("/",os.sep)

    ##Splits strings to prevent extremely long names
    #input_str=input_str[:40]

    return input_str