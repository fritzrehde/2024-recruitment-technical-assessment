from collections import defaultdict
from dataclasses import dataclass


@dataclass
class File:
    id: int
    name: str
    categories: list[str]
    parent: int
    size: int


def leafFiles(files: list[File]) -> list[str]:
    """
    Task 1:
    The first task is to implement the leafFiles function, which takes in a list of files and returns a list containing the names of all leaf files, that is, files which have no children.
    The file names can be returned in any order.
    """
    parent_ids = set(file.parent for file in files if file.parent != -1)

    # Leaf files are those who are not parents of any other files.
    return [file.name for file in files if file.id not in parent_ids]


def kLargestCategories(files: list[File], k: int) -> list[str]:
    """
    Task 2:
    The second task is to implement the kLargestCategories function, which takes in a list of files and a number k and returns a list containing the k categories that have the most files.
    This list should be returned in descending order of size. If multiple categories have the same size, they should be ordered alphabetically. If there are less than k categories in the list of files, the returned list should contain all categories.
    """
    category_count = defaultdict(int)
    for file in files:
        for category in file.categories:
            category_count[category] += 1

    def cmp(item):
        category, count = item
        return (
            # Sort by count, descendingly.
            -count,
            # Sort alphabetically, ascendingly.
            category)

    category_count_sorted = sorted(category_count.items(), key=cmp)
    return [category for category, _count in category_count_sorted[:k]]


def largestFileSize(files: list[File]) -> int:
    """
    Task 3:
    The third and final task is to implement the largestFileSize function, which returns the size of the file with the largest total size. Total size includes the size of all children files (this includes grandchildren etc.).
    If there are no files, this function should return 0.
    """
    files_by_id = {file.id: file for file in files}

    # Map each (parent) file to its children
    children_by_parent_id = defaultdict(list)
    for child in files:
        if child.parent != -1:
            children_by_parent_id[child.parent].append(child.id)

    # TODO: improve performance: use memoization to skip re-calculating total_size
    # Calculate total size recursively
    def total_size(file_id: int) -> int:
        file_size = files_by_id[file_id].size
        children_size = sum(total_size(child_id)
                            for child_id in children_by_parent_id[file_id])
        return file_size + children_size

    return max([total_size(file.id) for file in files], default=0)


if __name__ == '__main__':
    testFiles = [
        File(1, "Document.txt", ["Documents"], 3, 1024),
        File(2, "Image.jpg", ["Media", "Photos"], 34, 2048),
        File(3, "Folder", ["Folder"], -1, 0),
        File(5, "Spreadsheet.xlsx", ["Documents", "Excel"], 3, 4096),
        File(8, "Backup.zip", ["Backup"], 233, 8192),
        File(13, "Presentation.pptx", ["Documents", "Presentation"], 3, 3072),
        File(21, "Video.mp4", ["Media", "Videos"], 34, 6144),
        File(34, "Folder2", ["Folder"], 3, 0),
        File(55, "Code.py", ["Programming"], -1, 1536),
        File(89, "Audio.mp3", ["Media", "Audio"], 34, 2560),
        File(144, "Spreadsheet2.xlsx", ["Documents", "Excel"], 3, 2048),
        File(233, "Folder3", ["Folder"], -1, 4096),
    ]

    assert sorted(leafFiles(testFiles)) == [
        "Audio.mp3",
        "Backup.zip",
        "Code.py",
        "Document.txt",
        "Image.jpg",
        "Presentation.pptx",
        "Spreadsheet.xlsx",
        "Spreadsheet2.xlsx",
        "Video.mp4"
    ]

    assert kLargestCategories(testFiles, 3) == [
        "Documents", "Folder", "Media"
    ]
    assert kLargestCategories(testFiles, 5) == [
        "Documents", "Folder", "Media", "Excel", "Audio"
    ]

    assert largestFileSize(testFiles) == 20992
