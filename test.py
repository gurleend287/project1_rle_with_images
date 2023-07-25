def main():

    rleString = "2e:15f:15f:5f:12:1a:12:6f:26:3f:12:2a:12:4f:46:3f:12:2a:22:2f:46:4f:12:2a:12:3f:26:2f:42:1a:12:1a:12:4f:22:1a:12:5a:12:3f:12:4a:12:4a:12:1f:22:10a:22:11a:12:1f:12:1a:32:2a:32:2a:12:1f:12:2a:12:1f:12:1a:12:2f:12:1a:12:2f:22:2f:12:2a:12:1f:12:2a:12"

    string1_split = rleString.split(':')
    string2 = []

    for item in string1_split:
        string2.append(item[:len(item) - 1])
        string2.append(item[len(item) - 1])

    print("haha", string2)

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

    # print(bytes(string_list))

    print("haha2", string_list)



if __name__ == '__main__':
    main()