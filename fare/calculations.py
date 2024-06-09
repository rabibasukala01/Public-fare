
import requests
def distance_duration_calculation(startcoords,endcoords):   #(lng,lat),(lng,lat)
    """
    https://project-osrm.org/docs/v5.22.0/api/#requests
    """
    response=requests.get(f"https://router.project-osrm.org/route/v1/driving/{startcoords};{endcoords}?alternatives=false&steps=false&overview=false&generate_hints=false").json()

    # in second and meter
    return float(response['routes'][0]['duration'])/60 , float(response['routes'][0]['distance'])/1000

# datapoints source
# https://myrepublica.nagariknetwork.com/news/public-transport-fare-goes-up-as-noc-hikes-diesel-price-1/

class CostCalculation:
    def __init__(self):
        self.data_points =[(5, 19), (10, 26), (15, 31), (20, 35)] # (km,rs)

    def linear_interpolation(self,x, x1, y1, x2, y2):
        """
        Perform linear interpolation to find the value of y for a given x
        between two points (x1, y1) and (x2, y2).
        """
        return y1 + ((x - x1) * (y2 - y1)) / (x2 - x1)

    def calculate_cost(self,distance):
        """
        Calculate the cost for a given distance using linear interpolation.
        """

        # Handling cases where distance is less than 5 or greater than 20
        if distance < 5:
            return 19
        elif distance >= 20:
            return 40

        # Find the appropriate data points for interpolation
        for i in range(len(self.data_points) - 1):
            if distance >= self.data_points[i][0] and distance < self.data_points[i + 1][0]:
                return self.linear_interpolation(distance, self.data_points[i][0], self.data_points[i][1], self.data_points[i + 1][0], self.data_points[i + 1][1])

if __name__ == "__main__":
    distance=14.4
    cost_calculator = CostCalculation()
    print(f"Cost for {distance} km: Rs {cost_calculator.calculate_cost(distance)}")




