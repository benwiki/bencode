import os
from PIL import Image, ImageChops, ImageStat


def compare_picture_lists(
    pics1: list[str], pics2: list[str]
) -> tuple[list[str], list[str]]:
    """
    Compare two picture lists by their content.
    List all differing pictures from both lists.
    """
    differing_pics1 = [
        pic for pic in pics1 if not any(pictures_identical(pic, pic2) for pic2 in pics2)
    ]
    differing_pics2 = [
        pic for pic in pics2 if not any(pictures_identical(pic, pic1) for pic1 in pics1)
    ]

    return differing_pics1, differing_pics2


def pictures_identical(pic_1: str, pic_2: str) -> bool:
    """
    Compare two pictures by their content.
    Return True if the pictures are the same, False otherwise.
    """
    pic1 = Image.open(pic_1)
    pic2 = Image.open(pic_2)

    diff = ImageChops.difference(pic1, pic2)
    p1name = pic_1.split('\\')[-1]
    p2name = pic_2.split('\\')[-1]
    name = f"diff_{p1name}_{p2name}.png"
    diff.save(name)
    name = "diff"+ pic_1.split('\\')[-1]+"_"+ pic_2.split('\\')[-1] + ".png"
    avg_brightness = brightness(diff)
    print(p1name, p2name, "*" * int(avg_brightness * 10))
    return avg_brightness < 10

def brightness(img: Image.Image):
    im = img.convert('L')
    stat = ImageStat.Stat(im)
    return stat.mean[0]


if __name__ == "__main__":
    PATH_1 = r"C:\Users\b.hargitai\Downloads\pl_extern_how_to_2025-01-24"
    names1 = list(sorted(os.walk(PATH_1).__next__()[2], key=lambda x: f"{x.split('.')[0]:0>2}"))
    pics1 = [PATH_1 + "\\" + item for item in names1]
    PATH_2 = r"C:\Users\b.hargitai\Downloads\pl_intern_how_to_2025-01-24"
    names2 = list(sorted(os.walk(PATH_2).__next__()[2], key=lambda x: f"{x.split('.')[0]:0>2}"))
    pics2 = [PATH_2 + "\\" + item for item in names2]

    # differing_pics1, differing_pics2 = compare_picture_lists(pics1, pics2)
    # print("Differing pictures in list 1:", differing_pics1)
    # print("Differing pictures in list 2:", differing_pics2)
    for pic1, pic2 in zip(pics1, pics2):
        if not pictures_identical(pic1, pic2):
            name1 = '/'.join(pic1.split('\\')[-2:])
            name2 = '/'.join(pic2.split('\\')[-2:])
            print(f"{name1} and {name2} are different.")
