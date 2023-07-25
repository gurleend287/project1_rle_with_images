import console_gfx

# Returns number of runs of data in an image data set
# count_runs([15, 15, 15, 4, 4, 4, 4, 4, 4]) yields integer 2
def count_runs(flatData: list):
    run = 1
    number = flatData[0]
    for item in flatData:
        if item != number:
            run += 1
            number = item
    return run

# Translates data (RLE or raw) a hexadecimal string (without delimiters)
#  to_hex_string([3, 15, 6, 4]) yields string "3f64"
def to_hex_string(data: list):
    hex_string = ''
    hex_translator = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    for item in data:
        hex_string += hex_translator[item]
    return hex_string

# Returns encoding (in RLE) of the raw data passed in; used to generate RLE representation of a data
# encode_rle([15,15,15,4,4,4,4,4,4]) yields b'\x03\x0f\x06\x04' (i.e., [3, 15, 6, 4])
def encode_rle(flat_data: list):
    count = 0
    number = flat_data[0]
    encoded_data = []

    # appends decimal length and hexadecimal digit to list
    for i, item in enumerate(flat_data):
        if item == number:
            count += 1
        else:
            # splits length if greater than 15
            if count > 15:
                num = count // 15
                while num > 0:
                    encoded_data.append(15)
                    encoded_data.append(number)
                    num = num - 1
                encoded_data.append(count % 15)
                encoded_data.append(number)
            else:
                encoded_data.append(count)
                encoded_data.append(number)
            count = 1
        number = flat_data[i]

        # values to append when at the end of the data
        if i == len(flat_data) - 1:
            if count > 15:
                num = count // 15
                while num > 0:
                    encoded_data.append(15)
                    encoded_data.append(item)
                    num = num - 1
                encoded_data.append(count % 15)
                encoded_data.append(item)
            else:
                encoded_data.append(count)
                encoded_data.append(item)

    return bytes(encoded_data)

# Returns decompressed size RLE data; used to generate flat data from RLE encoding
# get_decoded_length([3, 15, 6, 4]) yields integer 9
def get_decoded_length(rle_data: list):
    count = 0
    for i, item in enumerate(rle_data):
        if i % 2 == 0:
            count += item

    return count

# Returns the decoded data set from RLE encoded data
# decode_rle([3, 15, 6, 4]) yields b'\x0f\x0f\x0f\x04\x04\x04\x04\x04\x04'
def decode_rle(rle_data: list):
    list1 = []
    for i, item in enumerate(rle_data):
        if i % 2 == 0:
            count = rle_data[i]
            while count != 0:
                list1.append(rle_data[i + 1])
                count = count - 1
    return bytes(list1)

# Translates a string in hexadecimal format into byte data (can be raw or RLE)
# string_to_data("3f64") yields b'\x03\x0f\x06\x04' (i.e., [3, 15, 6, 4])
def string_to_data(data_string: str):
    rle_data = []
    hex_translator = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    temp = 0
    for i, item in enumerate(data_string):
        for x, number in enumerate(hex_translator):
            if item.lower() == number:
                temp = x
        rle_data.append(temp)

    return bytes(rle_data)

# Translates RLE data into a human-readable representation. For each run, in order, it should display the run
# length in decimal (1-2 digits); the run value in hexadecimal (1 digit); and a delimiter, ‘:’, between runs.
#  to_rle_string([10, 15, 6, 4]) yields string "10f:64"
def to_rle_string(rleData: list):
    hex_translator = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    string_list = []
    string = ""
    for i, item in enumerate(rleData):
        if i % 2 == 1:
            temp = hex_translator[item]
            string_list.append(temp)
            if i != len(rleData) - 1:
                string_list.append(":")
        else:
            string_list.append(str(item))

    string = "".join(string_list)
    return string

# Translates a string in human-readable RLE format (with delimiters) into RLE byte data
# string_to_rle("10f:64") yields b'\x0a\x0f\x06\x04' (i.e., [10, 15, 6, 4]).
def string_to_rle(rleString: str):
    string1_split = rleString.split(':')
    string2 = []

    for item in string1_split:
        string2.append(item[:len(item) - 1])
        string2.append(item[len(item) - 1])

    hex_translator = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

    temp = 0
    string_list = []
    for i, item in enumerate(string2):
        if i % 2 == 1:
            for x, number in enumerate(hex_translator):
                if item.lower() == number:
                    temp = x
                    string_list.append(temp)
        else:
            string_list.append(int(item))

    return bytes(string_list)

# Displays the menu and error checks for invalid user input
def menu():
    print('''
RLE Menu
--------
0. Exit
1. Load File
2. Load Test Image
3. Read RLE String
4. Read RLE Hex String
5. Read Data Hex String
6. Display Image
7. Display RLE String
8. Display Hex RLE Data
9. Display Hex Flat Data''')
    print()

    menu_choice = int(input("Select a Menu Option: "))

    while menu_choice > 9 or menu_choice < 0:
        print("Error! Invalid input.")
        print('''
RLE Menu
--------
0. Exit
1. Load File
2. Load Test Image
3. Read RLE String
4. Read RLE Hex String
5. Read Data Hex String
6. Display Image
7. Display RLE String
8. Display Hex RLE Data
9. Display Hex Flat Data''')
        print()

        menu_choice = int(input("Select a Menu Option: "))

    return menu_choice


def main():
    # Welcome screen, with TEST_RAINBOW and menu
    print("Welcome to the RLE image encoder!")
    print()
    print("Displaying Spectrum Image:")

    console_gfx.display_image(console_gfx.TEST_RAINBOW)
    menu_choice = menu()

    # Variable initialization
    file_name = ''
    test_image = ''
    flat_hex_string = ''
    rle_string = ''
    hex_string = ''
    rle_string = ''
    current_data = 0
    result = "(no data)"
    res = "(no data)"
    r = "(no data)"

    while menu_choice != 0:

        # Accepts a filename from the user
        if menu_choice == 1:
            file_name = input("Enter name of file to load: ")
            file = console_gfx.load_file(file_name)
            current_data = 1

            menu_choice = menu()

        # Loads console_gfx.TEST_IMAGE
        if menu_choice == 2:
            test_image = console_gfx.TEST_IMAGE
            print("Test image data loaded.")
            current_data = 2

            menu_choice = menu()

        # Reads RLE data from the user in decimal notation with delimiters
        if menu_choice == 3:
            rle_string = input("Enter an RLE string to be decoded: ")
            # sample string
            # rle_string = "2e:15f:15f:5f:12:1a:12:6f:26:3f:12:2a:12:4f:46:3f:12:2a:22:2f:46:4f:12:2a:12:3f:26:2f:42:1a:12:1a:12:4f:22:1a:12:5a:12:3f:12:4a:12:4a:12:1f:22:10a:22:11a:12:1f:12:1a:32:2a:32:2a:12:1f:12:2a:12:1f:12:1a:12:2f:12:1a:12:2f:22:2f:12:2a:12:1f:12:2a:12"
            current_data = 3

            menu_choice = menu()

        # Reads RLE data from the user in hexadecimal notation without delimiters
        if menu_choice == 4:
            hex_string = input("Enter the hex string holding RLE data: ")
            # smiley example
            # hex_string = "28106B10AB102B10CB102B105B20BB106B10"

            byte_value = string_to_data(hex_string)
            list1 = list(byte_value)
            decoded_length = get_decoded_length(list1)
            print("RLE decoded length:", decoded_length)
            current_data = 4

            menu_choice = menu()

        # Reads raw (flat) data from the user in hexadecimal notation
        if menu_choice == 5:
            flat_hex_string = input("Enter the hex string holding flat data: ")
            # smiley example
            # flat_hex_string = "880bbbbbb0bbbbbbbbbb0bb0bbbbbbbbbbbb0bb0bbbbb00bbbbbbbbbbb0bbbbbb0"
            # flat_hex_string = "eefffffffffffffffffffffffffffffffffff2a2ffffff66fff2aa2ffff6666fff2aa22ff6666ffff2aa2fff66ff2222a2a2ffff22a2aaaaa2fff2aaaa2aaaa2f22aaaaaaaaaa22aaaaaaaaaaa2f2a222aa222aa2f2aa2f2a2ff2a2ff22ff2aa2f2aa2"
            flat_list = list(string_to_data(flat_hex_string))
            print(flat_list)
            final_runs = count_runs(flat_list)
            print("Number of runs:", final_runs)
            current_data = 5

            menu_choice = menu()

        # Displays current image
        if menu_choice == 6:
            if current_data == 0 or current_data > 3:
                print('Displaying image...')
                print('(no data)')

                menu_choice = menu()
            else:
                if len(file_name) > 0:
                    print("Displaying image...")
                    console_gfx.display_image(file)

                    menu_choice = menu()
                else:
                    print("Displaying image...")
                    console_gfx.display_image(test_image)

                    menu_choice = menu()

        # Converts the current data into a human-readable RLE representation (with delimiters)
        # length is always in decimal and value is always in hexademical
        if menu_choice == 7:

            if current_data == 1:
                result = to_rle_string(list(encode_rle(file)))

            if current_data == 2:
                result = to_rle_string(list(encode_rle(test_image)))

            if current_data == 3:
                result = rle_string.lower()

            if current_data == 4:
                result = to_rle_string(list(string_to_data(hex_string)))

            if current_data == 5:
                result = to_rle_string(list(encode_rle(flat_list)))

            print('RLE representation:', result)

            menu_choice = menu()

        # Converts the current data into RLE hexadecimal representation (without delimiters)
        if menu_choice == 8:
            if current_data == 1:
                res = to_hex_string(list(encode_rle(file)))

            if current_data == 2:
                res = to_hex_string(list(encode_rle(test_image)))

            if current_data == 3:
                result2 = string_to_rle(rle_string)
                res = to_hex_string(result2)

            if current_data == 4:
                res = hex_string.lower()

            if current_data == 5:
                res = to_hex_string(list(encode_rle(flat_list)))

            print('RLE hex values:', res)

            menu_choice = menu()

        # Displays the current raw (flat) data in hexadecimal representation (without delimiters)
        if menu_choice == 9:

            if current_data == 1:
                r = to_hex_string(file)

            if current_data == 2:
                r = to_hex_string(test_image)

            if current_data == 3:
                str1 = string_to_rle(rle_string)
                r1 = decode_rle(list(str1))
                r = to_hex_string(list(r1))

            if current_data == 4:
                print(hex_string)
                r1 = decode_rle(list(string_to_data(hex_string)))
                r = to_hex_string(list(r1))

            if current_data == 5:
                r = flat_hex_string

            print('Flat hex values:', r)

            menu_choice = menu()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# def get_initial_board(rows: int, columns: int):
