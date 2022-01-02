def findCourseAssignments(course):
    assignment_views = []

    # Get all assignments
    assignments = course.get_assignments()
    
    try:
        for assignment in assignments:
            # Create a new assignment view
            assignment_view = assignmentView()

            #ID
            assignment_view.id = assignment.id if \
                hasattr(assignment, "id") else ""

            # Title
            assignment_view.title = makeValidFilename(str(assignment.name)) if \
                hasattr(assignment, "name") else ""
            # Description
            assignment_view.description = str(assignment.description) if \
                hasattr(assignment, "description") else ""
            
            # Assigned date
            assignment_view.assigned_date = assignment.created_at_date.strftime(DATE_TEMPLATE) if \
                hasattr(assignment, "created_at_date") else ""
            # Due date
            assignment_view.due_date = assignment.due_at_date.strftime(DATE_TEMPLATE) if \
                hasattr(assignment, "due_at_date") else ""    

            # HTML Url
            assignment_view.html_url = assignment.html_url if \
                hasattr(assignment, "html_url") else ""   
            # External URL
            assignment_view.ext_url = str(assignment.url) if \
                hasattr(assignment, "url") else ""
            # Other URL (more up-to-date)
            assignment_view.updated_url = str(assignment.submissions_download_url).split("submissions?")[0] if \
                hasattr(assignment, "submissions_download_url") else ""

            try:
                try: # Download all submissions for entire class
                    submissions = assignment.get_submissions()
                    submissions[0] # Trigger Unauthorized if not allowed
                except Unauthorized:
                    print("Not authorized to download entire class submissions for this assignment")
                    # Download submission for this user only
                    submissions = [assignment.get_submission(USER_ID, include=["submission_comments", "submission_history"] )]
                submissions[0] #throw error if no submissions found at all but without error
            except (ResourceDoesNotExist, NameError, IndexError):
                print('Got no submissions from either class or user: {}'.format(USER_ID))
            except Exception as e:
                print("Failed to retrieve submissions for this assignment")
                print(e.__class__.__name__)
            else:
                try:
                    for submission in submissions:

                        sub_view = submissionView()

                        # Submission ID
                        sub_view.id = submission.id if \
                            hasattr(submission, "id") else 0
                            
                        # My grade
                        sub_view.grade = str(submission.grade) if \
                            hasattr(submission, "grade") else ""
                        # My raw score
                        sub_view.raw_score = str(submission.score) if \
                            hasattr(submission, "score") else ""
                        # Total possible score
                        sub_view.total_possible_points = str(assignment.points_possible) if \
                            hasattr(assignment, "points_possible") else ""
                        # Submission comments
                        sub_view.submission_comments = str(submission.submission_comments) if \
                            hasattr(submission, "submission_comments") else ""
                        # Attempt
                        sub_view.attempt = submission.attempt if \
                            hasattr(submission, "attempt") else 0
                        # User ID
                        sub_view.user_id = str(submission.user_id) if \
                            hasattr(submission, "user_id") else ""
                        
                        # Submission URL
                        sub_view.preview_url = str(submission.preview_url) if \
                            hasattr(submission, "preview_url") else ""
                        #   External URL
                        sub_view.ext_url = str(submission.url) if \
                            hasattr(submission, "url") else ""

                        try:
                            submission.attachments
                        except AttributeError:
                            print('No attachments')
                        else:
                            for attachment in submission.attachments:
                                attach_view = attachmentView()
                                attach_view.url = attachment["url"]
                                attach_view.id = attachment["id"]
                                attach_view.filename = attachment["filename"]
                                sub_view.attachments.append(attach_view)
                        assignment_view.submissions.append(sub_view)
                except Exception as e:
                    print("Skipping submission that gave the following error:")
                    print(e)

            assignment_views.append(assignment_view)
    except Exception as e:
        print("Skipping course assignments that gave the following error:")
        print(e)

    return assignment_views

def downloadAssignmentPages(api_url, course_view, cookies_path):
    if(cookies_path == "" or len(course_view.assignments) == 0):
        return

    base_assign_dir = os.path.join(DL_LOCATION, course_view.term,
        course_view.course_code, "assignments")

    # Create directory if not present
    if not os.path.exists(base_assign_dir):
        os.makedirs(base_assign_dir)

    assignment_list_path = os.path.join(base_assign_dir, "assignment_list.html")

    # Download assignment list (theres a chance this might be the course homepage if the course has the assignments page disabled)
    if not os.path.exists(assignment_list_path):
        download_page(api_url + "/courses/" + str(course_view.course_id) + "/assignments/", cookies_path, base_assign_dir, "assignment_list.html")

    for assignment in course_view.assignments:     
        assign_dir = os.path.join(base_assign_dir, makeValidFilename(assignment.title))

        # Download an html image of each assignment (includes assignment instructions and other stuff). 
        # Currently, this will only download the main assignment page and not external pages, this is
        # because these external pages are given in a json format. Saving these would require a lot
        # more work then normal.
        if assignment.html_url != "":
            if not os.path.exists(assign_dir):
                os.makedirs(assign_dir)

            assignment_page_path = os.path.join(assign_dir, "assignment.html")

            # Download assignment page, this usually has instructions and etc.
            if not os.path.exists(assignment_page_path):
                download_page(assignment.html_url, cookies_path, assign_dir, "assignment.html")

        for submission in assignment.submissions:
            submission_dir = assign_dir

            # If theres more then 1 submission, add unique id to download dir
            if len(assignment.submissions) != 1:
                submission_dir = os.path.join(assign_dir, str(submission.user_id))

            if submission.preview_url != "":
                if not os.path.exists(submission_dir):
                    os.makedirs(submission_dir)

                submission_page_dir = os.path.join(submission_dir, "submission.html")

                # Download submission url, this is typically a more focused page
                if not os.path.exists(submission_page_dir):
                    download_page(submission.preview_url, cookies_path, submission_dir, "submission.html")    

            # If theres more then 1 attempt, save each attempt in attempts folder
            if (submission.attempt != 1 and assignment.updated_url != "" and assignment.html_url != "" 
                and assignment.html_url.rstrip("/") != assignment.updated_url.rstrip("/")):
                submission_dir = os.path.join(assign_dir, "attempts")
                
                if not os.path.exists(submission_dir):
                    os.makedirs(submission_dir)

                # Saves the attempts if multiple were taken, doesn't account for
                # different ID's however, as I wasnt able to find out what the url 
                # for the specific id's attempts would be. 
                for i in range(submission.attempt):
                    filename = "attempt_" + str(i+1) + ".html"
                    submission_page_attempt_dir = os.path.join(submission_dir, filename)

                    if not os.path.exists(submission_page_attempt_dir):
                        download_page(assignment.updated_url + "/history?version=" + str(i+1), cookies_path, submission_dir, filename)
