import py.lib.lib
import py.proto.libecho_proto  # pyright: ignore[reportMissingImports]


def main():
    ab = py.lib.lib.NewAddressBook()
    p = ab.person.add()
    p.name = "chenfeng"
    p.id = 9527
    p.email = "chen3feng@gmail.com"
    print(ab)


if __name__ == "__main__":
    main()
