
def get_class_by_name(name):
    parts = name.split('.')
    cls_name = parts[-1]
    module_name = ".".join(parts[:-1])

    module = __import__(module_name, fromlist=[cls_name])
    cls = getattr(module, cls_name)
    return cls
