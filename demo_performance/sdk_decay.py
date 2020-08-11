from modeltestSDK import SDKclient
import numpy
from qats.signal import find_maxima

from modeltestSDK import plot_timeseries

import time

start = time.perf_counter()

client = SDKclient()

campaign = client.campaign.get_by_name("STT")
test_name = "waveIrreg_2101"
sensor_name = "M206_COF X"
t_dur = 35

test = campaign.get_tests(type="floater")[test_name]

timeseries = test.get_timeseries()[sensor_name]

timeseries.get_data_points()

sensors = [timeseries.get_sensor()]
data = [timeseries.data_points.to_pandas()]

times, values = timeseries.to_arrays()

maxima, indices = find_maxima(values, retind=True)

Tn = []

# Defines relevant durations for the decay tests. Also obtains an average Tn-value for the test in question.
i = 1
t1 = times[indices[-i]]
t2 = t1 + t_dur

maxima, indices2 = find_maxima(values[(t1 < times) & (times <= t2)], retind=True)

Tn = numpy.mean(times[indices2[0:-2]] - times[indices2[1:-1]])

print("------------------------------------ SDK -------------------------------------")
print("Periods between maximas are: ")
print(times[indices2[0:-2]] - times[indices2[1:-1]])
print("Number of oscillations observed is", len(times[indices2[0:-2]] - times[indices2[1:-1]]))

print("Natural period for modeltest is", Tn, "seconds")
print("Full scale natural period is", Tn * numpy.sqrt(campaign.scale_factor), "seconds")

end = time.perf_counter()

plot_timeseries(data, test, sensors)

print("TOTAL COMPUTING TIME: ", end-start)