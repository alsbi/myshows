from myshows import MyshowsApiBase

def main():
    myshows = MyshowsApiBase('demo', 'demo')
    print myshows.profile()

if __name__ == "__main__":
    main()
