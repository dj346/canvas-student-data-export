def getCoursePageUrls(course):
    page_urls = []

    try:
        # Get all pages
        pages = course.get_pages()

        for page in pages:
            if hasattr(page, "url"):
                page_urls.append(str(page.url))
    except Exception as e:
        if e.message != "Not Found":
            print("Skipping page that gave the following error:")
            print(e)

    return page_urls

def findCoursePages(course):
    page_views = []

    try:
        # Get all page URLs
        page_urls = getCoursePageUrls(course)

        for url in page_urls:
            page = course.get_page(url)

            page_view = pageView()

            # ID
            page_view.id = page.id if hasattr(page, "id") else 0

            # Title
            page_view.title = str(page.title) if hasattr(page, "title") else ""
            # Body
            page_view.body = str(page.body) if hasattr(page, "body") else ""
            # Date created
            page_view.created_date = dateutil.parser.parse(page.created_at).strftime(DATE_TEMPLATE) if \
                hasattr(page, "created_at") else ""
            # Date last updated
            page_view.last_updated_date = dateutil.parser.parse(page.updated_at).strftime(DATE_TEMPLATE) if \
                hasattr(page, "updated_at") else ""

            page_views.append(page_view)
    except Exception as e:
        print("Skipping page download that gave the following error:")
        print(e)

    return page_views  