import matplotlib.pyplot as plt


def means(file_path):
    totalTime = 0
    count = 0

    with open(file_path, 'r') as file:
        for line in file:
            if "Time taken:" in line:
                timeTaken = float(line.strip().split(': ')[1].split(' ')[0])
                totalTime += timeTaken
                count += 1

    if count > 0:
        mean = totalTime / count
        return mean
    else:
        return "No time found"

def plot(processCount, meanValues):
    positions = range(len(processCount))
    plt.figure(figsize=(10, 5))
    plt.plot(positions, meanValues, marker='o')
    plt.title('Execution time vs processes')
    plt.xlabel('Number of processes')
    plt.ylabel('Mean time (S)')
    plt.grid(True)
    plt.xticks(positions, processCount)
    plt.show()


mean8 = means('results/MC8.txt')
print(f"Mean time taken for 8: {mean8} seconds")
mean16 = means('results/MC16.txt')
print(f"Mean time taken for 16: {mean16} seconds")
mean32 = means('results/MC32.txt')
print(f"Mean time taken for 32: {mean32} seconds")
mean64 = means('results/MC64.txt')
print(f"Mean time taken  for 64: {mean64} seconds")
mean128 = means('results/MC128.txt')
print(f"Mean time taken 128: {mean128} seconds")
mean256 = means('results/MC256.txt')
print(f"Mean time taken 256: {mean256} seconds")

processCount = [8, 16, 32, 64, 128, 256]
means = [mean8, mean16, mean32, mean64, mean128, mean256]
plot(processCount, means)