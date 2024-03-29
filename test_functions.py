from rest_repository import get

if __name__ == '__main__':
    # print("Get tags:")
    # print(get.tags())

    print("Get tag content(\"todo\"):")
    print(get.content("todo"))
    print("-----------------------------")
    print("Get tag content(\"td\"):")
    content = ""
    try:
        content = get.content("td")
    except KeyError:
        content = "Tag not found"
    print(content)
    print("---------------------------")
    print("Get tag content(\"av_test\"):")
    print(get.content("av_test"))
