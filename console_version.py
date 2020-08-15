from search import get_doc

search = input("Name doc - ")  # SEARCH REQUEST
count = input("Count = ")  # Count Results


result = get_doc(search, count)
for key, value in result.items():
    url = key
    title, size, time = value
    print(title)
    print(time)
    print(size)
    print(url)
print("-" * 128)