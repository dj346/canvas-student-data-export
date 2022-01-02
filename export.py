# built in
import json
import os

# external
from canvasapi import Canvas
from canvasapi.exceptions import ResourceDoesNotExist, Unauthorized

from singlefile import download_page

import jsonpickle
import yaml

try:
    with open("credentials.yaml", 'r') as f:
        credentials = yaml.full_load(f)
except OSError:
    # Canvas API URL
    API_URL = ""
    # Canvas API key
    API_KEY = ""
    # My Canvas User ID
    USER_ID = 0000000
    # Browser Cookies File
    COOKIES_PATH = ""
else:
    API_URL = credentials["API_URL"]
    API_KEY = credentials["API_KEY"]
    USER_ID = credentials["USER_ID"]
    COOKIES_PATH = credentials["COOKIES_PATH"]

if __name__ == "__main__":

    print("Welcome to the Canvas Student Data Export Tool\n")

    if API_URL == "":
        # Canvas API URL
        print("We will need your organization's Canvas Base URL. This is "
              "probably something like https://{schoolName}.instructure.com)")
        API_URL = input("Enter your organization's Canvas Base URL: ")

    if API_KEY == "":
        # Canvas API key
        print("\nWe will need a valid API key for your user. You can generate "
              "one in Canvas once you are logged in.")
        API_KEY = input("Enter a valid API key for your user: ")

    if USER_ID == 0000000:
        # My Canvas User ID
        print("\nWe will need your Canvas User ID. You can find this by "
              "logging in to canvas and then going to this URL in the same "
              "browser {yourCanvasBaseUrl}/api/v1/users/self")
        USER_ID = input("Enter your Canvas User ID: ")
    
    if COOKIES_PATH == "": 
        # Cookies path
        print("\nWe will need your browsers cookies file. This needs to be "
              "exported using another tool. This needs to be a path to a file "
              "formatted in the NetScape format. This can be left blank if an html "
              "images aren't wanted. ")
        COOKIES_PATH = input("Enter your cookies path: ")

    print("\nConnecting to canvas\n")

    # Initialize a new Canvas object
    canvas = Canvas(API_URL, API_KEY)

    print("Creating output directory: " + DL_LOCATION + "\n")
    # Create directory if not present
    if not os.path.exists(DL_LOCATION):
        os.makedirs(DL_LOCATION)

    all_courses_views = []

    print("Getting list of all courses\n")
    courses = canvas.get_courses(include="term")

    skip = set(COURSES_TO_SKIP)


    if (COOKIES_PATH):
        print("  Downloading course list page")
        downloadCourseHTML(API_URL, COOKIES_PATH)

    for course in courses:
        if course.id in skip or not hasattr(course, "name") or not hasattr(course, "term"):
            continue

        if not course.id == 68029:
            continue

        course_view = getCourseView(course)

        all_courses_views.append(course_view)

        print("  Downloading all files")
        #downloadCourseFiles(course, course_view)

        print("  Downloading submission attachments")
        #download_submission_attachments(course, course_view)

        print("  Getting modules and downloading module files")
        #course_view.modules = findCourseModules(course, course_view)

        if(COOKIES_PATH):
            print("  Downloading course home page")
            #downloadCourseHomePageHTML(API_URL, course_view, COOKIES_PATH)

            print("  Downloading assignment pages")
            #downloadAssignmentPages(API_URL, course_view, COOKIES_PATH)

            print("  Downloading course module pages")
            #downloadCourseModulePages(API_URL, course_view, COOKIES_PATH)

            print("  Downloading course announcements pages")
            #downloadCourseAnnouncementPages(API_URL, course_view, COOKIES_PATH)   

            print("  Downloading course dicussion pages")
            #downloadCourseDicussionPages(API_URL, course_view, COOKIES_PATH)

        print("  Exporting all course data")
        #exportAllCourseData(course_view)

    print("Exporting data from all courses combined as one file: "
          "all_output.json")
    # Awful hack to make the JSON pretty. Decode it with Python stdlib json
    # module then re-encode with indentation
    json_str = json.dumps(json.loads(jsonpickle.encode(all_courses_views,
                                                       unpicklable=False)),
                          indent=4)

    all_output_path = os.path.join(DL_LOCATION, "all_output.json")

    with open(all_output_path, "w") as out_file:
        out_file.write(json_str)

    print("\nProcess complete. All canvas data exported!")
