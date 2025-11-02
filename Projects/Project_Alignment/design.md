# Alignment Design


## Baseline

### How it works

- Basically you put one string on the horizontal of a table leaving one space to the left and one string going down the 
side of the table leaving one space above it empty so that each table element corresponds to one element from the horizontal 
string and one element from the vertical string.
- In the table element corresponding to both empty spots a zero is put and then each box to the right is filled in by adding 
the gap cost to the element to its left. After this the first column is filled out with each box equaling the box above it 
plus the gap cost.
- After the first row and column are filled out the rest of the table will be filled out by choosing whichever of the following 
four possible options would add to the smallest value.
- If the two elements values in the strings that the box corresponds to match then the box up and left diagonally from the 
box can have its value added to the cost of matching values.
- If the two element values don't match then the box can become the value of the box up and left one plus the cost of a mismatch.
- The value of the box can be the cost of the gap added to the value of either the box to the left or directly above it.
- After filling out the table the cost of aligning the strings will be the rightmost bottom corner of the table.
- Then, starting at the bottom right box you will make your way back to the upper left corner choosing the smallest value 
to the left, above, or up and left using these rules:
- If you move diagonally, then each string will keep the two elements corresponding to the box in the same place.
- If you move left, then the vertical string will have an empty slot added that will correspond to the horizontal string's
element the box matches to.
- If you move up, then an empty slot will be added to the horizontal string's element that corresponds to the box to the right.


### My Implementation

- I will use the needleman-wunsch algorithm to fill out the table and then i will make a function that will edit the string's
elements to match the shortest path through the table.
- I plan to use a matrix to store my table elements. The pros are that it has fast lookup speed and is efficient at storing
large amounts of data. There aren't really any cons that I can think of for using this.



## Core


### How it works

- You do everything the same as the unbanded algorithm except that instead of going for an entire row
you only fill out elements in the row +- the band width (how far from the origin (0,0) you want to go in either direction)
- So basically you move in a diagonal line towards the ending box following the above mentioned rules and filling out boxes
within the range of the bandwidth.

### My implementation

- I set it up when making my baseline to be able to use the same traceback method to actually implement the alignment of
sequences
- I will be using a dictionary to store my values and fill the table as I make it
- Using a dictionary is good because it won't waste space by adding unused spaces that the algorithm wouldn't use
like using a matrix would
- The only major downsides that i see is that it won't be as easy to see how the entries relate to each other as it would
be in a matix
- I'm going to use a fill table method to fill the table and then i'll use my traceback method that i used with my unbound 
algorithm to get the sequences aligned