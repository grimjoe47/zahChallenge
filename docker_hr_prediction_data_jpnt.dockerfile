# Use the official Jupyter base image
FROM jupyter/base-notebook

# Install required packages, including pandas
RUN pip install pandas scikit-learn matplotlib

# Copy your Jupyter Notebook files into the container
COPY Challenge_Model-checkpoint.ipynb /home/jovyan/work/

# Set the default notebook to run the Jupyter Notebook server with a specific notebook filename
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "/home/jovyan/work/Challenge_Model-checkpoint.ipynb"]
