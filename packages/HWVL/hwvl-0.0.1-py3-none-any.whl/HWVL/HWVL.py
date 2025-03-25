from os import system, name

def clear_console():

    if name == 'nt':
        system('cls')
    else:
        system('clear')
        
def string_to_int(char):
    return ord(char)

def int_to_string(Int):
    printable_start = 33
    printable_end = 126
    range_size = printable_end - printable_start + 1
    return chr(printable_start + (Int % range_size))

def shift_right(lst, shift):
    shift = shift % len(lst)
    return lst[-shift:] + lst[:-shift]

def calculate_column_wise_average(lst):
    num_columns = len(lst[0])
    return [round(sum(row[j] for row in lst) / len(lst)) for j in range(num_columns)]

def average_with_right(lst):

    if len(lst) < 2:
        return lst

    new_lst = []
    
    for i in range(len(lst) - 1):

        avg = (lst[i] + lst[i + 1]) / 2
        new_lst.append(avg)

    avg_last_first = (lst[-1] + lst[0]) / 2
    new_lst.append(avg_last_first)
    return new_lst

def HWVL(text="",l=32):
    if text=="":
        return ""
    
    while not len(text)%l==0:
        text+="@"
    b=[]
    
    for a in range(len(text)//l):
        li=[]
        for i in list(text[a*l:(a+1)*l]):
            li.append(string_to_int(i))
        li=average_with_right(li)
        
        for i in range(l): 
            li=shift_right(li,int(li[0]))
            li.sort()
            for i in range(len(li)-2):
                li[i]=li[i]*li[i+1]/li[i+2]
        li.reverse()
        b.append(li)
    
    output_list=calculate_column_wise_average(b)
    output_text=""
    
    for i in output_list:  
        output_text+=int_to_string(i)

            
    return output_text

if __name__ == "__main__":
    while True:
        text=input(">>>")
        if text=="exit":
            break
        elif text=="cls":
            clear_console()
        elif text!="":
            Hash=HWVL(text)
            print(Hash)
