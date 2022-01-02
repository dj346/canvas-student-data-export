from export_utils import discussionView

def getDiscussionView(discussion_topic):
    # Create discussion view
    discussion_view = discussionView()

    #ID
    discussion_view.id = discussion_topic.id if hasattr(discussion_topic, "id") else 0

    # Title
    discussion_view.title = str(discussion_topic.title) if hasattr(discussion_topic, "title") else ""
    # Author
    discussion_view.author = str(discussion_topic.user_name) if hasattr(discussion_topic, "user_name") else ""
    # Posted date
    discussion_view.posted_date = discussion_topic.created_at_date.strftime("%B %d, %Y %I:%M %p") if hasattr(discussion_topic, "created_at_date") else ""
    # Body
    discussion_view.body = str(discussion_topic.message) if hasattr(discussion_topic, "message") else ""

    # URL
    discussion_view.url = str(discussion_topic.html_url) if hasattr(discussion_topic, "html_url") else ""
    
    # Keeps track of how many topic_entries there are.
    topic_entries_counter = 0

    # Topic entries
    if hasattr(discussion_topic, "discussion_subentry_count") and discussion_topic.discussion_subentry_count > 0:
        # Need to get replies to entries recursively?

        discussion_topic_entries = discussion_topic.get_topic_entries()

        try:
            for topic_entry in discussion_topic_entries:
                topic_entries_counter += 1
                
                # Create new discussion view for the topic_entry
                topic_entry_view = topicEntryView()

                # ID
                topic_entry_view.id = topic_entry.id if hasattr(topic_entry, "id") else 0
                # Author
                topic_entry_view.author = str(topic_entry.user_name) if hasattr(topic_entry, "user_name") else ""
                # Posted date
                topic_entry_view.posted_date = topic_entry.created_at_date.strftime("%B %d, %Y %I:%M %p") if hasattr(topic_entry, "created_at_date") else ""
                # Body
                topic_entry_view.body = str(topic_entry.message) if hasattr(topic_entry, "message") else ""

                # Get this topic's replies
                topic_entry_replies = topic_entry.get_replies()

                try:
                    for topic_reply in topic_entry_replies:
                        # Create new topic reply view
                        topic_reply_view = topicReplyView()
                        
                        # ID
                        topic_reply_view.id = topic_reply.id if hasattr(topic_reply, "id") else 0

                        # Author
                        topic_reply_view.author = str(topic_reply.user_name) if hasattr(topic_reply, "user_name") else ""
                        # Posted Date
                        topic_reply_view.posted_date = topic_reply.created_at_date.strftime("%B %d, %Y %I:%M %p") if hasattr(topic_reply, "created_at_date") else ""
                        # Body
                        topic_reply_view.message = str(topic_reply.message) if hasattr(topic_reply, "message") else ""

                        topic_entry_view.topic_replies.append(topic_reply_view)
                except Exception as e:
                    print("Tried to enumerate discussion topic entry replies but received the following error:")
                    print(e)

                discussion_view.topic_entries.append(topic_entry_view)
        except Exception as e:
            print("Tried to enumerate discussion topic entries but received the following error:")
            print(e)
        
    # Amount of pages  
    discussion_view.amount_pages = int(topic_entries_counter/50) + 1 # Typically 50 topic entries are stored on a page before it creates another page.
    
    return discussion_view
    
def findCourseDiscussions(course):
    discussion_views = []

    try:
        discussion_topics = course.get_discussion_topics()

        for discussion_topic in discussion_topics:
            discussion_view = None
            discussion_view = getDiscussionView(discussion_topic)

            discussion_views.append(discussion_view)
    except Exception as e:
        print("Skipping discussion that gave the following error:")
        print(e)

    return discussion_views

def findCourseAnnouncements(course):
    announcement_views = []

    try:
        announcements = course.get_discussion_topics(only_announcements=True)

        for announcement in announcements:
            discussion_view = getDiscussionView(announcement)

            announcement_views.append(discussion_view)
    except Exception as e:
        print("Skipping announcement that gave the following error:")
        print(e)

    return announcement_views

def downloadCourseAnnouncementPages(api_url, course_view, cookies_path):
    if(cookies_path == "" or len(course_view.announcements) == 0):
        return

    base_announce_dir = os.path.join(DL_LOCATION, course_view.term,
        course_view.course_code, "announcements")

    # Create directory if not present
    if not os.path.exists(base_announce_dir):
        os.makedirs(base_announce_dir)

    announcement_list_dir = os.path.join(base_announce_dir, "announcement_list.html")
    
    # Download assignment list (theres a chance this might be the course homepage if the course has the assignments page disabled)
    if not os.path.exists(announcement_list_dir):
        download_page(api_url + "/courses/" + str(course_view.course_id) + "/announcements/", cookies_path, base_announce_dir, "announcement_list.html")

    for announcements in course_view.announcements:
        announce_dir = os.path.join(base_announce_dir, makeValidFilename(announcements.title))

        if announcements.url == "":
            continue

        if not os.path.exists(announce_dir):
            os.makedirs(announce_dir)

        # Downloads each page that a discussion takes.
        for i in range(announcements.amount_pages):
            filename = "announcement_" + str(i+1) + ".html"
            announcement_page_dir = os.path.join(announce_dir, filename)

            # Download assignment page, this usually has instructions and etc.
            if not os.path.exists(announcement_page_dir):
                download_page(announcements.url + "/page-" + str(i+1), cookies_path, announce_dir, filename)
        
def downloadCourseDicussionPages(api_url, course_view, cookies_path):
    if(cookies_path == "" or len(course_view.discussions) == 0):
        return

    base_discussion_dir = os.path.join(DL_LOCATION, course_view.term,
        course_view.course_code, "discussions")

    # Create directory if not present
    if not os.path.exists(base_discussion_dir):
        os.makedirs(base_discussion_dir)

    dicussion_list_dir = os.path.join(base_discussion_dir, "discussion_list.html")

    # Download assignment list (theres a chance this might be the course homepage if the course has the assignments page disabled)
    if not os.path.exists(dicussion_list_dir):
        download_page(api_url + "/courses/" + str(course_view.course_id) + "/discussion_topics/", cookies_path, base_discussion_dir, "discussion_list.html")

    for discussion in course_view.discussions:
        dicussion_dir = os.path.join(base_discussion_dir, makeValidFilename(discussion.title))

        if discussion.url == "":
            continue

        if not os.path.exists(dicussion_dir):
            os.makedirs(dicussion_dir)

        # Downloads each page that a discussion takes.
        for i in range(discussion.amount_pages):
            filename = "dicussion_" + str(i+1) + ".html"
            dicussion_page_dir = os.path.join(dicussion_dir, filename)
            
            # Download assignment page, this usually has instructions and etc.
            if not os.path.exists(dicussion_page_dir):
                download_page(discussion.url + "/page-" + str(i+1), cookies_path, dicussion_dir, filename)