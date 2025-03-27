import time

def desc_prep(desc):
	length = len(desc)
	if length >= 15:
		new_desc = desc[:12] + "... " 
	else:
		new_desc = desc + (" " * (15-length))
	return "🌈 " + new_desc

def lgbt(iterable, desc="Processing:"):

	colours = ["\033[31m", "\033[38;5;214m", "\033[33m", "\033[32m", "\033[36m", "\033[34m", "\033[35m" ]
	desc = desc_prep(desc)
	number_of_colours = len(colours)
	total = len(iterable)
	bar_width = 70  
	
	start = time.perf_counter()
	for i, data in enumerate(iterable, 1):
		filled = round(i / total * bar_width) 
		empty = bar_width - filled  

		bar = "▋" * filled + " " * empty  
		percent = (i / total) * 100  

		painted_bar = "".join(colours[i // (bar_width // number_of_colours)]  + c if i % (bar_width // number_of_colours) == 1 else c for i, c in enumerate(bar,1))
		to_print = desc + painted_bar

		end = time.perf_counter() - start
		percent_str = f'[{percent:.1f}%]'
		time_str = f'[{end:.2f}s]'
		it_srt = f'[{i/end:.2f}it]' + (" "*5) 
		print(f"\r{to_print} {percent_str} {time_str} {it_srt}\033[0m", end="", flush=True)

		yield data

	print("\n\033[0m")  