# pylint: disable=c-extension-no-member
import py.proto.libaddress_book_proto

def NewAddressBook():
    return py.proto.libaddress_book_proto.AddressBook()
