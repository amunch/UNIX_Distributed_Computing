Project 02: Distributed Computing
=================================

Please see the [distributed computing project] write-up.

[distributed computing project]: https://www3.nd.edu/~pbui/teaching/cse.20189.sp16/homework10.html

**Report**

**1)** hulk.py creates every permutation of a given length from an alphabet of all lowercase and numeric characters.  It then converts these words to their corresponding md5 hash and if there is a match, it returns that words as that word is in our list of md5 hashes.  Some features include the ability to pass along your own alphabet, the ability to specify the desired length of passwords, the ability to specify a path where the file full of hashes is located, and a prefix appended to every permutation of length l.
	To test hulk and verify that it worked properly, we tested various lengths and prefixes and made sure that the prefixes were all in the ouputted passwords as well as that the various lengths were outputting passwords of that length.  We also made sure that a new alphabet will work correctly, and limit the number of permuations required.

**2)** fury.py works by sending the hulk.py script along with various prefixes to divy up the work done by different CPUs.  It does this by declaring the command as a string and then sending it along to the work_queue by creating a task object as such:
		
	task = work_queue.Task(command)

Then specifying the source file and source script:

	for source in ('hulk.py', HASHES):
		task.specify_file(source, source, work_queue.WORK_QUEUE_INPUT)

and then submitting the task to the queue using queue.submit(task).

To divide up the work among many workers, I first sent 5 tasks for passwords of length 1 to 5 using the above method and a for loop. To get passwords of length 6, 7, and 8, I used the prefix feature of hulk to accomplish this.  I did this by creating permutaitons of the alphabet stated above to create the prefixes, and then passing these along as the prefixes.  I did these for lengths 1 to 3, and appending these to the permutations of length 5 gave several tens of thousands of tasks that were essentially each cracking passcodes of 5, but together were all permuations up to length 8. To create the prefixes, I used the following:
		
	for prefix in itertools.product(ALPHABET, repeat = int(num))

To keep track of what tasks have been done already, I created a json fike.  I first opened this json file in the beginning of the program using the following:
	
	JOURNAL = json.load(open('journal.json'))

Whenever a task was completed and if its return status was 0, I editted this json object to include the outputs of the program using the following:

	JOURNAL[task.command] - task.output.split()

Which gives the passwrods for every command run.  I then wrote this to a file called journal.json.new, and then renamed it to journal.json, so that if any errors occurred it would not corrupt our precious journal.

The journal was the main method by which we recovered from failures.  My process was killed once, so we had everything in the journal and we could simply run the program again and it would not run the commands that have already been run, using the following if statement:

	if command in JOURNAL:

where it added the task for that command to the queue if the command was in the JOURNAL.  Thus, we could save a lot of time if there was a failure somewhere.

To test that fury.py worked correctly, I first started with only a length of 1 and then moved up from there, adding more tasks and workers.  When I added the prefix functionality, I printed out all of the commands and made sure they were what I desired.  Once I verified that all of this was coorect, I added the journal and made sure that the journal was keeping entries correctly and that running fury again would not rerun processes.  Once I verified all of this, I ran it for all of the prefixes and lengths.

**3)** By mulitplication rule, the number of permutations will be the length of the alphabet to the power that is the length of the password.  Increasing the length of the password will increase the number of permuatations exponentially.  Increasing the length of the alphabet will only increase what is mulitplied , and this will not affect the time it takes to run nearly as bad as the exponenetial increase.  For example, consider an alphabet of 26 characters with a length of 5.  This will have 11,881,376 possible combinations.  If the length is increased to 6, it now has 308,915,776 possible combination. If the alphabet is increased to 27, however, the number of combinations only raises to 14,348,907.
