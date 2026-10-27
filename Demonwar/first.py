def countequal (height):
    sorted_height = sorted(height)
    count =0
    for i in range (len(height)):
        if height[i]!=sorted_height[i]:
            count+=1
    return count
height = input("Enter numbers: ")
height = [int(x) for x in height.split(",")]
print(countequal(height))