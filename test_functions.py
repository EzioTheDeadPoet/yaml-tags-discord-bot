from rest_repository import get

if __name__ == '__main__':
    print("Get tags:")
    print(get.tags())

    print("Get tag content(\"todo\"):")
    print(get.content("todo"))
