"""Cleverbot powered Tinder!"""
from cleverbot import Cleverbot


def main():
    """Main method"""
    print "Starting CBOT TIND!"
    cbot = Cleverbot()
    response = cbot.ask("Hello!")
    print response

if __name__ == "__main__":
    main()
