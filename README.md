README.md
Firstly, we need a dataset. Unable to find a suitable dataset online, I decided to collect data manually from various photos. These photos are divided into two groups: 'cheat' and 'normal'.
The file Model_for_test.ipynb assists us in using this dataset. It facilitates training and applying a CNN model to detect normal and cheat photos. I've saved the model as an H5 extension file, allowing anyone to use it without needing the dataset. However, if you find the model's performance unsatisfactory, you can create your own dataset and use it for all processes.
Afterward, I deployed it for a web app using the Flask library. I've also configured it to run on 0.0.0.0 host, enabling it to work across all devices on the same network. To achieve this, you need to create a new firewall rule to fit the port (for example, most commonly used is port 5000).
Please note that this code serves only as a demo. You're encouraged to improve upon it and follow along with my progress.










