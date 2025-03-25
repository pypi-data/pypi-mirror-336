def reverse_string(sentence):
    word = ""
    main = []

    a = sentence.split("")

    # Extract words from the sentence
    for char in sentence:
        if char != "":
            word += char
        elif word:
            main.append(word)
            word = ""

    if word:
        main.append(word)

    # Display reversed order
    return "".join(main[::-1])