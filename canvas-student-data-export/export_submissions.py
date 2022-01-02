import os
import requests

from export_utils import DL_LOCATION, makeValidFilename

def download_submission_attachments(course, course_view):
    course_dir = os.path.join(DL_LOCATION, course_view.term,
                              course_view.course_code)

    # Create directory if not present
    if not os.path.exists(course_dir):
        os.makedirs(course_dir)

    for assignment in course_view.assignments:
        for submission in assignment.submissions:
            attachment_dir = os.path.join(course_dir, "assignments", assignment.title)
            if(len(assignment.submissions)!=1):
                attachment_dir = os.path.join(attachment_dir,str(submission.user_id))
            if (not os.path.exists(attachment_dir)) and (submission.attachments):
                os.makedirs(attachment_dir)
            for attachment in submission.attachments:
                filepath = os.path.join(attachment_dir, makeValidFilename(str(attachment.id) +
                                        "_" + attachment.filename))
                if not os.path.exists(filepath):
                    print('Downloading attachment: {}'.format(filepath))
                    r = requests.get(attachment.url, allow_redirects=True)
                    with open(filepath, 'wb') as f:
                        f.write(r.content)
                else:
                    print('File already exists: {}'.format(filepath))
