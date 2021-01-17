  # elif 'plot' or 'graph' in query:
        #     speak("I can only plot linear regression graphs. Please enter the x axis values below")
        #     x=list(map(int,input("X Values").split(","))) 
        #     speak("Please enter the y axis values below")
        #     y=list(map(int,input("Y Values").split(","))) 
        #     if len(x)!= len(y):
        #         while len(x)!= len(y):
        #             if len(x)> len(y):
        #                 x.pop()
        #             else: 
        #                 y.pop()
        #     plt.plot(x, y)
        #     speak("Please enter the names of x and y labels below")
        #     xlab= input("X label: ")
        #     ylab= input("Y label: ")
        #     plt.xlabel(xlab)
        #     plt.ylabel(ylab)
        #     speak("Enter the name of your graph")
        #     title= input("Name: ")
        #     plt.title(title)
        #     plt.show()