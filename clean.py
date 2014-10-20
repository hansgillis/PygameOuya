def clean_up():
    import os
    for root, dirs, files in os.walk("./"):
        for file in files:
            if file.endswith(".pyc") or file.endswith(".pyo"):
                os.remove(os.path.join(root, file))

if __name__ == "__main__":
    clean_up()
