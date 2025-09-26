
def guess_number(target, lst, type_)->list[int, int | None]:

    '''
      ввод значений с клавиатуры для формирования
      списка, о которому мы ищем искомое число и
      искомого числа
      (опционально) предложить пользователю
      сформировать список вручную с клавиатуры

      __вызов функции guess-number  параметрами:__
        - искомое число (target)
        - список, по которому идём
        - тип поиска (последовательный, бинарный)

      __вывод результатов на экран__
      :return:
      '''
    lst.sort()
    iter_count=0
    if type_=='seq':
        k=0
        for i in range(len(lst)-1):
            iter_count+=1
            if lst[i]==target:
                return [target,iter_count]
    elif type_=="bin":
        low=0 #нижняя граница диапозона
        high=len(lst)-1 #верхняя граница диапозона
        while low<=high:
            iter_count+=1
            mid=(low+high)//2 #находим середину
            guess=lst[mid]
            if guess==target:
                return [target,iter_count] #нашли элемент
            elif guess<target:
                low=mid+1 #поиск в правой половине
            else:
                high=mid-1 #поиск в левой половине
        return None