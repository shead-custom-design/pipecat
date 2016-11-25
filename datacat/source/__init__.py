import itertools

def limit(source, count):
    for observation in itertools.islice(source, count):
        yield observation
