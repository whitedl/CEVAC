# WAP Experimentation
## What we want to address
* How accurate are signal-noise-ratio and received-signal-strength-indicator
  * Does this correlate well with vendor, Network, Device type, Distance,
* Can average session throughput be useful in filtering
* Can paths throughout the building be accurately measured,
* What users actually need to be counted (what measure reflects best)

## Filtering
Not all WAP data collected is useful for predicting occupancy. We have 3 databases
that collect different aggregations of the wap data. These databases are useful
for their own reasons, but do not show the same information.
* `CEVAC_WATT_WAP_HIST`
  * This database shows an hourly count of unique users by network per WAP
* `CEVAC_WATT_WAP_FLOOR_HIST`
  * This database shows an hourly count of unique users (as guests or clemson)
  per floor
* `CEVAC_WATT_WAP_DAILY_HIST`
  * This database shows a daily count of unique users in the entire building
  during the day
The WFIC WAPs support 4 networks
1. `eduroam`, the clemson staff/student/faculty network
   * This is used to predict clemson staff/student/faculty occupancy by username
2. `clemsonguest`, the open network for guests who visit clemson
   * This is used to predict occupancy based on username
     * The "test" username is filtered as unique users based on MAC Address
3. `resmedianet`, the network for staff/student/faculty IOT devices with the
potential for long-lasting, heavy connections, as to not clog the `eduroam` network
   * This is not used for predicting occupancy
4. `morrison`, the network for devices that cannot support modern protocols
   * This network is not used for predicting occupancy, as users don't use it for
   main devices

## Log
### 05/30
* For a basic experiment, Drew and Harrison walked around all floors of Watt to
test how they would be tracked in the hourly CSV (3 PM)
  * We both were only picked up on a single WAP during the entire hour, meaning
	that certain WAPs are not reporting consistently, are not reporting at all, or
	are being filtered
	* We found 44 unique waps reporting during this past week, there are ~46 in the
	building (meaning the basements waps are probably not reporting)

### 05/31, 06/3
* RSSI and SNR are both useful measures for determining signal strength
  * RSSI (received signal strength indicator) is a relative index for signal
	strength where -30 dBm is the best possible signal and -80 downward is borderline
	unusable
	* SNR (signal noise ratio, or S/N) is the ratio of signal to noise, where higher
	would be better by whatever order of magnitude than 1
* When looking through the wap logs, a great many session durations last for
approximately 5 minutes, 10 seconds
  * Since (I'm assuming) it doesn't take 5 minutes exactly for 99% of students to
	walk across the Building, this might be the default idle timeout for the
	wap network
* Why the 05/30 experiment didn't have the expected results, we don't yet know.
  * Zach A had an interesting theory that once a user's phone connects to the network,
	the association time is marked (this router will likely be one by the entrances),
	and within 5 minutes the user will be in the desired room they will be for an hour
	or so. After 5 minutes, the initial router will check for the user (even though
	it already handed the user off) and mark the dissociation time. The new router
	will not mark association/dissociation time because it was handed the user. The
	reason users my show up again while they are in the building is because they
	will open up their laptops throughout the day and laptops usually turn wifi of
	while in sleep.
	* I'm going to filter the data to see if this could be true
	```
	c-wfic-1-108ne-ap2702i-32 7
	c-wfic-3-310s-ap2702i-111 13
	c-wfic-3-316s-ap2702i-55 21
	c-wfic-3-316n-ap2702i-112 30
	c-wfic-3-310n-ap2702i-56 33
	c-wfic-1-108se-ap2702i-39 33
	c-wfic-4-413-ap2802i-7 44
	c-wfic-1-100l-ap2702i-36 48
	c-wfic-4-444-ap2802i-11 50
	c-wfic-1-101a-ap2702i-40 54
	c-wfic-3-344c-ap2702i-49 55
	c-wfic-3-313-ap2702i-59 59
	c-wfic-4-416-ap2802i-8 62
	c-wfic-2-218-ap2702i-41 65
	c-wfic-1-108nw-ap2702i-34 76
	c-wfic-4-terrace-n-ap1562i-4 77
	c-wfic-1-106nw-ap2702i-38 78
	c-wfic-1-108sw-ap2702i-35 78
	c-wfic-4-408-ap2802i-6 78
	c-wfic-2-208sw-ap2702i-47 82
	c-wfic-2-200s-ap2702i-44 86
	c-wfic-3-344u-ap2702i-50 86
	c-wfic-2-208se-ap2702i-45 89
	c-wfic-1-113-ap2702i-27 93
	c-wfic-3-323-ap2702i-58 94
	c-wfic-4-418-ap2802i-9 94
	c-wfic-3-308-ap2702i-60 101
	c-wfic-4-401u-ap2802i-5 107
	c-wfic-1-112-ap2702i-31 110
	c-wfic-3-333-ap2702i-53 110
	c-wfic-2-208nw-ap2702i-46 113
	c-wfic-2-216-ap2702i-43 113
	c-wfic-4-433-ap2802i-10 120
	c-wfic-2-200n-ap2702i-42 124
	c-wfic-3-319-ap2702i-57 131
	c-wfic-3-300d-ap2702i-52 138
	c-wfic-1-102-ap2702i-33 152
	c-wfic-3-329-ap2702i-54 159
	c-wfic-1-106se-ap2702i-37 163
	c-wfic-3-303-ap2702i-61 163
	c-wfic-3-339e-ap2702i-51 219
	c-wfic-2-203-ap2702i-48 223
	c-wfic-4-terrace-s-ap1562i-3 278
	c-wfic-1-110-ap2702i-30 293
	```
	  * It would be expected that a few (2-4) waps would have an order of magnitude
		more connections less than 6 minutes than others, but this is not true, it
		appears linear
	* If connection time isn't considered, this data shows for the past week:
	```
	c-wfic-1-108ne-ap2702i-32 7
	c-wfic-3-316s-ap2702i-55 26
	c-wfic-3-310s-ap2702i-111 29
	c-wfic-3-316n-ap2702i-112 36
	c-wfic-3-310n-ap2702i-56 39
	c-wfic-1-108se-ap2702i-39 43
	c-wfic-1-108nw-ap2702i-34 87
	c-wfic-3-344c-ap2702i-49 95
	c-wfic-4-terrace-n-ap1562i-4 96
	c-wfic-1-100l-ap2702i-36 96
	c-wfic-4-444-ap2802i-11 100
	c-wfic-1-108sw-ap2702i-35 106
	c-wfic-3-344u-ap2702i-50 112
	c-wfic-3-313-ap2702i-59 114
	c-wfic-1-101a-ap2702i-40 114
	c-wfic-1-106nw-ap2702i-38 126
	c-wfic-4-413-ap2802i-7 128
	c-wfic-2-216-ap2702i-43 129
	c-wfic-2-218-ap2702i-41 131
	c-wfic-4-416-ap2802i-8 131
	c-wfic-4-401u-ap2802i-5 156
	c-wfic-2-200s-ap2702i-44 173
	c-wfic-1-112-ap2702i-31 178
	c-wfic-2-208se-ap2702i-45 186
	c-wfic-2-208sw-ap2702i-47 189
	c-wfic-4-418-ap2802i-9 189
	c-wfic-1-113-ap2702i-27 207
	c-wfic-3-319-ap2702i-57 209
	c-wfic-3-333-ap2702i-53 211
	c-wfic-3-323-ap2702i-58 216
	c-wfic-2-200n-ap2702i-42 222
	c-wfic-2-208nw-ap2702i-46 227
	c-wfic-1-102-ap2702i-33 228
	c-wfic-3-329-ap2702i-54 228
	c-wfic-1-106se-ap2702i-37 231
	c-wfic-4-408-ap2802i-6 239
	c-wfic-4-433-ap2802i-10 241
	c-wfic-3-308-ap2702i-60 252
	c-wfic-3-300d-ap2702i-52 269
	c-wfic-4-terrace-s-ap1562i-3 325
	c-wfic-3-303-ap2702i-61 345
	c-wfic-2-203-ap2702i-48 424
	c-wfic-3-339e-ap2702i-51 451
	c-wfic-1-110-ap2702i-30 547
	```
	  * WAP 110 is very logical, it is by the entrance that most people enter from
		* WAP 339 is used for offices, so it makes sense that many people use it
		* WAP 203 is less intuitive. Perhaps there has been a class in that room this
		week?
		* WAP 303 might also be offices
* On 06/03, to determine just how waps work, we'll be conducting the following:
  1. A second pass through the building
	   * Was the first pass an anomaly?
	2. Walking around the outside of the building (mainly testing the porch)
		 * Curious about RSSI
	3. Turning the wifi on and off at different locations
	   * We can check the IP address of the connected router via our phones: are
		 they different before and after connection? How often do they change throughout
		 the Watt center?
  4. Results
	   * Both Drew (2 devices) and Harrison (1 device) toured the building to test
		 the wap data, the room we stayed at for over 6 minutes was room 308
		   * The WAP data only picked up 2 locations per device
			   * Harrison's phone (actively connected and reconnected)
				   1. Room 203
					 2. Room 308
				 * Drew's phone (passively connected)
				   1. Room 106 south east
					 2. Room 308
				 * Drew's laptop (streaming the whole time)
				   1. Room 110 (note: this wasn't him coming to work, this was leaving for
					 the experiment)
					 2. Room 308
		 * What we found was as follows
		   1. WAP does not record each connection and disconnection
			    * Laptop theory is falsified
			 2. WAP *probably* does record which room you were in for over 5 minutes
			 3. WAP *probably* does not record the actual amount of time we were in the building
			    * We don't exactly know as we can't see readings from the basement
			 4. The connections we connected to are along the path we travelled
			 5. WAP logs rooms in/beside locations we are at for more than 5 minutes
			 (we eventually connect to a location we are at for a decent amount of time)

### 06/04
* Now that data can be filtered more easily, we would like to test how accurate
it is in measuring occupancy
  * Room 106 has 2 WAPS and 64 seats, we're going to be counting how many people
	are in the room and comparing it to the wap data
* Harrison and Drew met with Tim Howard and Dr. White and discussed the future
of the wap data
  * A per floor per hour count would be more enlightening
	* A unique per day
	* Morrison network devices are used for devices that can't do the modern protocols

### 06/05
* We counted the total occupancy of the building at ~10:45 on 06/04
  * When we filtered the data, we realized our count had only been 11% off of
	the filtered data (93 counted, 104 filtered)
	  * Upon further analysis, we realized that the filtered count for the entire
		building was probably more accurate than our actual count
		  * People may have left the building right before our count, or been in the
			bathroom, or even changed floors
		* The breakdown by floor is less accurate
	* We decided we will build more databases
	  * Our current database will exist to have the breakdown of unique IDs per
		room per hour
		* A new table of unique IDs in the building per hour, broken down by floor
		* A new table of unique IDs in the building per day

### 06/06
* We worked on filtering data per network per day, giving a unique user count for
the entire building. From our rote counts we found that this number is accurate
+/- 10%, but splitting this up by floor may yield less accurate results.
  * Our initial results for the past few weeks of data are:
	```
	date					edu  guest total
	2019-05-24    62   3     65
	2019-05-25    9    2     11
	2019-05-26    10   1     11
	2019-05-27    16   1     17
	2019-05-28    231  16    247
	2019-05-29    220  18    238
	2019-05-30    315  17    332
	2019-05-31    196  9     205
	2019-06-01    12   0     12
	2019-06-02    9    0     9
	2019-06-03    289  16    305
	2019-06-04    329  31    360
	2019-06-05    281  9     290
	2019-06-06    44   8     52
	```

## 06/10
* When doing our daily count, we noticed that guest vs clemson count didn't
correlate well with the data we received
  * Very few guests were apparently connected to the internet
  * This may be what "test" connections are used for, so I added them to our
  new CEVAC_WATT_WAP_FLOOR_HIST database

## 06/11
* After adding "test" accounts to the guest count, the numbers appear more accurate
* The CEVAC_WATT_WAP_FLOOR_HIST count is running and we began working on the daily script

## 06/12
* We now have `CEVAC_WATT_WAP_DAILY_HIST`

## 06/26
* When looking at orientation numbers, the waps are under-reporting by a large
margin
  * This is due to a mix of:
    1. New students not yet connecting to the internet
    2. New students not being in the WATT center long enough for the waps to
    pick them up
  ```
  date  actual  clemson guest (clemson+guest)
  6/7-  410     3       97    100
  6/10- 266     44      138   182
  6/11- 932     31      70    101
  6/13- 963     35      62    97
  6/17- 506     18      55    73
  6/18- 959     50      73    123
  6/20- 966     41      47    88
  6/24- 933     69      93    162
  6/26- 553     24      89    113
  ```
