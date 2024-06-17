def willRun(code):
    OutputInstructions = ['H', 'Q', '9']
    
    for i in range(len(code)):
        assert ord(code[i]) in range(33, 127)
        if code[i] in OutputInstructions:
            return 'YES'
    
    return 'NO'


def main():
    HQ9_code = input()
    
    print(willRun(HQ9_code))

if __name__ == "__main__":
    main()