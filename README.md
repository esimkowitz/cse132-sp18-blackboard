# CSE 132 SP18 Blackboard Scripts

## Notes - Evan

1. I'm not sure how Josh stores late assignment tallies
1. I found an Excel to JSON function and added it to gradeStuff. I haven't tested it in gradeStuff but I tested it on the Studio 1 form output and it worked! I'm working to integrate it into the rest of the process() function.
1. From what I can tell, Blackboard expects you to download the whole Gradebook and then upload the whole Gradebook with the changes. To do this, I'm thinking about modifying the Student class to store all relevant grade data. When making the studentDict at the beginning of the program, I'd load in all the grade data in each of the Student objects. All updates to the grade data would be stored in these objects and then at the end would be loaded back into the Gradebook CSV before uploading it.
1. I am thinking that to do this I'd also need to store a mapping from CSV column to header name to make the unloading and loading of grade data easier.