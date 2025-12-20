import textnode


def main():
    tn = textnode.TextNode("This is some anchor text", textnode.TextType.link, "https://www.boot.dev")
    print(tn)


if __name__ == "__main__":
    main()