def findCourseModules(course, course_view):
    modules_dir = os.path.join(DL_LOCATION, course_view.term,
                               course_view.course_code, "modules")

    # Create modules directory if not present
    if not os.path.exists(modules_dir):
        os.makedirs(modules_dir)

    module_views = []

    try:
        modules = course.get_modules()

        for module in modules:
            module_view = moduleView()

            # ID
            module_view.id = module.id if hasattr(module, "id") else ""

            # Name
            module_view.name = str(module.name) if hasattr(module, "name") else ""

            try:
                # Get module items
                module_items = module.get_module_items()

                for module_item in module_items:
                    module_item_view = moduleItemView()

                    # ID
                    module_item_view.id = module_item.id if hasattr(module_item, "id") else 0

                    # Title
                    module_item_view.title = str(module_item.title) if hasattr(module_item, "title") else ""
                    # Type
                    module_item_view.content_type = str(module_item.type) if hasattr(module_item, "type") else ""

                    # URL
                    module_item_view.url = str(module_item.html_url) if hasattr(module_item, "html_url") else ""
                    # External URL
                    module_item_view.external_url = str(module_item.external_url) if hasattr(module_item, "external_url") else ""

                    if module_item_view.content_type == "File":
                        # If problems arise due to long pathnames, changing module.name to module.id might help
                        # A change would also have to be made in downloadCourseModulePages(api_url, course_view, cookies_path)
                        module_dir = os.path.join(modules_dir, makeValidFilename(str(module.id)), "files") 

                        try:
                            # Create directory for current module if not present
                            if not os.path.exists(module_dir):
                                os.makedirs(module_dir)

                            # Get the file object
                            module_file = course.get_file(str(module_item.content_id))

                            # Create path for module file download
                            module_file_path = os.path.join(module_dir, makeValidFilename(str(module_file.display_name)))

                            # Download file if it doesn't already exist
                            if not os.path.exists(module_file_path):
                                module_file.download(module_file_path)
                        except Exception as e:
                            print("Skipping module file download that gave the following error:")
                            print(e)

                    module_view.items.append(module_item_view)
            except Exception as e:
                print("Skipping module item that gave the following error:")
                print(e)

            module_views.append(module_view)

    except Exception as e:
        print("Skipping entire module that gave the following error:")
        print(e)

    return module_views

def downloadCourseModulePages(api_url, course_view, cookies_path): 
    if(cookies_path == "" or len(course_view.modules) == 0):
        return

    modules_dir = os.path.join(DL_LOCATION, course_view.term,
        course_view.course_code, "modules")

    # Create modules directory if not present
    if not os.path.exists(modules_dir):
        os.makedirs(modules_dir)

    module_list_dir = os.path.join(modules_dir, "modules_list.html")

    # Downloads the modules page (possible this is disabled by the teacher)
    if not os.path.exists(module_list_dir):
        download_page(api_url + "/courses/" + str(course_view.course_id) + "/modules/", COOKIES_PATH, modules_dir, "modules_list.html")

    for module in course_view.modules:
        for item in module.items:
            # If problems arise due to long pathnames, changing module.name to module.id might help, this can also be done with item.title
            # A change would also have to be made in findCourseModules(course, course_view)
            items_dir = os.path.join(modules_dir, makeValidFilename(str(module.id)))
            
            # Create modules directory if not present
            if item.url != "":
                if not os.path.exists(items_dir):
                    os.makedirs(items_dir)

                filename = makeValidFilename(str(item.title)) + ".html"
                module_item_dir = os.path.join(items_dir, filename)

                # Download the module page.
                if not os.path.exists(module_item_dir):
                    download_page(item.url, cookies_path, items_dir, filename)
