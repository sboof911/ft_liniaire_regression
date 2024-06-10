import numpy as np
import json

def estimated_price(mileage, theta0, theta1):
    return theta0 + (theta1 * mileage)

def get_teta0(theta0, theta1, data):
    m = len(data)
    return (1/m) * np.sum([estimated_price(data[:, 0][i], theta0, theta1) - data[:, 1][i] for i in range(m)])

def get_teta1(theta0, theta1, data):
    m = len(data)
    return (1/m) * np.sum([(estimated_price(data[:, 0][i], theta0, theta1) - data[:, 1][i]) * data[:, 0][i] for i in range(m)])

def compute_cost(theta0, theta1, data):
    m = len(data)
    return (1/m) * np.sum([(estimated_price(data[:, 0][i], theta0, theta1) - data[:, 1][i])**2 for i in range(m)])

def normalize_data(data):
    mean_mileage = np.mean(data[:, 0])
    std_mileage = np.std(data[:, 0])
    mean_price = np.mean(data[:, 1])
    std_price = np.std(data[:, 1])
    data[:, 0] = (data[:, 0] - mean_mileage) / std_mileage
    data[:, 1] = (data[:, 1] - mean_price) / std_price
    return data, mean_mileage, std_mileage, mean_price, std_price

if __name__ == "__main__":
    initial_theta0 = 0
    initial_theta1 = 0
    precisions = [1, 0.1, 0.01, 0.001, 0.0001, 0.00001]
    best_precision = None
    best_theta0 = None
    best_theta1 = None
    num_iterations = 1000
    min_cost = float('inf')
    tolerance = 1e-8

    data = np.genfromtxt('data.csv', delimiter=',', skip_header=1)
    data, mean_mileage, std_mileage, mean_price, std_price = normalize_data(data)

    theta0 = initial_theta0
    theta1 = initial_theta1
    prev_cost = compute_cost(theta0, theta1, data)

    for learningRate in precisions:
        count = 0
        theta0 = initial_theta0
        theta1 = initial_theta1
        for _ in range(num_iterations):
            gradient_theta0 = get_teta0(theta0, theta1, data)
            gradient_theta1 = get_teta1(theta0, theta1, data)
            theta0 -= learningRate * gradient_theta0
            theta1 -= learningRate * gradient_theta1

            cost = compute_cost(theta0, theta1, data)
            if abs(prev_cost - cost) < tolerance:
                break

            prev_cost = cost

        # print(f"Alpha: {learningRate}, Cost: {cost}, theta0: {theta0}, theta1: {theta1}")
        if cost < min_cost:
            min_cost = cost
            best_precision = learningRate
            best_theta0 = theta0
            best_theta1 = theta1
    
    Predection = {
        "theta0":best_theta0,
        "theta1":best_theta1,
        "mean_mileage":mean_mileage,
        "std_mileage":std_mileage,
        "mean_price":mean_price,
        "std_price":std_price
    }
    with open('Prediction_Data.json', 'w') as json_file:
        json.dump(Predection, json_file, indent=4)