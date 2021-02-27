import matplotlib.pyplot as plt
import pandas as pd

cn_eval = pd.read_csv('client_num_eval.csv')
cn_data_multiple = 32 * 10 * 10 # 32K * 10 files * 10 repeat times
cn_speed = cn_eval['N'] * cn_data_multiple / cn_eval['total_time'] / 1024 # in MB
cn_eval['speed'] = cn_speed

ds_eval = pd.read_csv('data_size_eval.csv')
ds_data_multiple = 10 * 4 * 10 # 10 files * 4 clients * 10 repeat times
ds_speed = ds_eval['size(kb)'] * ds_data_multiple / ds_eval['total_time'] / 1024 # in MB
ds_eval['speed'] = ds_speed

print(cn_eval)
print(ds_eval)

x = cn_eval['N']
y = cn_eval['speed']

# plot
plt.plot(x, y, marker='o', markersize=5, color="blue")

plt.title("Client Number Evaluation")
plt.xlabel("Number of Clients")
plt.ylabel("Transfer Speed (MB/s)")

plt.savefig("client_num_eval_graph.png")
plt.show()

x = ds_eval['size(kb)']
y = ds_eval['speed']

# plot
plt.plot(x, y, marker='o', markersize=5, color="blue")

plt.title("File Size Evaluation")
plt.xlabel("File Size (KB)")
plt.ylabel("Transfer Speed (MB/s)")

plt.savefig("data_size_eval_graph.png")
plt.show()