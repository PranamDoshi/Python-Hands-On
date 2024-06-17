def main():
    wubSong = input()
    assert len(wubSong) > 0

    songWords = wubSong.split('WUB')
    originalSong = []

    for word in songWords:
        if len(word) > 0 and word != "WUB":
            originalSong.append(word.strip())
    
    print(" ".join(originalSong))
    

if __name__ == "__main__":
    main()