import sys, json

def estimated_price(mileage, theta0, theta1):
    return theta0 + (theta1 * mileage)

def normalize_input(mileage, mean, std):
    return (mileage - mean) / std

def denormalize_output(normalize_price, mean, std):
    return normalize_price * std + mean

mean_mileage = 101066.25
std_mileage = 51565.1899106445
mean_price = 6331.833333333333
std_price = 1291.8688873961714
theta0 = 2.0354088784794536e-16
theta1 = -0.8561394207905023

mileage = 61789

# normalized_mileage = normalize_input(mileage, mean_mileage, std_mileage)
# normalize_price = estimated_price(normalized_mileage, theta0, theta1)
# print(denormalize_output(normalize_price, mean_price, std_price))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("please enter the car mileage!")
    else:
        if sys.argv[1].isdigit():
            mileage = float(sys.argv[1])
            with open('Prediction_Data.json', 'r') as json_file:
                data = json.load(json_file)
            normalized_mileage = normalize_input(mileage, data["mean_mileage"], data["std_mileage"])
            normalize_price = estimated_price(normalized_mileage, data["theta0"], data["theta1"])
            print(denormalize_output(normalize_price, data["mean_price"], data["std_price"]))
        else:
            print("mileage must be Digits!")