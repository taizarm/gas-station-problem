import re


class GasStationClass(object):

    def validate_input(self, strArr):
        '''
            Validate strArr. Verify if n >=2 and if the size of elements corresponds to n
        '''

        n = int(strArr[0])

        if n < 2:
            raise Exception

        if len(strArr) -1 != n:
            raise Exception

        return n

    def construct_array_diff(self, n, strArr):
        '''
            Construct array diff, whose value corresponds to difference between g and c
        '''
        array_diff = [None] * n

        for i in range(1, n+1):
            gc = strArr[i]

            if not re.match('[0-9]+:[0-9]+', gc):
                raise Exception

            gc_split = gc.split(':')

            array_diff[i-1] = int(gc_split[0]) - int(gc_split[1])

        return array_diff

    def GasStation(self, strArr=None):
        '''
            Return the smallest index of the starting gas station that will allow you to travel around the whole route once
        '''

        try:
            n = self.validate_input(strArr)
            array_diff = self.construct_array_diff(n, strArr)
        except:
            return 'invalid input'

        begin = 0
        end = 1
        sum = array_diff[begin]

        if n == 2:
            if sum < 0:
                begin += 1
                sum = array_diff[begin]
        else:
            while not (begin >= n or (begin == 0 and end == n-1) or (end == begin-1)):

                while sum < 0 and begin < end and begin < n:
                    sum -= array_diff[begin]
                    begin += 1

                if begin < n:
                    sum += array_diff[end]
                    end += 1
                    if end >= n:
                        end = 0

        if sum < 0 or begin >= n:
            return 'impossible'

        return str(begin + 1)
