from textnode import *

def main():

    text = "djsfla;kj"
    text_type = TextType.NORMAL
    url = "boot.dev"

    node = TextNode(text, text_type, url)
    print(node)

main()
