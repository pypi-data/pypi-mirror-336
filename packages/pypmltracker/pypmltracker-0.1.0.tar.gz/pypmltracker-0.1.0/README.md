
# MLTracker: A Comprehensive ML Experiment Tracking Library

**MLTracker** is a powerful and flexible experiment tracking library designed for machine learning projects. It helps data scientists and ML engineers efficiently track, visualize, and manage their experiments. Whether you're training models locally or in the cloud, MLTracker provides all the tools you need to streamline your ML workflow and collaborate with your team.

---

## Features ✨

- 📊 **Experiment Tracking**: Log metrics, parameters, and artifacts during model training.
- 🖥️ **System Monitoring**: Track CPU, memory, disk, and GPU usage during experiments.
- 🔄 **Framework Integrations**: Native support for **PyTorch**, **TensorFlow**, and **scikit-learn**.
- 📈 **Visualization**: Interactive dashboard to visualize and compare experiments.
- 💾 **Storage Options**: Local storage and cloud storage (AWS S3) support.
- 🌐 **API**: Client-server architecture for team collaboration.

---
---

## 🔧 Used Libraries & Tools

- **🔗 PyTorch**: [![PyTorch](https://img.shields.io/badge/PyTorch-v1.9.0-blue?logo=pytorch)](https://pytorch.org)
- **🔗 TensorFlow**: [![TensorFlow](https://img.shields.io/badge/TensorFlow-v2.5.0-green?logo=tensorflow)](https://www.tensorflow.org)
- **🔗 scikit-learn**: [![scikit-learn](https://img.shields.io/badge/scikit--learn-v0.24.2-yellowgreen?logo=scikit-learn)](https://scikit-learn.org)
- **☁️ AWS S3**: [![AWS](https://img.shields.io/badge/AWS-S3-orange?logo=amazonaws)](https://aws.amazon.com/s3/)
- **📈 Plotly**: [![Plotly](https://img.shields.io/badge/Plotly-v4.14.3-82D4FF?logo=plotly)](https://plotly.com)
- **📦 MLTracker**: [![MLTracker](https://img.shields.io/badge/MLTracker-v1.0-0078D4?logo=python)](https://github.com/mltracker)

---

## Installation ⚙️

### Install MLTracker

To install **MLTracker**, use the following pip command:

```bash
pip install mltracker
```
## Optional Features
You can install specific features based on your needs:

- **PyTorch integration**:
```bash
pip install mltracker[pytorch]
```
- **TensorFlow integration**:
```bash
pip install mltracker[tensorflow]
```
- **scikit-learn integration**:
```bash
pip install mltracker[sklearn]
```
- **Cloud storage (AWS S3)**:

```bash

pip install mltracker[cloud]
```
- **All features (PyTorch, TensorFlow, scikit-learn, and Cloud)**:

```bash

pip install mltracker[all]
```

# Quick Start 🚀
**1. Initialize an Experiment**

```bash
import mltracker

experiment = mltracker.Experiment(
    project_name="my_project",
    run_name="first_run",
    config={"learning_rate": 0.01, "batch_size": 32}
)
experiment.log({"accuracy": 0.85, "loss": 0.35})
experiment.log_artifact("model", "model.pkl")
experiment.finish()
dashboard = mltracker.Dashboard()
dashboard.start(open_browser=True)
```


# Framework Integrations 🤖
MLTracker integrates with several popular machine learning frameworks. Below are examples of how to use MLTracker with PyTorch, TensorFlow, and scikit-learn.

```bash
import torch
import torch.nn as nn
import mltracker

experiment = mltracker.Experiment(project_name="pytorch_example")
tracker = mltracker.PyTorchTracker(experiment, log_gradients=True)
model = nn.Sequential(nn.Linear(10, 5), nn.ReLU(), nn.Linear(5, 1))
tracker.watch(model)

for epoch in range(10):
    loss = train_step(model, data)
    tracker.track_metrics({"loss": loss})
    val_accuracy = validate(model, val_data)
    tracker.on_epoch_end(epoch, model, {"val_accuracy": val_accuracy})
tracker.save_model(model, "final_model")
```




# System Monitoring 🖥️
Track system resources such as CPU, memory, and disk usage during your experiments.

```bash
import mltracker
import time

experiment = mltracker.Experiment(project_name="system_monitoring")
monitor = mltracker.SystemMonitor(experiment)
monitor.start()

for i in range(10):
    time.sleep(1)
    experiment.log({"step": i, "value": i * 2})
monitor.stop()
experiment.finish()
```

# Dashboard 📊
Start the MLTracker web dashboard to visualize and compare your experiments.

```bash
import mltracker

dashboard = mltracker.Dashboard(
    storage_dir="./mltracker_data",
    host="127.0.0.1",
    port=8000
)
dashboard.start(open_browser=True)
```

# Team Collaboration 🤝
MLTracker supports client-server architecture to facilitate team collaboration.

- **Server**
Start the server to expose MLTracker functionality via a REST API:

```bash
import mltracker

server = mltracker.MLTrackerServer(
    storage_dir="./mltracker_data",
    host="0.0.0.0",
    port=5000,
    api_key="your-secret-api-key"
)
server.start()
```


- **Client 📡**
Connect to the remote server and interact with it:

```bash
import mltracker

client = mltracker.MLTrackerClient(
    base_url="http://server-address:5000",
    api_key="your-secret-api-key"
)
projects = client.list_projects()
print("Projects:", projects)
```



# License 📜
MLTracker is licensed under the MIT License.

# Contributing 🤗
Contributions are welcome! If you’d like to contribute to the development of MLTracker, please feel free to submit a pull request.

