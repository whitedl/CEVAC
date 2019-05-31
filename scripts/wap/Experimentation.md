# WAP Experimentation
## What we want to address
* How accurate are signal-noise-ratio and received-signal-strength-indicator
  * Does this correlate well with vendor, Network, Device type, Distance,
* Can average session throughput be useful in filtering
* Can paths throughout the building be accurately measured,
* What users actually need to be counted (what measure reflects best)

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
