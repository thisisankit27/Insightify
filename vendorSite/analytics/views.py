from django.shortcuts import render
import numpy as np  # For making numpy Arrays
import pandas as pd  # For making Data Frames
import matplotlib.pyplot as plt  # Data Visualization
import seaborn as sns  # Data Visualization
from sklearn.cluster import KMeans  # Clustering Algorithm

import io
import urllib, base64

# Create your views here.

def analytics(request):
    customer_data = pd.read_csv('templates/Kaggle Data/Mall_Customers.csv')
    X = customer_data.iloc[:,[2,3]].values
    # Within Cluster Sum Of Squares (WCSS): measures sum of distances of observations from their cluster centroids
    wcss = []

    for i in range(1,11):
        # init='k-means++' Initiation Step is best among others
        kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
        kmeans.fit(X)

        #.inertia_ : gives us the wcss value for the cluster
        wcss.append(kmeans.inertia_)
    
    sns.set()
    plt.plot(range(1,11), wcss)
    plt.title('Elbow Point Graph')
    plt.xlabel('Number of Clusters')
    plt.ylabel('WCSS')
    # plt.show()
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close()
    return render(request, 'analytics.html', {'data': uri})

def kMeans(request):
    if request.method == 'POST':
        numberOfCluster = request.POST['numberOfCluster']
        kmeans = KMeans(n_clusters=int(numberOfCluster), init='k-means++', random_state=0)
        customer_data = pd.read_csv('templates/Kaggle Data/Mall_Customers.csv')
        X = customer_data.iloc[:,[2,3]].values   
        Y = kmeans.fit_predict(X)
        plt.figure(figsize=(8,8))
        
        color = ['green', 'red', 'yellow', 'violet', 'blue', 'cyan', 'magenta'] 
        
        for i in range(0, int(numberOfCluster)):
            plt.scatter(X[Y==i,0], X[Y==i,1], s=50, c=color[i], label=('Cluster '+str(i+1)))
            
        plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1],  s=100, c='black', label='centroid')
        plt.title('Customer Groups')
        plt.xlabel('Annual Income')
        plt.ylabel('Spending Score')
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        plt.close()
        return render(request, 'kMeans.html', {'data': uri})
    else:
        return render(request, 'analytics.html')
