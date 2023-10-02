import time


# Your function that processes each item and saves output to a file
def process_item(item):
    # Replace this with your actual processing logic and file-saving code
    # For demonstration purposes, we'll simply sleep for a random time to simulate the processing time
    processing_time = 0.1
    time.sleep(processing_time)


# The list of 100 items
items_list = list(range(1, 101))

# Variables to keep track of time
start_time = time.time()
average_time_per_item = 0

# Loop over each item and apply the function
for i, item in enumerate(items_list, 1):
    # Measure the time taken for each item
    item_start_time = time.time()

    process_item(item)  # THIS IS THE ACTUAL LINE I AM INTERESTED IN!

    item_end_time = time.time()
    item_time_taken = item_end_time - item_start_time

    # Calculate the average time per item so far
    average_time_per_item = (average_time_per_item * (i - 1) + item_time_taken) / i

    # Calculate estimated time remaining
    items_remaining = len(items_list) - i
    estimated_time_remaining = average_time_per_item * items_remaining

    # Print progress
    print(
        f"Item {i} of {len(items_list)} finished; Time elapsed: {time.time() - start_time:.2f}s; Time taken for last item: {item_time_taken:.2f}s; Estimated time remaining: {estimated_time_remaining:.2f}s"
    )

print("All items processed!")
