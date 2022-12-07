import os
import time


class Dir:

    def __init__(self, name, parent_dir):
        self.name = name
        self.parent_dir = parent_dir
        self.sub_dirs = {}
        self.files = {}
        self.size = None

    def add_sub_dir(self, sub_dir):
        if sub_dir.name in self.sub_dirs:
            raise Exception("Whoot?")
        self.sub_dirs[sub_dir.name] = sub_dir

    def add_file(self, name, size):
        if name in self.files:
            raise Exception("Whoot?")
        self.files[name] = size

    def get_sub_dir(self, name):
        return self.sub_dirs[name]

    def get_size(self):
        if not self.size:
            sub_dir_size = sum([sub_dir.get_size() for sub_dir in self.sub_dirs.values()])
            file_size = sum(self.files.values())
            self.size = sub_dir_size + file_size
        return self.size


def main(puzzle_input):
    root = Dir("/", None)
    current_dir = None
    for line in puzzle_input:
        if line.startswith("$ cd /"):
            current_dir = root
        elif line.startswith("$ cd .."):
            current_dir = current_dir.parent_dir
        elif line.startswith("$ cd "):
            current_dir = current_dir.get_sub_dir(line[5:])
        elif line.startswith("$ ls"):
            pass
        elif line.startswith("dir "):
            new_dir = Dir(line[4:], current_dir)
            current_dir.add_sub_dir(new_dir)
        else:
            size, name = line.split(" ")
            current_dir.add_file(name, int(size))

    dir_sizes = []
    dirs = [root]
    while dirs:
        current_dir = dirs.pop()
        dirs.extend(current_dir.sub_dirs.values())
        dir_sizes.append(current_dir.get_size())

    print("Solution 1: {}".format(sum([dir_size for dir_size in dir_sizes if dir_size < 100000])))

    missing_size = 30000000 - (70000000 - root.get_size())
    size_to_delete = next(dir_size for dir_size in sorted(dir_sizes) if dir_size - missing_size > 0)

    print("Solution 2: {}".format(size_to_delete))


if __name__ == "__main__":
    input_filename = os.path.basename(__file__).replace("aoc", "input").replace("py", "txt")
    with open("input/{}".format(input_filename)) as f:
        content = f.read().splitlines()

    start = time.time()
    main(content)
    end = time.time()
    diff = (end - start)
    if diff >= 1:
        print("The solutions took {}s".format(round(diff)))
    else:
        print("The solutions took {}ms".format(round(diff * 1000)))
