import numpy as np

history_ratio=0.6
index=-1
height=5
width=1
scale_factor=2
array_size=height*scale_factor
first_round=True
history_count = int(history_ratio*height)
partition_count = height - history_count
next_index=0
spatio_array=np.zeros((array_size,width),dtype=np.int)
i=0

while(1):
    index= (index+1)%array_size
    i+=1
    spatio_array[index%array_size,]=i

    if  first_round :
        if(index==array_size-1):
            first_round= False

        if(index==height-1):
            next_index = index + partition_count

            print spatio_array[:index+1,]


        if(index>height and index==next_index) :
            next_index = (index + partition_count) % array_size
            print spatio_array[index-(height-1):index+1,]


    else:
        if next_index == index:
            next_index = (index + partition_count) % array_size
            if index < height-1 :
                print index
                print np.concatenate((spatio_array[-(height-index-1):,],spatio_array[:index+1,]),axis=0)

            else:
                print spatio_array[index - (height-1):index+1,]







