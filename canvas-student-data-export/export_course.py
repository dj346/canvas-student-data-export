def downloadCourseFiles(course, course_view):
    # file full_name starts with "course files"
    dl_dir = os.path.join(DL_LOCATION, course_view.term,
                          course_view.course_code)

    # Create directory if not present
    if not os.path.exists(dl_dir):
        os.makedirs(dl_dir)

    try:
        files = course.get_files()

        for file in files:
            file_folder=course.get_folder(file.folder_id)
            
            folder_dl_dir=os.path.join(dl_dir, makeValidFilename(file_folder.full_name))
            
            if not os.path.exists(folder_dl_dir):
                os.makedirs(folder_dl_dir)
        
            dl_path = os.path.join(folder_dl_dir, makeValidFilename(str(file.display_name)))

            # Download file if it doesn't already exist
            if not os.path.exists(dl_path):
                print('Downloading: {}'.format(dl_path))
                file.download(dl_path)
    except Exception as e:
        print("Skipping file download that gave the following error:")
        print(e)

def getCourseView(course):
    course_view = courseView()

    # Course ID
    course_view.course_id = course.id if hasattr(course, "id") else 0

    # Course term
    course_view.term = makeValidFilename(course.term["name"] if hasattr(course, "term") and "name" in course.term.keys() else "")

    # Course code
    course_view.course_code = makeValidFilename(course.course_code if hasattr(course, "course_code") else "")

    # Course name
    course_view.name = course.name if hasattr(course, "name") else ""

    print("Working on " + course_view.term + ": " + course_view.name)

    # Course assignments
    print("  Getting assignments")
    course_view.assignments = findCourseAssignments(course)

    # Course announcements
    print("  Getting announcements")
    course_view.announcements = findCourseAnnouncements(course)

    # Course discussions
    print("  Getting discussions")
    course_view.discussions = findCourseDiscussions(course)

    # Course pages
    print("  Getting pages")
    course_view.pages = findCoursePages(course)

    #https://4cd.instructure.com/api/v1/courses/68029/enrollments
    #https://4cd.instructure.com/api/v1/courses/68029/quizzes
    #https://4cd.instructure.com/api/v1/courses/68029/tabs
    #https://4cd.instructure.com/api/v1/courses/68029/users

    return course_view

def exportAllCourseData(course_view):
    json_str = json.dumps(json.loads(jsonpickle.encode(course_view, unpicklable = False)), indent = 4)

    course_output_dir = os.path.join(DL_LOCATION, course_view.term,
                                     course_view.course_code)

    # Create directory if not present
    if not os.path.exists(course_output_dir):
        os.makedirs(course_output_dir)

    course_output_path = os.path.join(course_output_dir,
                                      course_view.course_code + ".json")

    with open(course_output_path, "w") as out_file:
        out_file.write(json_str)

def downloadCourseHTML(api_url, cookies_path):
    if(cookies_path == ""):
        return

    course_dir = DL_LOCATION

    if not os.path.exists(course_dir):
        os.makedirs(course_dir)

    course_list_path = os.path.join(course_dir, "course_list.html")

    # Downloads the course list.
    if not os.path.exists(course_list_path):
        download_page(api_url + "/courses/", cookies_path, course_dir, "course_list.html")

def downloadCourseHomePageHTML(api_url, course_view, cookies_path):
    if(cookies_path == ""):
        return

    dl_dir = os.path.join(DL_LOCATION, course_view.term,
                         course_view.course_code)

    # Create directory if not present
    if not os.path.exists(dl_dir):
        os.makedirs(dl_dir)

    homepage_path = os.path.join(dl_dir, "homepage.html")

    # Downloads the course home page.
    if not os.path.exists(homepage_path):
        download_page(api_url + "/courses/" + str(course_view.course_id), cookies_path, dl_dir, "homepage.html")