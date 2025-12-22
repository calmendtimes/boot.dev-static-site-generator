import shutil
import textnode


def main():
    tn = textnode.TextNode("This is some anchor text", textnode.TextType.link, "https://www.boot.dev")
    print(tn)


def copy_static_to_public():
    shutil.rmtree("./public", ignore_errors=True)
    shutil.copytree("./static", "./public")


if __name__ == "__main__":
    copy_static_to_public()
    main()  