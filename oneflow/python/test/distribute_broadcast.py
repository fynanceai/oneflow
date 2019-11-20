import oneflow as flow
import numpy as np

flow.config.gpu_device_num(2)
flow.config.grpc_use_no_signal()

flow.config.default_data_type(flow.float)

def Print(prefix):
    def _print(x):
        print(prefix)
        print(x)
    return _print

@flow.function
def DistributeBroadcast(x = flow.input_blob_def((2, 5), is_dynamic=True)):
  with flow.device_prior_placement("gpu", "0:0"):
    a = flow.identity(x)
    b = flow.math.relu(x)
  y = flow.advanced.distribute_partial_sum([a, b])
  (s, t) = flow.advanced.distribute_broadcast(y)
  print(x.shape, y.shape, s.shape, t.shape)
  return s, t

index = [-2, -1, 0, 1, 2]
data = []
for i in index: data.append(np.ones((1, 5), dtype=np.float32) * i)
for x in data: print(DistributeBroadcast(x).get())