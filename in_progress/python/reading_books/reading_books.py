with open('books.txt', 'a+') as books_file:
    books = [line.strip() for line in books_file.readlines()]

    book = input('Existing books (you can add):\n' +
                 '\n'.join(books) +
                 '\nWrite the book name here: ')

    with open(f'{book}.txt', 'a+') as b:
        data = b.readline()
        if data == '':
            pagenum = int(input("Please give the number of pages: "))
            reading_time = int(input('Reading time in days: '))
            session_per_day = int(input('Number of sessions per day: '))
            pps = pagenum//reading_time//session_per_day
            print(f'Your estimated number of pages per session: {pps}-{pps+1}')
            data = {'pagenum': pagenum, 'reading_time': reading_time,
                    'session_per_day': session_per_day}
            b.write(str(data))
        else:
            data = eval(data)
            pps = data['pagenum']//data['reading_time']//data['session_per_day']
            print(f'Your estimated number of pages per session: {pps}-{pps+1}')
    books_file.write(book+'\n')
