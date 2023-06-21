import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 读csv
df = pd.read_csv('test.csv')

# Preprocessing block_size and field_size to be integer tuples (using first value of tuple)
df['block_size'] = df['block_size'].str.replace('(', '').str.replace(')', '').str.split(', ').apply(lambda x: int(x[0]))
df['field_size'] = df['field_size'].str.replace('(', '').str.replace(')', '').str.split(', ').apply(lambda x: int(x[0]))

# 按field_size和plot分组
grouped = df.groupby('field_size')
for name, group in grouped:
    plt.figure(figsize=(10, 6))
    plt.plot(group['block_size'], group['time_traversal_parallel'], label='Parallel Traversal', marker='o')
    plt.plot(group['block_size'], group['time_block_based_traversal'], label='Block-based Traversal', marker='o')
    plt.xlabel('Block Size')
    plt.ylabel('Time (ms)')
    plt.title(f'Field Size = {name}')
    plt.legend()
    plt.grid(True)
    plt.show()


# heatmap
plt.figure(figsize=(10, 6))
pivot_table = df.pivot(index='field_size', columns='block_size', values='time_traversal_parallel')
sns.heatmap(pivot_table, annot=True, fmt=".1f", cmap='YlGnBu')
plt.title('Time (ms) of Traversal Parallel')
plt.xlabel('Block Size')
plt.ylabel('Field Size')
plt.show()

plt.figure(figsize=(10, 6))
pivot_table = df.pivot(index='field_size', columns='block_size', values='time_block_based_traversal')
sns.heatmap(pivot_table, annot=True, fmt=".1f", cmap='YlGnBu')
plt.title('Time(ms) of Block Based Traversal')
plt.xlabel('Block Size')
plt.ylabel('Field Size')
plt.show()

# boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(x='block_size', y='time_traversal_parallel', data=df)
plt.title('Boxplot of Time Traversal Parallel vs Block Size')
plt.xlabel('Block Size')
plt.ylabel('Time Traversal Parallel')
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x='block_size', y='time_block_based_traversal', data=df)
plt.title('Boxplot of Block Based Traversal vs Block Size')
plt.xlabel('Block Size')
plt.ylabel('Block Based Traversal')
plt.show()
