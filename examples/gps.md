# How GPS Works

The Global Positioning System, or GPS, is a satellite-based navigation system that allows a receiver on Earth to estimate its position and time. It is used in smartphones, cars, aircraft, ships, surveying equipment, scientific instruments, and many other systems. Although using GPS feels simple—open a map and wait for a location marker—the underlying process depends on precise timing, radio signals, orbital information, geometry, and corrections for several physical effects.

GPS works using a constellation of satellites orbiting Earth. Each satellite continuously broadcasts radio signals that contain two especially important pieces of information: the satellite's position in space and the precise time at which the signal was transmitted. The satellites carry highly accurate atomic clocks, allowing them to keep time much more precisely than an ordinary phone or navigation device.

A GPS receiver listens for signals from several satellites at the same time. When a signal arrives, the receiver compares the transmission time included in the signal with the time at which the signal was received. Radio waves travel at approximately the speed of light. Therefore, if the receiver knows how long the signal took to travel, it can estimate the distance between itself and the satellite.

The basic idea can be expressed as:

distance = signal travel time × speed of light

This sounds straightforward, but the required timing precision is extremely demanding. Light travels roughly 300,000 kilometers in one second, so even a very small timing error can create a large positioning error.

Knowing the distance to one satellite does not reveal a unique location. If a receiver is a certain distance from one satellite, it could be located anywhere on the surface of an imaginary sphere centered on that satellite. A measurement from a second satellite introduces another sphere. The possible locations are reduced to the intersection of those two spheres. A third satellite narrows the position further.

This geometric process is called trilateration. It differs from triangulation because GPS primarily uses measured distances rather than measured angles. In an idealized situation, distances from three satellites can determine a three-dimensional position.

Real GPS receivers normally use at least four satellites. The reason is that the receiver's clock is not as accurate as the atomic clocks aboard the satellites. Even a tiny clock error affects every measured signal travel time. The fourth satellite provides another equation, allowing the receiver to solve for both its three-dimensional position and its clock offset.

Satellite position is also important. It is not enough to know how far away a satellite is; the receiver must know where that satellite was when it transmitted the signal. GPS messages therefore include orbital information that allows the receiver to calculate the satellite's position.

Several sources of error can affect GPS measurements. Signals passing through the ionosphere and troposphere can be delayed. Buildings, mountains, and other surfaces can reflect radio signals, creating a phenomenon called multipath propagation. Satellite orbit predictions are not perfectly exact, and small clock errors can remain even in highly accurate satellite systems.

The geometry of the visible satellites also matters. If several satellites appear clustered in the same part of the sky, position estimates are generally less precise than when satellites are widely distributed. This effect is often described using dilution of precision.

Relativity must also be considered. GPS satellites move quickly relative to receivers on Earth, producing a special-relativistic effect on their clocks. At the same time, they orbit high above Earth's surface, where gravity is weaker, producing a general-relativistic effect in the opposite direction. These effects are small on everyday time scales but significant for a system that depends on nanosecond-level timing. GPS satellite clocks are therefore corrected so that relativistic effects do not accumulate into large navigation errors.

Modern GPS receivers often combine satellite measurements with other information. Smartphones may use Wi-Fi positioning, cellular networks, accelerometers, gyroscopes, or other satellite navigation systems. Vehicles and aircraft may combine GPS with inertial navigation systems.

GPS is therefore not simply a system that tells a device where it is. It is a carefully coordinated timing and measurement system. Satellites broadcast precise time and position data, receivers estimate distances from signal travel times, trilateration converts those distances into a position, and multiple corrections improve the final result. The familiar location marker on a map is the product of orbital mechanics, atomic clocks, radio engineering, geometry, and even Einstein's theory of relativity.
